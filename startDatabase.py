'''
Chase Badalato
101072570
Group m2
SYSC3010 Project

This code starts the database loop.  It clears the tables, reinitializes the database and calls gatherInfo
'''

import mainDatabase as db
import sqlite3
import random
import socket, sys, time
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 1025
server_address = ('', port)
s.bind(server_address)

#This calls the mainDatabase code
db.clearTables()
db.initializeDatabase()

print('')
while True:
    #forever gather info
    db.gatherInfo(s, port, server_address)
    print('')

s.close()

