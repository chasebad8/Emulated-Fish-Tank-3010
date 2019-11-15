#Chase Badalato
#SYSC3010 Design Project
#2019/11/04

#This code utilizes SQLite3 to reinitizlie a database for our E-tank

import sqlite3
import random
import socket, sys, time
import json
from datetime import datetime
#This connects to our main database
connection = sqlite3.connect("projectDataBase.db")

#cursor (needed to code in SQL)
crs = connection.cursor()

def initializeDatabase():
    #Create a new table IF it doesnt exist
    turnOnForeign = """PRAGMA foreign_keys = ON;"""
    createTanks = """CREATE TABLE IF NOT EXISTS tanks(id INTEGER, name TEXT, location TEXT, petType TEXT, PRIMARY KEY(id));"""
    createSensorVals = """CREATE TABLE IF NOT EXISTS sensorVals(tank_id INTEGER, timeRecorded DATE, motion FLOAT, temperature FLOAT, targetTemp FLOAT, fed BOOLEAN, FOREIGN KEY(tank_id) REFERENCES tanks(id));"""

    #Execute the created commands
    crs.execute(turnOnForeign)
    crs.execute(createTanks)
    crs.execute(createSensorVals)
    #Save the changes to the files
    connection.commit()
    
    return

#Add a new tank entry into the database
def addTank(tank_id, name, location, petType):
    crs.execute('''INSERT or IGNORE INTO tanks VALUES(?, ?, ?, ?);''',(tank_id, name, location, petType))
    connection.commit()
    
    return

#Add a new sensorValue to the database
def addSensVal(tank_id, timeRecorded, motion, temperature, targetTemp, fed):
    crs.execute('''INSERT INTO sensorVals VALUES(?, ?, ?, ?, ?, ?);''',(tank_id, timeRecorded, motion, temperature, targetTemp, fed))
    connection.commit()
    
    return

def printTankList():
    crs.execute("SELECT * FROM tanks;")
    for row in crs:
        print(row)
    print("")
    return

def printSensorValList(tank_id):
    crs.execute("SELECT * FROM sensorVals;")
    for row in crs:
        print(row)
    return

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
      
    return

def sendSensor(address, timeRequested):
    crs.execute("SELECT * FROM sensorVals WHERE timeRecorded = ?;",(str(timeRequested)))
    
    for row in crs:
        print(row)
        
        host = 'localHost'
        textport = 1025
                
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = int(textport)
        server_address = (host, port)

        data = {"tank_id": row[0], "timeRecorded" : row[1], "motion" : row[3], "temperature" : row[4], "targetTemp" : row[5], "fed": row[6]}

        sendIt = json.dumps(data)
        s.sendto(str(sendIt).encode('utf-8'), server_address)

    s.close()
    return
#Gathers all important information from the packet
def breakDownPacket(address, jfile):
    if jfile["packetType"] == "tank":
        addTank(jfile["tank_id"], jfile["name"], jfile["location"], jfile["petType"])
        
    elif jfile["packetType"] == "sensorVal":
        addSensVal(jfile["tank_id"], jfile["timeRecorded"], jfile["motion"], jfile["temperature"], jfile["targetTemp"], jfile["fed"])
    
    elif jfile["packetType"] == "requestSensVal":
        sendSensor(address, jfile["timeRequested"])
        
    else:
        print("JSON packet was not properly received")
    return



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 1025
server_address = ('localhost', port)
s.bind(server_address)

initializeDatabase()
print('Database Initialized Successfully')
print('')
while True:
    gatherInfo(s, port, server_address)
    print('')

s.close()

