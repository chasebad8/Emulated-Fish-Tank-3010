# Source: https://pymotw.com/2/socket/udp.html
import random
import socket, sys, time
import json

#host = sys.argv[1]
host = 'localHost'
#textport = sys.argv[2]
textport = 1025

n = 10

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)
count = 0

#while count <= n:

#data = {"tank_id": count, "name" : "Joe", "location" : "New York", "petType": "Salamander", "packetType": "tank"}
data = {"tank_id": count, "timeRecorded" : "5", "motion" : "10", "temperature" : "23.5", "targetTemp" : "22.1", "fed": "False", "packetType": "sensorVal"}

sendIt = json.dumps(data)
#s.sendall(data.encode('utf-8'))
s.sendto(str(sendIt).encode('utf-8'), server_address)
count += 1
    
s.close()

