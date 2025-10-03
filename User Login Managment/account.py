import mysql.connector
import bcrypt

# Connects to aiven db
conn = mysql.connector.connect(
    host="mysql-30d350d9-stetson-f3bc.i.aivencloud.com",
    port=21547,
    user="avnadmin",
    password="AVNS_Dz1ct-QA5R6g5E3iM3T",
    database="defaultdb"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Accounts (
    Username VARCHAR(255) PRIMARY KEY,
    Password VARCHAR(255) NOT NULL
)
""")
conn.commit()

def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ").encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO Accounts (username, password) VALUES (%s, %s)",
            (username, hashed.decode("utf-8"))
        )
        conn.commit()
        print("Account created successfully!")
    except mysql.connector.errors.IntegrityError:
        print("Username already exists. Try another one.")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ").encode("utf-8")
    cursor.execute(
        "SELECT password FROM Accounts WHERE username=%s",
        (username,)
    )
    row = cursor.fetchone()
    if row and bcrypt.checkpw(password, row[0].encode("utf-8")):
        print(f"Welcome, {username}!")
    else:
        print("Invalid username or password.")

while True:
    print("Welcome to Sketchi!")
    print("\n1. Sign Up")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose: ")
    if choice == "1":
        signup()
    elif choice == "2":
        login()
    elif choice == "3":
        break
    else:
        print("Please try again.")
