import mainDatabase as db
import sqlite3
import random
import socket, sys, time
import json
import serial

port = "/dev/ttyACM0"#put your port here
baudrate = 9600
ser = serial.Serial(port, baudrate) #initializing the serial connection

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 1027
server_address = ('localhost', port)
s.bind(server_address)

def tell(msg):
    msg = msg + '\n'
    x = msg.encode('ascii') # encode n send
    ser.write(x)

def testThread():
    while True:

        print ("Waiting to receive on port %d" % port)

        buf, address = s.recvfrom(port)
        if not len(buf):
            break

        print ("Received from %s %s: " % (address, buf))
        jfile = json.loads(buf)

        sendVal = jfile["fed"] + jfile["temp"]
        tell(sendVal)

        break
while True:
    testThread()