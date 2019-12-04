#Chase Badalato, Chase Fridgen

#SYSC3010 Project Group M2
#November 25th 2019

'''This code receives values from the Arduino through UART and then sends them to the other RPi through UDP'''

from datetime import datetime
import serial
import sqlite3
import random
import socket, sys, time
import json
import thread

#Setup the UART communication
port = "/dev/ttyACM0"
baudrate = 9600
ser = serial.Serial(port, baudrate) #initializing the serial connection

testTemp = 25 #set temp in Rpi2
tempTrue = "True" #reference for testing 

'''This funtion encodes and sends to the arduino through the serial connection'''
def tell(msg): 
    msg = msg + '\n'
    x = msg.encode('ascii') # encode n send
    ser.write(x)

'''This funtion retrieves from the arduino and encodes it to a string'''
def hear():
    msg = ser.read_until() # read until a new line
    mystring = msg.decode('ascii')
    return mystring

'''This function takes care of excess unwanted characters coming when retrieving strings from hear()'''
def encodeString(msg):
    i = len(msg) #takes length of string
    newString = ""
    for i in range (0, (i - 2)): #traverses and inserts characters into a new String excluding the last two chars (unwanted chars)
        newString = newString + msg[i]
    
    return newString #returns new string

'''Send a JSON packet to the GUI to be update in realtime'''
def sendPacket(data):
    host = '169.254.164.162'
    textport = 1025

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = int(textport)
    server_address = (host, port)
    try: #Try to send data to the main database code
        sendIt = json.dumps(data)
        s.sendto(str(sendIt).encode('utf-8'), server_address)
        s.close()
        sendPacketAgain(data)
        
    except: #If the data cannot be sent it fails
        #print colored("Test FAILED", 'red')
        print("Could not send the requested data")

'''Send a packet of sensor values to RpiOne to get updated into database'''
def sendPacketAgain(data):
    host = '169.254.42.100'
    textport = 1029

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = int(textport)
    server_address = (host, port)
    try: #Try to send data to the main database code
        sendIt = json.dumps(data)
        s.sendto(str(sendIt).encode('utf-8'), server_address)
        s.close()

    except: #If the data cannot be sent it fails
        #print colored("Test FAILED", 'red')
        print("Could not send the requested data")
        
'''Wait until UART sends over values, and then convert them into JSON and send the values over UDP'''
while True:
    #thread.start_new_thread(testThread, ())
    tank = encodeString(hear())
    motion = encodeString(hear())
    temp = encodeString(hear())
    targTemp = encodeString(hear())
    fed = encodeString(hear())
    
    timeYes = str(datetime.now()) #Get the current time
    timeYes = timeYes[:-10] #Cut out the seconds as they are not needed
    
    data = {"tank_id": tank, "timeRecorded" : timeYes, "motion" : motion, "temperature" : temp, "targetTemp" : targTemp, "fed": fed, "packetType": "sensorVal"}
    print(data)
    
    sendPacket(data)



