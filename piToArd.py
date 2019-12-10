'''
Chase Badalato, Chase Fridgen
101072570, 

Group m2
SYSC3010 Project
'''
import mainDatabase as db
import sqlite3
import random
import socket, sys, time
import json
import serial

'''This script sends values that are received from the RpiTwo to the arduino through UART connection'''

#Set up UART
port = "/dev/ttyACM0"#UART Port
baudrate = 9600
ser = serial.Serial(port, baudrate) #initializing the serial connection

#Set up UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 1027
server_address = ('', port)
s.bind(server_address)

'''Send message to Arduino'''
def tell(msg):
    msg = msg + '\n'
    x = msg.encode('ascii') # encode n send
    ser.write(x)

'''Wait on port 2027 for any UDP information.  If received it will try to convert some JSON values to "Fed" or "Target Temperature" to send to Arduino (Through tell function)'''
def gatherInfo():
    while True:

        #Get a fed val or targetTemp
        print ("Waiting to receive on port %d" % port)

        buf, address = s.recvfrom(port)
        if not len(buf):
            break

        print ("Received from %s %s: " % (address, buf))
        jfile = json.loads(buf)
        
        #The gathered info is then send to Arduino through tell
        sendVal = str(jfile["fed"]) + str(jfile["targetTemp"])
        
        tell(sendVal)

        break
    
'''Continuously poll gather info'''
while True:
    gatherInfo()
