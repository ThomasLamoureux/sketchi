# sketchi
A communication and collaboration app made for artists.

# Setup
1. Clone the repository

2. Install dependencies:
```
pip install -r requirements.txt
```

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

## Starting The Client
1. Open the client directory in a seperate terminal:
```
cd .\Client
```
2. Start the client:
```
python -m client
```

3. If the server is running on the same device as the client, connect by entering "localhost" and then the port number seperated by a colan (eg, localhost:8000)

4. If you are connecting from a secondary device, make sure that both devices are on the same network. Enter the ip address of the server device followed by the port seperated by a colon. (eg, 192.0.0.1:8000)\
**(IMPORTANT, please note that connecting from a secondary device is currently very unstable due to some issues with server to client communication.)**



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
### Week 5; 10/6 - 10/10
- Added changes to the database, for security made them to be hashed by using bcrypt. Also created two new tables in the database. Teams and TeamManager that creates a team 5 or so. Later on the main goal is to have User1 and User2 draw and communicate live time. Will work with backend for this. - LA
- Revamped app GUI - BW
- Revamped connection and login GUI - TL
- Setup collaboration drawing with new GUI - TL


# Group Members:
- Thomas Lamoureux
- Bridget Wexler
- Luke Alley
