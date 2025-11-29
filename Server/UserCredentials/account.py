import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Trinity123",
    database="sketchi_db"
)
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
    Friends JSON
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

def signup(username, password, email):
    verification_code = "67694201738"  # swtich 

    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

    try:
        cursor.execute(
    "INSERT INTO Accounts (Username, Email, Password, Email_Verified, Email_Verification_Code, Projects, Friends) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    (username, email, hashed, False, verification_code, "{}", "[]")
        )
        conn.commit()

        print("DEBUG Verification Code:", verification_code)
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

    if row and bcrypt.checkpw(password.encode("utf-8"), row[0].encode("utf-8")):
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

if __name__ == "__main__":
    current_user = None

    while True:
        if not current_user:
            print("Welcome to Sketchi!")
            print("\n1. Sign Up")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose: ")

            if choice == "1":
                username = input("Enter a username: ")
                email = input("Enter Email: ")
                password = input("Enter a password: ")

                result = signup(username, password.encode("utf-8"), email)

                if result == 1:
                    print("Account Created!")
                else:
                    print("That username or email is taken.")

            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")

                result = login(username, password)

                if result == 1:
                    current_user = username
                    print(f"Success! Welcome, {username}!")
                else:
                    print("Invalid credentials.")

            elif choice == "3":
                break

            else:
                print("Please try again.")

        else:
            print(f"\nLogged in as: {current_user}")
            print("1. Create Team")
            print("2. Logout")
            choice = input("Choose: ")

            if choice == "1":
                create_team(current_user)

            elif choice == "2":
                current_user = None

            else:
                print("Please try again.")
