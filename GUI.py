#Using tkinter for a GUI
#import tkinter as tk
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import  tkinter.ttk as ttk
import sqlite3
from functools import partial
#from mainDatabase import addTank

                #required database initializations
connection = sqlite3.connect("projectDataBase.db")#database connection
                #from lab, to access columns by name
connection.row_factory = sqlite3.Row
crs = connection.cursor()#database cursor
                
class Application(Tk):
        def __init__(self):
                #Initializations for the GUI
                super(Application, self).__init__()
                self.title("Strawberri E-tank system interface")
                self.minsize(1920, 1080)
                self.create_widgets()

        
        def create_widgets(self):
                tabControl = ttk.Notebook(self)#creates tab structure

                #FIRST TAB CONTENTS
                tab1 = ttk.Frame(tabControl)
                tabControl.add(tab1, text="Register a new System")

                labelTankID = ttk.Label(tab1, text="Tank ID (A unique integer from 1-1000 inclusive): ")
                labelTankID.grid(row=0, column=0, sticky=E)
                labelPetName = ttk.Label(tab1, text="Pet Name: ")
                labelPetName.grid(row=1, column=0, sticky=E)
                labelPetType = ttk.Label(tab1, text="Pet Type")
                labelPetType.grid(row=2, column=0, sticky=E)
                labelLocation = ttk.Label(tab1, text="Location of the tank: ")
                labelLocation.grid(row=3, column=0, sticky=E)

                entryID = ttk.Entry(tab1)
                entryID.grid(row=0, column=1)
                entryName = ttk.Entry(tab1)
                entryName.grid(row=1, column=1)
                entryType = ttk.Entry(tab1)
                entryType.grid(row=2, column=1)
                entryLocation = ttk.Entry(tab1)
                entryLocation.grid(row=3, column=1)

                submitButton = ttk.Button(tab1, text="Register new tank", command = partial(self.enterTankInfo, entryID, entryName, entryType, entryLocation))
                submitButton.grid(row=4, column=1)

                #SECOND TAB CONTENTS
                tab2 = ttk.Frame(tabControl)
                tabControl.add(tab2, text = "Records")
                
                labelRecords = ttk.Label(tab2, text="Enter the date and time of the records you would like")
                labelRecords.grid(row=3,column=0, sticky=W)
                labelYear = ttk.Label(tab2, text = "The year")
                labelYear.grid(row=4,column=0,sticky=W)
                labelMonth = ttk.Label(tab2, text = "The month")
                labelMonth.grid(row=5,column=0,sticky=W)
                labelDay = ttk.Label(tab2, text = "The day")
                labelDay.grid(row=6,column=0,sticky=W) 
                labelHour = ttk.Label(tab2, text = "The Hour")
                labelHour.grid(row=7,column=0,sticky=W)     
                labelMinute = ttk.Label(tab2, text = "The minute")
                labelMinute.grid(row=8,column=0,sticky=W)     
                
                entryYear = ttk.Entry(tab2)
                entryYear.grid(row=4,column=0)
                entryMonth = ttk.Entry(tab2)
                entryMonth.grid(row=5,column=0)  
                entryDay = ttk.Entry(tab2)
                entryDay.grid(row=6,column=0)      
                entryHour = ttk.Entry(tab2)
                entryHour.grid(row=7,column=0)   
                entryMinute = ttk.Entry(tab2)
                entryMinute.grid(row=8,column=0)                

                #THIRD TAB CONTENTS
                tab3 = ttk.Frame(tabControl)
                tabControl.add(tab3, text = "Current System Status")
                
                tabControl.pack(expan = 1, fill = "both")
                
                labelTemp = ttk.Label(tab3, text = "The current temperature is X degrees")
                labelTemp.grid(row = 0, column = 0, padx = 120)
                labelHumid = ttk.Label(tab3, text = "The current Humidity is X degrees")
                labelHumid.grid(row = 0, column = 1, padx = 120)
                labelMotion = ttk.Label(tab3, text="There is(n't) currently motion in the tank")
                labelMotion.grid(row=0, column=2, padx=120)
                labelIR = ttk.Label(tab3, text="There are(n't) currently IR readings in the tank")
                labelIR.grid(row=0, column=3, padx=120)

                frameTemp = ttk.Frame(tab3)
                frameTemp.grid(row=1, column=0)
                frameHumid = ttk.Frame(tab3)
                frameHumid.grid(row=1, column=1)
                frameMotion = ttk.Frame(tab3)
                frameMotion.grid(row=1, column=2)
                frameIR = ttk.Frame(tab3)
                frameIR.grid(row=1, column=3)
        
        def enterTankInfo(self, entryID, entryName, entryType, entryLocation):
                #addTank(int(entryID.get()), entryName.get(), entryLocation.get(), entryType.get())
                crs.execute('''INSERT or IGNORE INTO tanks VALUES(?, ?, ?, ?);''',(int(entryID.get()), entryName.get(), entryLocation.get(), entryType.get()))
                connection.commit()
                return        

root = Application()
root.mainloop()


#root = tk.Tk()
#root.geometry("1600x900+0+0") #set default size of GUI window
#root.title("Strawberri E-tank system interface")
#root.mainloop()

#self.hi_there = tk.Button(self)
#self.hi_there["text"] = "Hello World\n(click me)"
#self.hi_there["command"] = self.say_hi
#self.hi_there.pack(side="top")

#self.quit = tk.Button(self, text="QUIT", fg="red",
#command=self.master.destroy)
#self.quit.pack(side="bottom")
#tabControl = ttk.Notebook(root)
#tab1 = ttk.Frame(tabControl)
#tabControl.add(tab1, text = "Tab 1")
        
#tab2 = ttk.Frame(tabControl)
#tabControl.add(tab2, text = "Tab 2")
                

#def say_hi(self):
        #print("hi there, everyone!")

