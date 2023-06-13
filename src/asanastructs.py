class Story:
    def __init__(self, data):
        self.gid = data['gid']
        self.created_at = data['created_at']
        self.created_by = User(data['created_by'])
        self.previews = data['previews']
        self.resource_type = data['resource_type']
        self.source = data['source']
        self.text = data['text']
        self.type = data['type']
        self.resource_subtype = data['resource_subtype']
        self.target = Task(data['target'])

class User:
    def __init__(self, user_data):
        if 'email' in user_data:
            self.gid = user_data['gid']
            self.email = user_data.get('email')
            self.name = user_data.get('name')
            self.photo = Photo(user_data.get('photo'))
            self.resource_type = user_data['resource_type']
            self.workspaces = []
            if 'workspaces' in user_data:
                for workspace_data in user_data['workspaces']:
                    self.workspaces.append(Workspace(workspace_data))
        else:
            self.gid = user_data['gid']
            self.resource_type = user_data['resource_type']

class Photo:
    def __init__(self, photo_data):
        if photo_data is not None:
            self.image_21x21 = photo_data.get('image_21x21')
            self.image_27x27 = photo_data.get('image_27x27')
            self.image_36x36 = photo_data.get('image_36x36')
            self.image_60x60 = photo_data.get('image_60x60')
            self.image_128x128 = photo_data.get('image_128x128')

class Workspace:
    def __init__(self, workspace_data):
        self.gid = workspace_data['gid']
        self.name = workspace_data['name']
        self.resource_type = workspace_data['resource_type']

class Task:
    def __init__(self, task_data):
        self.gid = task_data['gid']
        self.name = task_data['name']
        self.resource_type = task_data['resource_type']
        self.resource_subtype = task_data['resource_subtype']

class Event:
    def __init__(self, data):
        self.user = User(data['user'])
        self.created_at = data['created_at']
        self.action = data['action']
        self.resource = Resource(data['resource'])
        if data["parent"]:
            self.parent = Parent(data['parent'])
        else:
            self.parent = None

class Resource:
    def __init__(self, resource_data):
        self.gid = resource_data['gid']
        self.resource_type = resource_data['resource_type']
        self.resource_subtype = resource_data.get('resource_subtype')

class Parent:
    def __init__(self, parent_data):
        self.gid = parent_data['gid']
        self.resource_type = parent_data['resource_type']
        self.resource_subtype = parent_data.get('resource_subtype')

class DetailedTask:
    def __init__(self, data):
        self.gid = data['gid']
        self.actual_time_minutes = data['actual_time_minutes']
        self.assignee = User(data['assignee']) if data['assignee'] else None
        self.assignee_status = data['assignee_status']
        self.completed = data['completed']
        self.completed_at = data['completed_at']
        self.created_at = data['created_at']
        self.custom_fields = data['custom_fields']
        self.due_at = data['due_at']
        self.due_on = data['due_on']
        self.followers = [User(follower_data) for follower_data in data['followers']]
        self.hearted = data['hearted']
        self.hearts = data['hearts']
        self.liked = data['liked']
        self.likes = data['likes']
        self.memberships = [Membership(membership_data) for membership_data in data['memberships']]
        self.modified_at = data['modified_at']
        self.name = data['name']
        self.notes = data['notes']
        self.num_hearts = data['num_hearts']
        self.num_likes = data['num_likes']
        self.parent = Task(data['parent']) if data['parent'] else None
        self.permalink_url = data['permalink_url']
        self.projects = [Project(project_data) for project_data in data['projects']]
        self.resource_type = data['resource_type']
        self.start_at = data['start_at']
        self.start_on = data['start_on']
        self.tags = data['tags']
        self.resource_subtype = data['resource_subtype']
        self.workspace = Workspace(data['workspace'])

class Membership:
    def __init__(self, membership_data):
        self.project = Project(membership_data['project'])
        self.section = Section(membership_data['section'])


class Project:
    def __init__(self, project_data):
        self.gid = project_data['gid']
        self.name = project_data['name']
        self.resource_type = project_data['resource_type']

class Section:
    def __init__(self, section_data):
        self.gid = section_data['gid']
        self.name = section_data['name']
        self.resource_type = section_data['resource_type']

class Comment:
    def __init__(self, data):
        self.gid = data["data"]["gid"]
        self.created_at = data["data"]["created_at"]
        self.created_by = User(data["data"]["created_by"])
        self.hearted = data["data"]["hearted"]
        self.hearts = data["data"]["hearts"]
        self.is_edited = data["data"]["is_edited"]
        self.is_pinned = data["data"]["is_pinned"]
        self.liked = data["data"]["liked"]
        self.likes = data["data"]["likes"]
        self.num_hearts = data["data"]["num_hearts"]
        self.num_likes = data["data"]["num_likes"]
        self.previews = data["data"]["previews"]
        self.resource_type = data["data"]["resource_type"]
        self.source = data["data"]["source"]
        self.text = data["data"]["text"]
        self.type = data["data"]["type"]
        self.resource_subtype = data["data"]["resource_subtype"]
        self.target = Task(data["data"]["target"])