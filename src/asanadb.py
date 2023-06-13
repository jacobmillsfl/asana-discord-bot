from tinydb import TinyDB, Query

class HookSecretManager:
    """
    Simple Database
    """
    def __init__(self, db_path):
        self.db = TinyDB(db_path)
        self.hook_secrets_table = self.db.table('hook_secrets')
        self.resources_table = self.db.table('resources')

    # Table: Hook_Secrets

    def insert_hook_secret(self, hook_secret):
        self.hook_secrets_table.insert({'hook_secret': hook_secret})

    def get_latest_hook_secret(self):
        result = self.hook_secrets_table.all()
        if result:
            return result[-1]['hook_secret']
        return None

    def delete_all_secrets(self):
        self.hook_secrets_table.truncate()

    # Table: Resource

    def insert_resource(self, gid):
        self.resources_table.insert({'gid': gid})

    def search_resource_by_gid(self, gid):
        Resource = Query()
        result = self.resources_table.search(Resource.gid == gid)
        return result

    def delete_all_resources(self):
        self.resources_table.truncate()