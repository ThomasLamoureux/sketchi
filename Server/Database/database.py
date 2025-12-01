import mysql.connector
import bcrypt
import configparser

import Main.EmailVerification as EmailVerification

conn = None
cursor = None


def init():
    global conn
    global cursor

    config_file = "Config_Files/database_config.ini"
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
        account_id INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(255) UNIQUE NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL,
        Password VARCHAR(255) NOT NULL,
        Email_Verified BOOLEAN DEFAULT FALSE,
        Email_Verification_Code VARCHAR(255),
        Projects JSON,
        Friends JSON,
        Profile_Picture MEDIUMBLOB
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Servers (
        server_id INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        Owner VARCHAR(255),
        FOREIGN KEY (Owner) REFERENCES Accounts(Username),
        Members JSON,
        Channels JSON,
        Icon MEDIUMBLOB
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


def signup(username, email, password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")


    verification_code = ""
    verification_enabled = EmailVerification.check_verification_enabled()
    verified = False


    if verification_enabled == True:
        verified = True
    else:
        verification_code = EmailVerification.generate_verification_code()
    
    try:
        cursor.execute(
            "INSERT INTO Accounts (Username, Email, Password, Email_Verified, Email_Verification_Code, Projects, Friends, Profile_Picture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (username, email, hashed, verified, verification_code, "{}", "[]", None)
        )
        conn.commit()

        return 1

    except mysql.connector.errors.IntegrityError as e:
        print("IntegrityError:", e)
        return 0
    

def get_data_from_account(username, field):
    try:
        cursor.execute(
            f"SELECT {field} FROM Accounts WHERE Username=%s",
            (username,)
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def set_data_in_account(username, field, value):
    try:
        cursor.execute(
            f"UPDATE Accounts SET {field}=%s WHERE Username=%s",
            (value, username)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False


def add_channel_message(server, channel_name, message, user, time):
    data = {"message": message, "user": user, "time": time}



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