#Chase^2
#SYSC3010 Project Group M2
#November 25th 2019

'''This code receives values from the Arduinp through UART and then sends them to the other RPi through UDP'''

from datetime import datetime
import serial
import sqlite3
import random
import socket, sys, time
import json
import thread

port = "/dev/ttyACM0"#put your port here
baudrate = 9600
ser = serial.Serial(port, baudrate) #initializing the serial connection

testTemp = 25 #set temp in Rpi2
tempTrue = "True" #reference for testing 

# def testThread():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     port = 1027
#     server_address = ('localhost', port)
#     s.bind(server_address)
#
#     while True:
#
#         print ("Waiting to receive on port %d" % port)
#
#         buf, address = s.recvfrom(port)
#         if not len(buf):
#             break
#
#         print ("Received from %s %s: " % (address, buf))
#         jfile = json.loads(buf)
#
#         infoPacket = breakDownPacket(address, jfile)
#
#         break


#This funtion encodes and sends to the arduino through the serial connection
def tell(msg): 
    msg = msg + '\n'
    x = msg.encode('ascii') # encode n send
    ser.write(x)

#This funtion retrieves from the arduino and encodes it to a string
def hear():
    msg = ser.read_until() # read until a new line
    mystring = msg.decode('ascii')  # decode n return 
    return mystring

#This function takes care of excess unwanted characters coming when retrieving strings from hear()
def encodeString(msg):
    i = len(msg) #takes length of string
    newString = ""
    for i in range (0, (i - 2)): #traverses and inserts characters into a new String excluding the last two chars (unwanted chars)
        newString = newString + msg[i]
    
    return newString #returns new string

def sendPacket(data):
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
    

#This is the main code that is ran
while True:
    #thread.start_new_thread(testThread, ())
    tank = encodeString(hear())
    motion = encodeString(hear())
    temp = encodeString(hear())
    targTemp = encodeString(hear())
    fed = encodeString(hear())
    timeYes = str(datetime.now())
    timeYes = timeYes[:-6]
    data = {"tank_id": tank, "timeRecorded" : timeYes, "motion" : motion, "temperature" : temp, "targetTemp" : targTemp, "fed": fed, "packetType": "sensorVal"}
    print(data)
    sendPacket(data)



