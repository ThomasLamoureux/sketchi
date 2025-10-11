# sketchi

How To:
Firstly, clone the repository onto your machine and install dependencies. (customtkiner, pillow, mysql-connector-python, bcrypt)


To start the server, open a terminal and open the server directory. (cd command)
Then run the command "**python -m server**"
Make note of the ip address and port number that appears in the terminal.


To start the client, open the client directory in a seperate terminal.
Then run the command "**python -m client**"

If the server is running on the same device as the client, connect by entering "localhost" and then the port number seperated by a colan (eg, localhost:5000)

If you are connecting from a secondary device, make sure that both devices are on the same network. Enter the ip address of the server device followed by the port seperated by a colon. (eg, 192.0.0.1:5000)



Miles stones:
Week 2; 9/8 - 9/14
- Basic Paint Prototype established - TL
- Deployed a MySQL Database using python to script in it. Using the free service Aiven has. - LA
Week 3; 9/15 - 9/21
- Created a python script that is connected to the MySQL database and Aiven server. It properly creates and stores a Username and Password in a table within MySQL - LA
- Continued development of Paint software
Week 4; 9/22 - 9/28
- Development of Messaging Systems - TL
Week 5; 10/6 - 10/10
- Added changes to the database, for security made them to be hashed by using bcrypt. Also created two new tables in the database. Teams and TeamManager that creates a team 5 or so. Later on the main goal is to have User1 and User2 draw and communicate live time. Will work with backend for this. - LA
