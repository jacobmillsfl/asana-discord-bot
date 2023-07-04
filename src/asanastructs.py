class Story:
    def __init__(self, data):
        self.gid = data.get('gid')
        self.created_at = data.get('created_at')
        self.created_by = User(data.get('created_by'))
        self.previews = data.get('previews')
        self.resource_type = data.get('resource_type')
        self.source = data.get('source')
        self.text = data.get('text')
        self.type = data.get('type')
        self.resource_subtype = data.get('resource_subtype')
        self.target = Task(data.get('target'))

class User:
    def __init__(self, user_data):
        self.gid = user_data.get('gid')
        self.email = user_data.get('email')
        self.name = user_data.get('name')
        self.photo = Photo(user_data.get('photo'))
        self.resource_type = user_data.get('resource_type')
        self.workspaces = []
        if 'workspaces' in user_data:
            for workspace_data in user_data.get('workspaces'):
                self.workspaces.append(Workspace(workspace_data))


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
        self.gid = workspace_data.get('gid')
        self.name = workspace_data.get('name')
        self.resource_type = workspace_data.get('resource_type')

class Task:
    def __init__(self, task_data):
        self.gid = task_data.get('gid')
        self.name = task_data.get('name')
        self.resource_type = task_data.get('resource_type')
        self.resource_subtype = task_data.get('resource_subtype')

class Event:
    def __init__(self, data):
        self.user = User(data.get('user'))
        self.created_at = data.get('created_at')
        self.action = data.get('action')
        self.resource = Resource(data.get('resource'))
        if data.get("parent"):
            self.parent = Parent(data.get('parent'))
        else:
            self.parent = None

class Resource:
    def __init__(self, resource_data):
        self.gid = resource_data.get('gid')
        self.resource_type = resource_data.get('resource_type')
        self.resource_subtype = resource_data.get('resource_subtype')

class Parent:
    def __init__(self, parent_data):
        self.gid = parent_data.get('gid')
        self.resource_type = parent_data.get('resource_type')
        self.resource_subtype = parent_data.get('resource_subtype')

class DetailedTask:
    def __init__(self, data):
        self.gid = data.get('gid')
        self.actual_time_minutes = data.get('actual_time_minutes')
        self.assignee = User(data.get('assignee')) if data.get('assignee') else None
        self.assignee_status = data.get('assignee_status')
        self.completed = data.get('completed')
        self.completed_at = data.get('completed_at')
        self.created_at = data.get('created_at')
        self.custom_fields = data.get('custom_fields')
        self.due_at = data.get('due_at')
        self.due_on = data.get('due_on')
        self.followers = [User(follower_data) for follower_data in data.get('followers', [])]
        self.hearted = data.get('hearted')
        self.hearts = data.get('hearts')
        self.liked = data.get('liked')
        self.likes = data.get('likes')
        self.memberships = [Membership(membership_data) for membership_data in data.get('memberships', [])]
        self.modified_at = data.get('modified_at')
        self.name = data.get('name')
        self.notes = data.get('notes')
        self.num_hearts = data.get('num_hearts')
        self.num_likes = data.get('num_likes')
        self.parent = Task(data.get('parent')) if data.get('parent') else None
        self.permalink_url = data.get('permalink_url')
        self.projects = [Project(project_data) for project_data in data.get('projects', [])]
        self.resource_type = data.get('resource_type')
        self.start_at = data.get('start_at')
        self.start_on = data.get('start_on')
        self.tags = data.get('tags')
        self.resource_subtype = data.get('resource_subtype')
        self.workspace = Workspace(data.get('workspace'))

class Membership:
    def __init__(self, membership_data):
        self.project = Project(membership_data.get('project'))
        self.section = Section(membership_data.get('section'))


class Project:
    def __init__(self, project_data):
        self.gid = project_data.get('gid')
        self.name = project_data.get('name')
        self.resource_type = project_data.get('resource_type')

class Section:
    def __init__(self, section_data):
        self.gid = section_data.get('gid')
        self.name = section_data.get('name')
        self.resource_type = section_data.get('resource_type')

class Comment:
    def __init__(self, data):
        self.gid = data["data"].get("gid")
        self.created_at = data["data"].get("created_at")
        self.created_by = User(data["data"].get("created_by"))
        self.hearted = data["data"].get("hearted")
        self.hearts = data["data"].get("hearts")
        self.is_edited = data["data"].get("is_edited")
        self.is_pinned = data["data"].get("is_pinned")
        self.liked = data["data"].get("liked")
        self.likes = data["data"].get("likes")
        self.num_hearts = data["data"].get("num_hearts")
        self.num_likes = data["data"].get("num_likes")
        self.previews = data["data"].get("previews")
        self.resource_type = data["data"].get("resource_type")
        self.source = data["data"].get("source")
        self.text = data["data"].get("text")
        self.type = data["data"].get("type")
        self.resource_subtype = data["data"].get("resource_subtype")
        self.target = Task(data["data"].get("target"))
