from Connected_User import Connected_User


connected_users = []


def find_user_by_id(id):
    pass



def find_user_by_username(username):
    pass


def add_user(connection, address):
    user = Connected_User(connection, address)

    connected_users.append(user)

    return user