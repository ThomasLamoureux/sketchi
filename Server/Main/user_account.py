class UserAccount:
    def __init__(self, client_id, username):
        self.client_id = client_id
        self.username = username


    def get_id(self):
        return self.client_id



    def get_projects(self):
        pass