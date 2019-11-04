#Chase Badalato
#SYSC3010 Design Project
#2019/11/04

#This code utilizes SQLite3 to create a database for our E-tank

import sqlite3
import random

#This connects to our main database
connection = sqlite3.connect("projectDataBase.db")

#cursor (needed to code in SQL)
crs = connection.cursor()

tank_id = 0
temperature = 0
names = ["John", "Steven", "Greg", "Harriet", "Bob"]

for i in range(5):
    tank_id += 1
    temperature = random.uniform(17.1, 23.5)
    
    crs.execute('''INSERT or IGNORE INTO tanks VALUES(?, ?, ?);''',(tank_id, names[i], "test"))
    crs.execute('''INSERT INTO sensorVals VALUES(?, ?, ?, ?, ?, ?);''',(tank_id, 0, 0, temperature, "Today", True))
    
#Execute the created commands
#crs.execute(tankOne)
#crs.execute(sensValsOne)

#Save the changes to the files
connection.commit()

crs.execute("SELECT * FROM tanks;")
for row in crs:
    print(row)

print("")

crs.execute("SELECT * FROM sensorVals;")
for row in crs:
    print(row)

connection.close()

#tankOne = '''INSERT or IGNORE INTO tanks VALUES(?, ?, ?);''',(tank_id, "test", "test")
#sensValsOne = ("""INSERT INTO sensorVals VALUES(?, ?, ?, ?, ?, ?);""",(tank_id, None, None, temperature, None, True))