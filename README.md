# sketchi
A communication and collaboration app made for artists.
<br><br>

# Setup
1. Clone the repository

2. Install dependencies:
```
pip install -r requirements.txt
```

<br><br>
## Database Setup
1. Download MySQL Community Server from https://dev.mysql.com/downloads/ and complete the MySQL setup.
3. Open the MySQL Command Line Client.
4. Create a server for your data base using the command
```
CREATE DATABASE database_name;
```
5. Open the database_config.ini file under Server/Config_Files and enter your database name, the password you set for MySQL and the port number
<br><br>
## Email Setup (Optional)
Email verification is disabled by default. To turn on, open the email_config.ini file under Server/Config_Files and set enabled to true.
### Setup with Gmail account
1. Go to Google Account at https://myaccount.google.com/ and search App Passwords under Security.
2. Create a new App Password and save it.
3. Go to the email_config.ini file and enter the password, and your email that you're using.

<br><br>
## Server Setup
1. Open the server directory in a terminal:
```
cd .\Server
```
2. Start the server:
```
python -m server
```

3. Make note of the ip address and port number that appears in the terminal, this will be used for connecting from the client

<br><br>
## Starting The Client
### Method 1
1. Open the client directory in a seperate terminal:
```
cd .\Client
```
2. Start the client:
```
python -m client
```

### Method 2 ( WINDOWS SUPPORT ONLY )
1. Extract the App.zip file.
2. Run client.exe
<br><br>
### Connecting to server
1. If the server is running on the same device as the client, connect by entering "localhost" and then the port number seperated by a colan (eg, localhost:8000)
2. If you are connecting from a secondary device, make sure that both devices are on the same network. Enter the ip address of the server device followed by the port seperated by a colon. (eg, 192.0.0.1:8000)\
<br><br>
## (Client is only built for Windows. Mac must use method 1 to start, please note that Mac is not tested and may have issues.)
<br><br>
<br><br>

# Miles stones:
### Week 1; 8/31 - 9/7
- Established app idea and presented in class - TL, BW, LA
### Week 2; 9/8 - 9/14
- Basic Paint Prototype established - TL
- Deployed a MySQL Database using python to script in it. Using the free service Aiven has. - LA
### Week 3; 9/15 - 9/21
- Created a python script that is connected to the MySQL database and Aiven server. It properly creates and stores a Username and Password in a table within MySQL - LA
- Continued development of Paint software - TL
### Week 4; 9/22 - 9/28
- Started development of Messaging Systems - TL
- Basic app GUI established - BW
- Setup login and server connection with a GUI - TL
### Week 5/6; 9/29 - 10/10
- Added changes to the database, for security made them to be hashed by using bcrypt. Also created two new tables in the database. Teams and TeamManager that creates a team 5 or so. Later on the main goal is to have User1 and User2 draw and communicate live time. Will work with backend for this. - LA
- Revamped app GUI - BW
- Revamped connection and login GUI - TL
- Setup collaboration drawing with new GUI - TL
### Week 7/8/9; 10/11 - 11/1
- Bug fixes. - TL
- Improved connection handling. - TL
- Database improvements - LA
### Final month
- Added config files - TL
- Redid UI, improved it and added animations. - BW
- Email Verification - TL
- More Database Improvements - LA
- Overall Improvements to the app.



# Group Members:
- Thomas Lamoureux
- Bridget Wexler
- Luke Alley
