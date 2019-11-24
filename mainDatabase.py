#Chase Badalato
#SYSC3010 Design Project
#2019/11/04

#This code utilizes SQLite3 to reinitizlie a database for our E-tank

import sqlite3
import random
import socket, sys, time
import json
from datetime import datetime
#import thread
#This connects to our main database
connection = sqlite3.connect("projectDataBase.db")

#cursor (needed to code in SQL)
crs = connection.cursor()

def initializeDatabase():
    '''Initialize the database.  Create tables if they do not exist'''
    
    #Create a new table IF it doesnt exist
    turnOnForeign = """PRAGMA foreign_keys = ON;"""
    createTanks = """CREATE TABLE IF NOT EXISTS tanks(id INTEGER, name TEXT, location TEXT, petType TEXT, PRIMARY KEY(id));"""
    createSensorVals = """CREATE TABLE IF NOT EXISTS sensorVals(tank_id INTEGER, timeRecorded DATE, motion INTEGER, temperature FLOAT, targetTemp FLOAT, fed BOOLEAN, FOREIGN KEY(tank_id) REFERENCES tanks(id));"""
    
    try:
        #Execute the created commands
        crs.execute(turnOnForeign)
        crs.execute(createTanks)
        crs.execute(createSensorVals)
        #Save the changes to the files
        connection.commit()
        return True
    
    except:
        return False
    
def clearTables():
    crs.execute('''DROP TABLE IF EXISTS sensorVals;''')
    crs.execute('''DROP TABLE IF EXISTS tanks;''')
    connection.commit()
    
def addTank(tank_id, name, location, petType):
    '''Add a new tank entry into the database'''

    crs.execute('''INSERT or IGNORE INTO tanks VALUES(?, ?, ?, ?);''',(tank_id, name, location, petType))
    connection.commit()
    

#Add a new sensorValue to the database
def addSensVal(tank_id, timeRecorded, motion, temperature, targetTemp, fed):
    crs.execute('''INSERT INTO sensorVals VALUES(?, ?, ?, ?, ?, ?);''',(tank_id, timeRecorded, motion, temperature, targetTemp, fed))
    connection.commit()

#print the tank list
def printTankList():
    crs.execute("SELECT * FROM tanks;")
    tankVals = []
    for row in crs:
        #print(row)
        tankVals.append(row)
    #print("")
    return tankVals

#print the snesor value of a certain tank
def printSensorValList(tank_id):
    crs.execute("SELECT * FROM sensorVals;")
    sensVals = []
    for row in crs:
        #print(row)
        sensVals.append(row)
        
    return sensVals
        
#Gets data from UDP connection
def gatherInfo(s, port, server_address):
    while True:

        print ("Waiting to receive on port %d" % port)

        buf, address = s.recvfrom(port)
        if not len(buf):
            break

        print ("Received from %s %s: " % (address, buf ))
        jfile = json.loads(buf)

        infoPacket = breakDownPacket(address, jfile)
        
        break
      

#Send sensor values to GUI or Android app
def sendSensorVal(address, timeRequested):
    host = 'localHost'
    textport = 1026
                
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    port = int(textport)
    server_address = (host, port)
    
    print("About to send a value")
    time.sleep(2)

    crs.execute("SELECT * FROM sensorVals WHERE timeRecorded = ?;",(str(timeRequested)))
    for row in crs:
        print(row)

        data = {"tank_id": row[0], "timeRecorded" : row[1], "motion" : row[2], "temperature" : row[3], "targetTemp" : row[4], "fed": row[5]}
        sendIt = json.dumps(data)
        s.sendto(str(sendIt).encode('utf-8'), server_address)
    s.close()

def sendArduinoVal(address, fed, targetTemp):
    time.sleep(2)
    
    host = 'localHost'
    textport = 1026
                
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    port = int(textport)
    server_address = (host, port)

    data = {"targetTemp" : targetTemp, "fed": fed}
    sendIt = json.dumps(data)
    
    try:
        s.sendto(str(sendIt).encode('utf-8'), server_address)
    
    except:
        print("No Connection :/")
    s.close()
    
#Checks JSON "PacketType" to decide what JSON it is
def breakDownPacket(address, jfile):
    #add a new tank entry
    if jfile["packetType"] == "tank":
        addTank(jfile["tank_id"], jfile["name"], jfile["location"], jfile["petType"])
        
    #Add sensor value entry
    elif jfile["packetType"] == "sensorVal":
        
        addSensVal(jfile["tank_id"], jfile["timeRecorded"], jfile["motion"], jfile["temperature"], jfile["targetTemp"], jfile["fed"])
    
    #send sensor vals to GUI or App
    elif jfile["packetType"] == "requestSensVal":

        sendSensorVal(address, jfile["timeRequested"])
    
    elif jfile["packetType"] == "arduinoVal":
        sendArduinoVal(address, jfile["fed"], jfile["targetTemp"])
        
    else:
        print("JSON packet was not properly received")


