import mainDatabase as db
import sqlite3
import random
import socket, sys, time
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 1025
server_address = ('', port)
s.bind(server_address)

db.clearTables()
db.initializeDatabase()

print('')
while True:
    db.gatherInfo(s, port, server_address)
    print('')

s.close()

