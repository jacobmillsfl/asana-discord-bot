#!/usr/bin/env python

import asana, sys, os, json, logging, signal, threading, hmac, hashlib
import discord
from flask import Flask, request, make_response
from src.asanastructs import User, Workspace, Story, Task, Event, Resource, Parent, Photo, DetailedTask, Comment
import asyncio
import json
import requests
from src.discordutil import DiscordUtil
from src.asanadb import HookSecretManager

# Check and set our environment variables
config = {
    'PAT': None,
    'WORKSPACE': None,
    'PROJECT': None,
    'TOKEN': None,
    'GUILD': None,
    'ASANA_CHANNEL': None
}

if 'TEMP_PAT' in os.environ \
    and 'ASANA_WORKSPACE' in os.environ \
    and 'ASANA_PROJECT' in os.environ \
    and 'TOKEN' in os.environ \
    and 'GUILD' in os.environ \
    and 'ASANA_CHANNEL' in os.environ:
    config['PAT'] = os.environ['TEMP_PAT']
    config['WORKSPACE'] = os.environ['ASANA_WORKSPACE']
    config['PROJECT'] = os.environ['ASANA_PROJECT']
    config['TOKEN'] = os.environ['TOKEN']
    config['GUILD'] = int(os.environ['GUILD'])
    config['ASANA_CHANNEL'] = int(os.environ['ASANA_CHANNEL'])
else:
    print("Error: Missing environment variables")
    quit()

# Get a python-asana client
asana_client = asana.Client.access_token(config['PAT'])

# Get a flask client
event_loop = asyncio.get_event_loop()
app = Flask('TAF Asana Discord Bot')
app.logger.setLevel(logging.INFO)

# Get a discord client
discord_client = DiscordUtil(config["TOKEN"], config["GUILD"], config["ASANA_CHANNEL"], app.logger)

# Get a database client
database = HookSecretManager("hook_secrets.json")

# We have to create the webhook in a separate thread, because client.webhooks.create
# will block until the handshake is _complete_, but the handshake cannot be completed
# unless we can asynchronously respond in receive_webhook.
# If running a server in a server container like gunicorn, a separate process
# instance of this script can respond async.
class CreateWebhookThread(threading.Thread):
    def run(self):
        # Note that if you want to attach arbitrary information (like the target project) to the webhook at creation time, you can have it
        # pass in URL parameters to the callback function
        webhook = asana_client.webhooks.create(resource=config['PROJECT'], target=f"https://asana.tafers.net/receive-webhook?project={config['PROJECT']}")

create_thread = CreateWebhookThread()

def get_all_webhooks():
    webhooks = list(asana_client.webhooks.get_all(workspace=config['WORKSPACE']))
    app.logger.info("All webhooks for this pat: \n" + str(webhooks))
    return webhooks

def teardown():
    webhooks = get_all_webhooks()
    if len(webhooks) == 0:
        app.logger.info("No webhooks")
    else:
        for hook in webhooks:
            try:
                asana_client.webhooks.delete_by_id(hook["gid"])
                app.logger.info("Deleted " + str(hook["gid"]))
            except Exception as e:
                print("Caught error: " + str(e))


# Initialize runtime
teardown()
database.delete_all_secrets()
database.delete_all_resources()
create_thread.start()

# @app.route("/create_webhook", methods=["GET"])
# def create_hook():
#     global create_thread
#     # First, try to get existing webhooks
#     webhooks = get_all_webhooks()
#     if len(webhooks) != 0:
#         return "Hooks already created: " + str(webhooks)
#     create_thread.start()
#     return """<html>
#     <head>
#       <meta http-equiv=\"refresh\" content=\"10;url=/all_webhooks\" />
#     </head>
#     <body>
#         <p>Attempting to create hook (may take up to 10s) Redirecting in 10s to <a href=/all_webhooks>/all_webhooks</a> to inspect.</p>
#     </body>"""



# Save a global variable for the secret from the handshake.
# This is crude, and the secrets will vary _per webhook_ so we can't make
# more than one webhook with this app, so your implementation should do
# something smarter.
@app.route("/receive-webhook", methods=["POST"])
def receive_webhook():
    app.logger.info("Headers: \n" + str(request.headers));
    app.logger.info("Body: \n" + str(request.data));

    hook_secret = database.get_latest_hook_secret()

    if "X-Hook-Secret" in request.headers:
        if hook_secret is not None:
            app.logger.warn("Second handshake request received. This could be an attacker trying to set up a new secret. Ignoring.")
        else:
            app.logger.info("New webhook")
            response = make_response("", 200)
            hook_secret = request.headers["X-Hook-Secret"]
            database.insert_hook_secret(hook_secret)
            response.headers["X-Hook-Secret"] = request.headers["X-Hook-Secret"]
            return response
    elif "X-Hook-Signature" in request.headers:
        signature = hmac.new(   hook_secret.encode('ascii', 'ignore'),
                                msg=request.data,
                                digestmod=hashlib.sha256).hexdigest()

        if not hmac.compare_digest(signature.encode(),
                request.headers["X-Hook-Signature"].encode('ascii', 'ignore')):
            app.logger.warn("Calculated digest does not match digest from API. This event is not trusted.")
            return
        contents = json.loads(request.data)
        app.logger.info("Received payload of %s events", len(contents["events"]))
        for event in contents["events"]:
            process_event(event)
        return ""
    else:
        # Asana heartbeat messages send an empty payload. An empty payload ideally does not have a signature.
        # Don't throw an error on empty or malformed payloads. Just return an empty response.
        #raise KeyError
        return ""

#############################
# Event Handling
#############################
def process_event(event_data):
    try:
        app.logger.info(f"Processing new event!!!\n\n{event_data}")
        event = Event(event_data)

        app.logger.info(f"Processing Event: {event.action}")

        existing_resource = database.search_resource_by_gid(event.resource.gid)
        if (existing_resource):
             app.logger.info(f"Ignoring duplicate resource ID: {event.resource.gid}")
        else:
            # Add to database
            database.insert_resource(event.resource.gid)

            if event.resource.resource_type == "story" \
                and event.resource.resource_subtype == "added_to_project":
                    app.logger.info("NEW STORY DETECTED: SPAWNING TASK")
                    event_loop.run_until_complete(handle_task(event))

            if event.resource.resource_type == "story" \
                and event.resource.resource_subtype == "added_to_task":
                    app.logger.info("NEW SUBSTORY DETECTED: SPAWNING TASK")
                    event_loop.run_until_complete(handle_task(event))

            if event.resource.resource_type == "story" \
                and event.resource.resource_subtype == "comment_added":
                    app.logger.info("NEW COMMENT DETECTED: SPAWNING TASK")
                    event_loop.run_until_complete(handle_comment(event))

            if event.resource.resource_type == "story" \
                and event.resource.resource_subtype == "marked_complete":
                    app.logger.info("NEW COMPLETION DETECTED: SPAWNING TASK")
                    event_loop.run_until_complete(handle_task_completion(event, True))

            if event.resource.resource_type == "story" \
                and event.resource.resource_subtype == "marked_incomplete":
                    app.logger.info("NEW COMPLETION DETECTED: SPAWNING TASK")
                    event_loop.run_until_complete(handle_task_completion(event, False))

    except Exception as ex:
        app.logger.error(ex)

async def handle_task_completion(event: Event, complete: bool):
    app.logger.info("Async: 'handle_task_completion' running....")
    asana_client = asana.Client.access_token(config['PAT'])
    story = Story(asana_client.stories.get_story(event.resource.gid))
    user = User(asana_client.users.get_user(story.created_by.gid))
    task = DetailedTask(asana_client.tasks.get_task(story.target.gid))
    update = "Complete" if complete else "Incomplete"
    status = ":white_check_mark:" if complete else ":x:"
    color = discord.Color.green() if complete else discord.Color.red()

    embed = discord.Embed(
        title=f"Task {update}: {task.name}",
        description=status,
        color=color,
        url=task.permalink_url
    )
    embed.set_author(
        name=user.name,
        icon_url=user.photo.image_21x21
    )
    embed.set_footer(
        text="- TYP"
    )
    discord_client.send_embed(embed.to_dict())

async def handle_comment(event: Event):
    app.logger.info("Async: 'handle_comment' running....")
    asana_client = asana.Client.access_token(config['PAT'])
    comment = Story(asana_client.stories.get_story(event.resource.gid))
    user = User(asana_client.users.get_user(comment.created_by.gid))
    task = DetailedTask(asana_client.tasks.get_task(comment.target.gid))

    embed = discord.Embed(
        title=f"New Comment: {task.name}",
        description = comment.text,
        color=discord.Color.blurple(),
        url=task.permalink_url
    )
    embed.set_author(
        name=user.name,
        icon_url=user.photo.image_21x21
    )
    embed.set_footer(
        text="- TAFBot"
    )
    discord_client.send_embed(embed.to_dict())

async def handle_task(event: Event):
    await asyncio.sleep(30)
    asana_client = asana.Client.access_token(config['PAT'])
    app.logger.info("Async: 'handle_task' running....")
    # Call Story API
    story = Story(asana_client.stories.get_story(event.resource.gid))
    user = User(asana_client.users.get_user(story.created_by.gid))
    task = DetailedTask(asana_client.tasks.get_task(story.target.gid))

    embed = discord.Embed(
        title=f"New Task: {task.name}",
        description=task.notes,
        color=discord.Color.blurple(),
        url=task.permalink_url
    )
    embed.set_author(
        name=user.name,
        icon_url=user.photo.image_21x21
    )
    embed.set_footer(
        text="- TAFBot"
    )

    embed.add_field(
         name = "Assigned To",
         value = task.assignee.name if task.assignee else "Unassigned",
         inline = False
    )

    discord_client.send_embed(embed.to_dict())
