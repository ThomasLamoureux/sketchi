


class Connected_User:
    

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address


    def set_id(self, id):
        self.id = id


    def disconnect(self):
        pass


    def get_address(self):
        return self.address
    

    def get_id(self):
        return self.id

    def get_connection(self):
        return self.connection


    def set_working_project(self, project):
        self.current_project = project


    def paint(self, args):
        if self.current_project:
            pass
