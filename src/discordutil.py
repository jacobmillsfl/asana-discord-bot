import json
import requests

class DiscordUtil:
    """
    Discord API helper
    """
    def __init__(self, token, guild, channel, logger):
        self.token = token
        self.guild = guild
        self.channel = channel
        self.logger = logger

    def send_embed(self, embed):
        self.logger.info("Attempting to send Discord embed")
        # Discord API endpoint for sending messages to a channel
        url = f'https://discord.com/api/v10/channels/{self.channel}/messages'

        headers = {
            'Authorization': f'Bot {self.token}',
            'Content-Type': 'application/json'
        }

        data = {
            'embeds': [embed]
        }

        # Convert the data to JSON format
        json_data = json.dumps(data)

        # Send a POST request to the Discord API
        response = requests.post(url, headers=headers, data=json_data)

        # Check the response status code
        if response.status_code == 200:
            self.logger.info('Discord Embed posted successfully.')
        else:
            self.logger.error('Failed to post the Discord embed.')
            self.logger.error(response.status_code)
            self.logger.error(response.text)

