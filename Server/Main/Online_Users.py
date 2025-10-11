from Main.Connected_User import Connected_User


connected_users = []


def find_user_by_id(id):
    pass



def find_user_by_username(username):
    pass


def remove_user(connection):
    pass


def add_user(connection, address):
    user = Connected_User(connection, address)

    connected_users.append(user)

    return user


def get_all():
    return connected_users