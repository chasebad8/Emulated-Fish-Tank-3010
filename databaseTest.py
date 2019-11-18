#Chase Badalato
#SYSC3010 Design Project
#2019/11/18

#This file contains 3 different Mocks.
#The GUI Mock, Arduino Mock, and the Android App Mock
import random
import mainDatabase as db
import socket, sys, time
import sqlite3
import json
#__________________________________
#GUI MOCK
#_________________________________

def testInitializeDatabase():
    db.initializeDatabase()
    return

def testAddNewTank(tankID, name, location, petType):
    host = 'localHost'
    textport = 1025
            
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = int(textport)
    server_address = (host, port)

    data = {"tank_id": int(tankID), "name" : name, "location" : location, "petType": petType, "packetType": "tank"}
    try:
        sendIt = json.dumps(data)
        s.sendto(str(sendIt).encode('utf-8'), server_address)

        s.close()
        
        print("Test PASSED!")
        
    except:
        print("Test FAILED")
        print("Could not send the requested data")
        
    return tankID

#MAIN PART OF SCRIPT
tankID = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

petNames = ["Stanley", "Freddy", "Betsy", "Henrietta", "Hank", "George", "Paulene", "Adrian", "Rocky", "Steven"]
petLocations = ["Main Room", "Back Room", "Cambodia", "Yukon"]
petTypes = ["Dog", "Cat", "Salamander", "Bird", "Lion", "Squirrel", "Elephant", "Komodo Dragon", "Python", "Ant"]

tempVal = {"21.4", "22.0", "23.2", "20.6", "19.9", "21.7", "24.2", "22.5", "18.2", "23.6"}
fedVal = {True, False}
motionVal = {"0", "8", "3", "9", "13", "18", "4", "15", "22", "24"}
timeRecordedVal = {"2019-01-06 15:06", "2018-03-17 8:32", "2019-04-19 4:20", "2019-09-3 13:56", "2018-06-16 12:24", "2019-11-17 21:43", "2019-7-24 6:30", "2016-12-20 0:23", "2017-2-28 14:41"}
targetTempVal = {"21.4", "22.0", "23.2", "20.6", "19.9", "21.7", "24.2", "22.5", "18.2", "23.6"}

usedVals[]

while True:
    print("Please choose an option below to begin a test:")
    print("")
    print("1) Initalize the database")
    print("2) Add a new tank")
    print("3) Add an existing tank")
    print("4) Send sensor values")
    print("5) Receive sensor values")
    print("6) Send target temperature")
    print("")
    choice = input("Selection: ")
    print("")
    
    if choice == "1":
        testInitializeDatabase()
        print("")
        
    elif choice == "2":
        valOne = random.randint(0,10)
        valTwo = random.randint(0,10)
        valThree = random.randint(0,4)
        valFour = random.randint(0,10)
        testAddNewTank(tankID[valOne], petNames[valTwo], petLocations[valThree], petTypes[valFour])
        usedVal.append(valOne)
        
    elif choice == "3":
        print('choice three')
#tempVal = []
#for i in range(0, 10):
    #randVal = random.uniform(18,22)
    #tempVal.append(randVal)

#print(tempVal)
