import mysql.connector

# Replace with your Aiven details
conn = mysql.connector.connect(
    host="mysql-30d350d9-stetson-f3bc.i.aivencloud.com",
    port=21547,
    user="avnadmin",
    password="AVNS_Dz1ct-QA5R6g5E3iM3T",  # paste the revealed password from Aiven
    database="defaultdb",
    ssl_ca="ca.pem"  # make sure ca.pem is in the same folder as this script
)

cursor = conn.cursor()

# Create a test table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
)
""")

# Insert example data
cursor.execute("INSERT INTO students (name) VALUES ('Alice')")
conn.commit()

# Query the table and print results
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()





