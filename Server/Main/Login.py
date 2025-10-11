import UserCredentials.account as account
import Main.Formatter as Formatter


def login(conn, address, username, password):
    result = account.login(username, password.encode("utf-8"))

    if result == 1:
        conn.sendall(Formatter.format_message("login", [1, username]))
    else:
        conn.sendall(Formatter.format_message("login", [-1]))



def sign_up(conn, address, username, password):
    result = account.signup(username, password.encode("utf-8"))

    if result == 1:
        conn.sendall(Formatter.format_message("signup", [1, username]))
    else:
        conn.sendall(Formatter.format_message("signup", [-1]))