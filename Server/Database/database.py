import mysql.connector
import bcrypt
import configparser

conn = None
cursor = None


def init():
    global conn
    global cursor

    config_file = 'Database/config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        conn = mysql.connector.connect(
            host=config.get('mysql', 'host'),
            port=config.getint('mysql', 'port'),
            user=config.get('mysql', 'user'),
            password=config.get('mysql', 'password'),
            database=config.get('mysql', 'database')
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("Please check your database configuration.")
        return

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Accounts (
        Username VARCHAR(255) PRIMARY KEY,
        Email VARCHAR(255) UNIQUE NOT NULL,
        Password VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teams (
        TeamID INT AUTO_INCREMENT PRIMARY KEY,
        TeamName VARCHAR(255) UNIQUE NOT NULL,
        CreatedBy VARCHAR(255),
        FOREIGN KEY (CreatedBy) REFERENCES Accounts(Username)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TeamMembers (
        TeamID INT,
        Username VARCHAR(255),
        PRIMARY KEY (TeamID, Username),
        FOREIGN KEY (TeamID) REFERENCES Teams(TeamID),
        FOREIGN KEY (Username) REFERENCES Accounts(Username)
    )
    """)
    conn.commit()


def signup(username, password):
    email = ("" + username + "@placeholder.com").encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
    try:
        cursor.execute(
            "INSERT INTO Accounts (Username, Email, Password) VALUES (%s, %s, %s)",
            (username, email, hashed)
        )
        conn.commit()
        return 1
    except mysql.connector.errors.IntegrityError as e:
        print("IntegrityError:", e)
        return 0

def login(username, password):
    cursor.execute(
        "SELECT Password FROM Accounts WHERE Username=%s",
        (username,)
    )
    row = cursor.fetchone()
    if row and bcrypt.checkpw(password, row[0].encode("utf-8")):
        return 1
    else:
        return 0

def create_team(username):
    team_name = input("Enter a new team name: ")
    try:
        cursor.execute(
            "INSERT INTO Teams (TeamName, CreatedBy) VALUES (%s, %s)",
            (team_name, username)
        )
        conn.commit()
        cursor.execute("SELECT TeamID FROM Teams WHERE TeamName=%s", (team_name,))
        team_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO TeamMembers (TeamID, Username) VALUES (%s, %s)",
            (team_id, username)
        )
        conn.commit()
        print(f"Team '{team_name}' created successfully!")
    except mysql.connector.errors.IntegrityError:
        print("That team name already exists.")



init()