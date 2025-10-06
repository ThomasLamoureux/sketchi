import mysql.connector
import bcrypt

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

def signup(username, password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO Accounts (username, password) VALUES (%s, %s)",
            (username, hashed.decode("utf-8"))
        )
        conn.commit()
        return 1 # Success
    except mysql.connector.errors.IntegrityError:
        return 0 # Failed

def login(username, password):
    cursor.execute(
        "SELECT password FROM Accounts WHERE username=%s",
        (username,)
    )
    row = cursor.fetchone()
    if row and bcrypt.checkpw(password, row[0].encode("utf-8")):
        return 1 # Success
    else:
        return 0 # Failed
        
if __name__ == "__main__":
    while True:
        print("Welcome to Sketchi!")
        print("\n1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            username = input("Choose a username: ")
            password = input("Choose a password: ").encode("utf-8")

            result = signup(username, password)
            if (result == 1):
                print("Created Account")
            else:
                print("That username is taken")
        elif choice == "2":
            username = input("Choose a username: ")
            password = input("Choose a password: ").encode("utf-8")

            result = login(username, password)

            if (result == 1):
                print("Success! Welcome, " + username + "!")
            else:
                print("Invalid credentials")
        elif choice == "3":
            break
        else:
            print("Please try again.")
