


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
