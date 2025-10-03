import mysql.connector

# Connect to Aiven MySQL
conn = mysql.connector.connect(
    host="mysql-30d350d9-stetson-f3bc.i.aivencloud.com",
    port=21547,
    user="avnadmin",
    password="AVNS_Dz1ct-QA5R6g5E3iM3T",
    database="defaultdb"
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Accounts (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
)
""")
conn.commit()

def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    try:
        cursor.execute(
            "INSERT INTO Accounts (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        print("Account created successfully!")
    except mysql.connector.errors.IntegrityError:
        print("Username already exists. Try another one.")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor.execute(
        "SELECT * FROM Accounts WHERE username=%s AND password=%s",
        (username, password)
    )
    if cursor.fetchone():
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
