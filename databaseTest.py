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
import os
import time
import threading
from threading import Thread
from os import system

#pip install termcolor
from termcolor import colored

'''This test initializes the database.  The db.initializeDatabase() returns true or false depending on if it properly initialized'''
def testInitializeDatabase():
    testPass = db.initializeDatabase()
    if testPass == True:
        print colored("Test PASSED!", 'green')
        time.sleep(1.5)
        return 1
    else:
        print colored("Test FAILED", 'red')
        print("The database was not initialized")
        time.sleep(1.5)
        return 0
    
'''This function send values to the database, emulating sending values from the arduino, android app, and GUI'''
'''Depending on what test is being run it will call specific functions to deal with the tests'''
def sendValue(data, testNum):
    host = 'localHost'
    textport = 1025
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = int(textport)
    server_address = (host, port)
    try: #Try to send data to the main database code
        sendIt = json.dumps(data)
        s.sendto(str(sendIt).encode('utf-8'), server_address)
        s.close()
    except: #If the data cannot be sent it fails
        print colored("Test FAILED", 'red')
        print("Could not send the requested data")
        return 0

    #Depending on what choice was made, after sending the code must call different functions
    if testNum == 1:
        #Must wait for the other code to actually append the sent data to the database
        time.sleep(1.5)
        return checkDatabase(data["tank_id"], data["name"], 3)        
    if testNum == 2:
        time.sleep(1.5)
        return checkDatabase(data["tank_id"], data["name"], 1)
    elif testNum == 3:
        time.sleep(1.5)
        return checkDatabase(data["tank_id"], data["name"], 2)
    elif testNum == 4:
        return receiveTempVal()
    elif testNum == 5:
        return checkDatabaseSensor(data)
    
    else:
        return

'''Check that the sensor values sent from the "Arduino" get saved into the database'''
def checkDatabaseSensor(data):
    time.sleep(0.5)
    allSens = db.printSensorValList(data["tank_id"])
    for i in allSens:
        print("Received: ", i[0], i[1], i[2], i[3], i[4], i[5])
        print("")
        if i[0] == data["tank_id"] and  i[1] == data["timeRecorded"] and int(i[2]) == int(data["motion"]) and float(i[3]) == float(data["temperature"]) and float(i[4]) == float(data["targetTemp"]) and i[5] == data["fed"]:
            print colored("Test PASSED!", 'green')
            print("")
            time.sleep(1.5)
            return 1
        
    print colored("Test FAILED", 'red')
    print("The correct values were not in the database")
    print("")
    time.sleep(1.5)
    return 0
    
'''This checks to see if the database contains a the proper entry in the actual db.  If testType = 1 then it checks if a value
was actually added to the db.  If testType = 2 then it checks that a tank entry DIDN'T get overriden by the new one'''
def checkDatabase(tankID, name, testType):
    
    #This checks the database to see if there is a new entry with the proper values
    allTanks = db.printTankList()
    for i in allTanks:
        #If test type 2 is selected
        if testType == 1:
            if i[0] == tankID:
                print("Received: ", i[0], i[1], i[2], i[3])
                print("")
                print colored("Test PASSED!", 'green')
                time.sleep(1.5)
                return 1
            
        #If test 3 is selected
        elif testType == 2:
            temp = i
            if temp[0] == tankID and temp[1] != name:
                print("Received: ", i[0], i[1], i[2], i[3])
                print("")
                print colored("Test PASSED!", 'green')
                time.sleep(1.5)
                return 1
            
        #When we just want to privatly look in database without printing
        elif testType == 3:
            if i[0] == tankID:
                testPass = True;
                return 1
    #If the fucntion has not returned after the for loop, there must be no entries, or an error occured
    print("")
    print colored("Test FAILED", 'red')
    print("Could not locate in database")
    time.sleep(1.5)
    return 0

'''Wait to receive requested temperature values from the database
This is checking if the mainDatabase can send out JSON to Arduino, GUI, and Android App'''
def receiveTempVal():
    host = 'localHost'
    textport = 1026
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = int(textport)
    server_address = (host, port)
    while True:
        print("Waiting to receive requested sensor reading on port 1026")
        print("Press CTL + C to break out if value is not received")
        
        try:
            buf, address = s.recvfrom(port)
            if not len(buf):
                break
            print ("ACK: %s" % (buf))
            
        except (KeyboardInterrupt):
            print("")
            print colored("Test FAILED", 'red')
            print("Never received requested sensor values")
            print("")
            time.sleep(1.5)
            return 0;
    s.close()
    
    return 0;

'''Super cool intro because I got bored...very fun'''
def intro():
    system('clear')
    print colored("Chase Badalato", "white", attrs=['bold'])
    print("")
    time.sleep(0.5)
    print colored("101072570", "white", attrs=['bold'])
    print("")
    time.sleep(0.5)
    print colored("SYSC3010 Test Cases", "white", attrs=['underline'])
    print("")
    time.sleep(0.5)
    print colored("November 25th 2019", "white", attrs=['underline'])
    time.sleep(1.5)

#____________________________________________________________
#MAIN PART OF SCRIPT
#____________________________________________________________

#The following are values that are randomly created to test against the mainDatabase code
tankID = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

#Random Tank Values
petNames = ["Stanley", "Freddy", "Betsy", "Henrietta", "Hank", "George", "Paulene", "Adrian", "Rocky", "Steven"]
petLocations = ["Main Room", "Back Room", "Cambodia", "Yukon"]
petTypes = ["Dog", "Cat", "Salamander", "Bird", "Lion", "Squirrel", "Elephant", "Komodo Dragon", "Ant", "Gecko"]

#Random Sensor Values
tempVal = ["21.4", "22.0", "23.2", "20.6", "19.9", "21.7", "24.2", "22.5", "18.2", "23.6"]
fedVal = [1, 0]
motionVal = ["0", "8", "3", "9", "13", "18", "4", "15", "22", "24"]
timeRecordedVal = ["2019-01-06_15:06", "2018-03-17_8:32", "2019-04-19_4:20", "2019-09-3_13:56", "2018-06-16_12:24", "2019-11-17_21:43", "2019-7-24_6:30", "2016-12-20_0:23", "2017-2-28_14:41", "2019-08-29_7:45"]
targetTempVal = ["21.4", "22.0", "23.2", "20.6", "19.9", "21.7", "24.2", "22.5", "18.2", "23.6"]


testsPassed = 0

intro()

while True:
    system('clear')
    print("___________________________________________________________________")
    print("")
    #Randomly generate numbers
    valOne = random.randint(0,9)
    valTwo = random.randint(0,9)
    valThree = random.randint(0,3)
    valFour = random.randint(0,9)
    valFive = random.randint(0,1)
    
    #Display a UI to choose a test
    print("Tests Passed so far: " + colored(str(testsPassed), 'cyan'))
    print("Please choose an option below to begin a test:")
    print("")
    print colored("GUI and Android App Mock", 'white', attrs=['bold'])
    print("1) Initalize the database")
    print("2) Add a new tank ID and values")
    print("3) Add an existing tank ID and new values (Should not work)")
    print("4) Request time specfic sensor values")
    print("")
    print colored("Arduino Mock", 'white', attrs=['bold'])
    print("5) Send sensor values to database")
    print("6) Rpi sends target temperature value and if pet should be fed")
    print("")
    print("8) Exit")
    print("___________________________________________________________________")
    print("")
    
    #choice = input("Selection: ")
    choice = raw_input ("Selection: ")
    print("")
    
    #Make decisions based on user input
    
    #Init DB
    if choice == "1":
        db.clearTables()
        testsPassed += testInitializeDatabase()
        print("")
    
    #Add Tank 
    elif choice == "2":
        db.clearTables()
        db.initializeDatabase()
        data = {"tank_id" : tankID[valOne], "name" : petNames[valTwo], "location" : petLocations[valThree], "petType" : petTypes[valFour], "packetType" : "tank"}
        print("Expected: ", tankID[valOne],  petNames[valTwo], petLocations[valThree], petTypes[valFour])
        testsPassed += sendValue(data, 2)
        print("")
        
    #Add Tank w/ existing ID
    elif choice == "3":
        db.clearTables()
        db.initializeDatabase()
        #Add a tank
        data = {"tank_id" : tankID[valOne], "name" : petNames[valTwo], "location" : petLocations[valThree], "petType" : petTypes[valFour], "packetType" : "tank"}
        print("Expected: ", tankID[valOne],  petNames[valTwo], petLocations[valThree], petTypes[valFour])
        sendValue(data, 1)
        
        #Generate more random numbers
        valTwo = random.randint(0,9)
        valThree = random.randint(0,3)
        valFour = random.randint(0,9)
        
        #TRY to add a tank with same ID but new values
        data = {"tank_id" : tankID[valOne], "name" : petNames[valTwo], "location" : petLocations[valThree], "petType" : petTypes[valFour], "packetType" : "tank"}
        testsPassed += sendValue(data, 3)
        print("")
    
    #Create 10 random sensors values and then search for 1 specfic one, and have it send it back
    elif choice == "4":
        db.clearTables()
        db.initializeDatabase()
        data = {"tank_id" : 0, "name" : petNames[valTwo], "location" : petLocations[valThree], "petType" : petTypes[valFour], "packetType" : "tank"}
        sendValue(data, None)
        idVals = []
        test = []
        for i in range(0, 10):
            #Generate random sensor values 10 times
            valOne = random.randint(0,9)
            valTwo = random.randint(0,9)
            valThree = random.randint(0,9)
            valFour = random.randint(0,9)
            valFive = random.randint(0,1)
            
            idVals.append(timeRecordedVal[valOne])
            
            data = {"tank_id": 0, "timeRecorded" : timeRecordedVal[valOne], "motion" : motionVal[valTwo], "temperature" : tempVal[valThree], "targetTemp" : targetTempVal[valFour], "fed": fedVal[valFive], "packetType": "sensorVal"}
            test.append(data)
            sendValue(data, None)
  
        randomExistingID = random.randint(0,9)
        
        print("Expected: Sensor values from time: " + idVals[randomExistingID])
        print("")
        for temp in test:
            if temp["timeRecorded"] == idVals[randomExistingID]:
                print(temp["tank_id"], temp["timeRecorded"], temp["motion"], temp["temperature"], temp["targetTemp"], temp["fed"])
        print("")
        data = {"timeRequested" : idVals[randomExistingID], "packetType" : "requestSensVal"}
        testsPassed += sendValue(data, 4)
    
    elif choice == "5":
        db.clearTables()
        db.initializeDatabase()
        data = {"tank_id" : 0, "name" : petNames[valTwo], "location" : petLocations[valThree], "petType" : petTypes[valFour], "packetType" : "tank"}
        sendValue(data, None)
        
        valOne = random.randint(0,9)
        valTwo = random.randint(0,9)
        valThree = random.randint(0,9)
        valFour = random.randint(0,9)
        valFive = random.randint(0,1)
        
        data = {"tank_id": 0, "timeRecorded" : 2, "motion" : motionVal[valTwo], "temperature" : tempVal[valThree], "targetTemp" : targetTempVal[valFour], "fed": fedVal[valFive], "packetType": "sensorVal"}
        print("Expected: ", data["tank_id"], data["timeRecorded"], data["motion"], data["temperature"], data["targetTemp"], data["fed"])
        testsPassed += sendValue(data, 5)
        
    elif choice == "6":
        print("Target Temperature: " + str(targetTempVal[valOne]))
        print("Feed Pet (1 yes, 0 no): " + str(fedVal[valFive]))
        print("Tank Number: " + str(0))
        print("")
        time.sleep(1)
        data = {"tank_id": 0, "targetTemp" : targetTempVal[valOne], "fed": fedVal[valFive], "packetType": "arduinoVal"}
        testsPassed += sendValue(data, 4)
        
    
    elif choice == "8":
        sys.exit()