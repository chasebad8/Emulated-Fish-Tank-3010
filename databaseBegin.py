#Chase Badalato
#SYSC3010 Design Project
#2019/11/04

#This code utilizes SQLite3 to reinitizlie a database for our E-tank

import sqlite3

#This connects to our main database
connection = sqlite3.connect("projectDataBase.db")

#cursor (needed to code in SQL)
crs = connection.cursor()

#Create a new table IF it doesnt exist
turnOnForeign = """PRAGMA foreign_keys = ON;"""
createTanks = """CREATE TABLE IF NOT EXISTS tanks(id INTEGER, name TEXT, location TEXT, PRIMARY KEY(id));"""
createSensorVals = """CREATE TABLE IF NOT EXISTS sensorVals(tank_id INTEGER, timeRecorded DATE, motion FLOAT, temperature FLOAT, targetTemp FLOAT, fed BOOLEAN, FOREIGN KEY(tank_id) REFERENCES tanks(id));"""

#Execute the created commands
crs.execute(turnOnForeign)
crs.execute(createTanks)
crs.execute(createSensorVals)

#Save the changes to the files
connection.commit()

connection.close()