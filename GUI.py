from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import tkinter.ttk as ttk
import sqlite3
from functools import partial
import socket, sys, time
import json
import requests

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from threading import Thread
import threading

sensorXValues = []  # used to store X values fetched from database
sensorYTempValues = []  # used to store Y values fetched from database
sensorYMotionValues = []  # used to store Y values fetched from database
pi1IP = ""
pi2IP = ""
#variables for drawing live graphs
xsTemp = []
ysTemp = []
#variables for live plotting
liveTempGraph = None
liveTempPlot = None
liveTempCanvas = None

#ports:
#1025 for GUI to Pi1
#1026 for pi1 to GUI
#1027 for GUI to pi2
#1029 for pi2 sending live updated values to GUI

class ReceiveMessage:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 1026
        self.server_address = ("", self.port)
        self.s.bind(self.server_address)
        self.running = True
        self.values = [[]]
        self.numToReceive = 0
        self.numReceived = 0
        self.done = threading.Event()

    def terminate(self):
        self.running = False

    def run(self):
        while self.running:
            print("RUNNNING")
            print("Waiting to receive on local port %d" % self.port)
            buf, address = self.s.recvfrom(self.port)
            if not len(buf):
                break

            print("Received from %s %s: " % (address, buf))
            self.numReceived += 1
            vals = json.loads(buf)
            self.values.append(vals) #IF A RECORD DOESNT EXIST, DOES ANYTHING GET RETURNED OVER UDP???
            sensorXValues.append(self.numReceived)
            sensorYTempValues.append(vals["fed"])
            sensorYMotionValues.append(vals["motion"])


            if self.numReceived == self.numToReceive:
                print("RECEIVED THE CORRECT AMOUNT")
                self.s.close()
                self.done.set()
                self.running = False

#Class used by threading to receive values for the live graph updates
class LiveValueFeed:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 1029
        self.server_address = ("", self.port)
        self.s.bind(self.server_address)
        self.running = True
        self.values = [[]]
        self.numToReceive = 0
        self.numReceived = 0
        self.done = threading.Event()

    def terminate(self):
        self.running = False

    def run(self):
        while self.running:
            print("Waiting to receive on local port %d" % self.port)
            buf, address = self.s.recvfrom(self.port)
            if not len(buf):
                break

            print("Received from %s %s: " % (address, buf))
            # self.numReceived += 1
            vals = json.loads(buf)
            #self.values.append(vals) #IF A RECORD DOESNT EXIST, DOES ANYTHING GET RETURNED OVER UDP???
            global xsTemp
            global ysTemp
            xsTemp.append(int(vals["timeRecorded"][14:16]))
            ysTemp.append(vals["temperature"])
            print("LIVE VALUE RECEIVED")
            global liveTempPlot

            liveTempPlot.clear()
            liveTempPlot.plot(xsTemp, ysTemp)
            #sensorYMotionValues.append(vals["motion"])

            if self.done.is_set():
                print("RECEIVED THE CORRECT AMOUNT")
                self.s.close()
                self.done.set()
                self.running = False

class Application(Tk):
    def __init__(self):
        # Initializations for the GUI
        super(Application, self).__init__()
        self.title("Strawberri E-tank system interface")
        self.minsize(800, 650)
        self.create_widgets()
        self.sensorValReceive = ReceiveMessage()
        # Thread for receiving sensor values through UDP, will be started and stopped in the appropriate functions
        self.sensorValReceiveThread = Thread(target=self.sensorValReceive.run)
        self.liveValueReceiver = LiveValueFeed()
        self.liveValueReceiverThread = Thread(target=self.liveValueReceiver.run)


    def create_widgets(self):
        tabControl = ttk.Notebook(self)  # creates tab structure

        # FIRST TAB CONTENTS
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

        submitButton = ttk.Button(tab1, text="Register new tank",
                                  command=partial(self.enterTankInfo, entryID, entryName, entryType, entryLocation))
        submitButton.grid(row=4, column=1)

        #Button to feed animal
        foodLabel = ttk.Label(tab1, text="Tank ID to give food to: ")
        foodLabel.grid(row=5,column=0)
        foodEntry = ttk.Entry(tab1)
        foodEntry.grid(row=5, column=1)
        dispenseFoodButton = ttk.Button(tab1, text="Dispense food",
                                  command=partial(self.dispenseFood, foodEntry))
        dispenseFoodButton.grid(row=6, column=1)
        #TTK for changing temperature
        temperatureLabel = ttk.Label(tab1, text="Enter new tank temperature here: ")
        temperatureLabel.grid(row=7, column=0)
        temperatureEntry = ttk.Entry(tab1)
        temperatureEntry.grid(row=7,column=1)
        temperatureNameLabel = ttk.Label(tab1, text="Enter tank ID here: ")
        temperatureNameLabel.grid(row=8, column=0)
        temperatureNameEntry = ttk.Entry(tab1)
        temperatureNameEntry.grid(row=8, column=1)
        temperatureButton = ttk.Button(tab1, text="Submit new temperature", command=partial(self.submitTemperature, temperatureEntry,temperatureNameEntry))
        temperatureButton.grid(row=9, column=1)

        # SECOND TAB CONTENTS ------------------------------------------------------------------------------------------
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text="Records")

        # SUBMIT LABELS
        labelRecords = ttk.Label(tab2, text="Enter the date and time range of the records you would like as numbers")
        labelRecords.grid(row=3, column=0)
        labelTank = ttk.Label(tab2, text="The tank name")
        labelTank.grid(row=4, column=0)
        labelYear = ttk.Label(tab2, text="Year")
        labelYear.grid(row=5, column=0)
        labelMonth = ttk.Label(tab2, text="Month")
        labelMonth.grid(row=6, column=0)
        labelDay = ttk.Label(tab2, text="Day")
        labelDay.grid(row=7, column=0)
        labelHour = ttk.Label(tab2, text="Hour")
        labelHour.grid(row=8, column=0)
        labelMinute = ttk.Label(tab2, text="Minute to Minute")
        labelMinute.grid(row=9, column=0)
        # SUBMIT ENTRIES
        entryTank = ttk.Entry(tab2)
        entryTank.grid(row=4, column=0, sticky=W)
        entryYear = ttk.Entry(tab2)
        entryYear.grid(row=5, column=0, sticky=W)
        entryMonth = ttk.Entry(tab2)
        entryMonth.grid(row=6, column=0, sticky=W)
        entryDay = ttk.Entry(tab2)
        entryDay.grid(row=7, column=0, sticky=W)
        entryHour = ttk.Entry(tab2)
        entryHour.grid(row=8, column=0, sticky=W)
        minuteEntry = ttk.Entry(tab2)
        minuteEntry.grid(row=9, column=0, sticky=W)
        minuteEntry.insert(0, "14")
        # SUBMIT ENTRIES TWO
        minuteEntry2 = ttk.Entry(tab2)
        minuteEntry2.grid(row=9, column=1, sticky=W)
        minuteEntry2.insert(0, "24")


        # TEMPERATURE LABEL
        tempLabel = ttk.Label(tab2, text="Feeding history")
        tempLabel.grid(row=0, column=0)
        # HUMIDTY LABEL
        #humidLabel = ttk.Label(tab2, text="Humidity")
        #humidLabel.grid(row=0, column=1)
        # MOTION LABEL
        motionLabel = ttk.Label(tab2, text="Motion")
        motionLabel.grid(row=0, column=1)
        # IR LABEL
        irLabel = ttk.Label(tab2, text="Motion")
        irLabel.grid(row=0, column=2)

        # GRAPH FRAMES
        # TEMP FRAME
        tempFrame = ttk.Frame(tab2, width=150, height=150)
        tempFrame.grid(row=1, column=0)
        # HUMID FRAME
        #humidFrame = ttk.Frame(tab2, width=150, height=150)
        #humidFrame.grid(row=1, column=1)
        # MOTION FRAME
        motionFrame = ttk.Frame(tab2, width=150, height=150)
        motionFrame.grid(row=1, column=1)
        # IR FRAME
        irFrame = ttk.Frame(tab2, width=150, height=150)
        irFrame.grid(row=1, column=3)

        # submitRecordsButton = ttk.Button(tab2, text="Submit", command=partial(self.fetchRecords, tab2))
        submitRecordsButton = ttk.Button(tab2, text="Get Records",
                                         command=partial(self.fetchRecords,entryTank,entryYear,entryMonth,
                                                         entryDay,entryHour,minuteEntry,minuteEntry2))
        submitRecordsButton.grid(row=10, column=0)
        #Button to check if records have been obtained an draw graphs if they have been
        drawGraphsButton = ttk.Button(tab2, text="Draw Graphs",
                                         command=partial(self.drawRecordGraphs, tempFrame, motionFrame))
        drawGraphsButton.grid(row=10, column=1)

        # THIRD TAB CONTENTS -------------------------------------------------------------------------------------------
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text="Current System Status")

        tabControl.pack(expan=1, fill="both")

        labelTemp = ttk.Label(tab3, text="The current fed status of the tank")
        labelTemp.grid(row=0, column=0, padx=120)
        # labelHumid = ttk.Label(tab3, text="The current Humidity is X degrees")
        # labelHumid.grid(row=0, column=1, padx=120)
        labelMotion = ttk.Label(tab3, text="The current motion in the tank")
        labelMotion.grid(row=0, column=1, padx=120)
        # labelIR = ttk.Label(tab3, text="There are(n't) currently IR readings in the tank")
        # labelIR.grid(row=0, column=3, padx=120)


        frameTemp = ttk.Frame(tab3)
        frameTemp.grid(row=1, column=0)
        # frameHumid = ttk.Frame(tab3)
        # frameHumid.grid(row=1, column=1)
        frameMotion = ttk.Frame(tab3)
        frameMotion.grid(row=1, column=1)
        # frameIR = ttk.Frame(tab3)
        # frameIR.grid(row=1, column=3)

        labelTankIDLive = ttk.Label(tab3, text="Tank ID: ")
        labelTankIDLive.grid(row=2, column=0, sticky=E)
        entryTankIDLive = ttk.Entry(tab3)
        entryTankIDLive.grid(row=2, column=1, sticky=W)
        startLiveFeedButton = ttk.Button(tab3, text="Start Live Feed", command=partial(self.startLiveFeed))
        startLiveFeedButton.grid(row=3, column=1)

        # TEMPERATURE GRAPH
        global liveTempGraph
        global liveTempPlot
        global liveTempCanvas
        liveTempGraph = Figure(figsize=(5, 5), dpi=75)
        liveTempPlot = liveTempGraph.add_subplot(111)
        liveTempPlot.plot([1,2,3], [1,2,3])
        liveTempCanvas = FigureCanvasTkAgg(liveTempGraph, frameTemp)
        liveTempCanvas.draw()
        liveTempCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ani = animation.FuncAnimation(liveTempGraph, self.animate, fargs=(xsTemp, ysTemp, ax), interval=100)
        # plt.show()
        #liveTempPlot.show()

        #TEST TAB CONTENTS --------------------------------------------------------------------------------------------
        testTab = ttk.Frame(tabControl)
        tabControl.add(testTab, text="TESTING")
        graphFrame1 = ttk.Frame(testTab)
        graphFrame1.grid(row=0,column=1)
        graphFrame2 = ttk.Frame(testTab)
        graphFrame2.grid(row=0, column=2)
        graphFrame3 = ttk.Frame(testTab)
        graphFrame3.grid(row=0, column=3)

        testGraphButton = ttk.Button(testTab, text="testGraphs",
                                     command=partial(self.testGraphs,graphFrame1,[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],graphFrame2,
                                                     [-1,-2,-3,-4,-5,-6,-7,-8],[1,2,3,4,5,6,7,8],graphFrame3,[1,2,3,4,5,6,7,8],[1,2,3,4]))
        testGraphButton.grid(row=0, column=0)
        testThreadingButton = ttk.Button(testTab, text="testThreading",command=self.testThreading)
        testThreadingButton.grid(row=1, column=0)

        testtempControlButton = ttk.Button(testTab, text="testTemperatureControl", command=partial(self.testTemperatureControl,20,21,19,21,25,21))
        testtempControlButton.grid(row=4, column=0)

    # function to send info of a newly registered tank
    def enterTankInfo(self, entryID, entryName, entryType, entryLocation):
        # IP of pi1
        host = "169.254.164.162"
        textport = 1025

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = int(textport)
        server_address = (host, port)

        data = {"tank_id": int(entryID.get()), "name": entryName.get(), "location": entryLocation.get(),
                "petType": entryType.get(), "packetType": "tank"}

        sendIt = json.dumps(data)
        s.sendto(str(sendIt).encode('utf-8'), server_address)

        s.close()

    # sends a command in the form of a json to tell the arduino to dispense food
    def dispenseFood(self, foodNameEntry):
        #IP of pi2
        host = "169.254.164.162"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = 1027
        server_address = (host, port)
        try:
            print("Feeding now")
            toSend = {"tank_id": int(foodNameEntry.get()), "targetTemp": 0, "fed": 1, "packetType" : "arduinoVal"}
            s.sendto(str(json.dumps(toSend)).encode('utf-8'), server_address)
            s.close()
        except:
            print("There was an error dispensing the food to tank "+foodNameEntry.get()+", please try again")

    # sends a command in the form of json to update the tank's current temperature
    def submitTemperature(self, tempEntry, tempNameEntry):
        temp = 1

        temperature = 0;
        try:
            temperature = int(tempEntry.get())
        except ValueError:
            temp = 0

        if temp == 0:
            api_key = "dce44afe0bc4170f14315300461e90fb"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + api_key + "&q=" + tempEntry.get()
            response = requests.get(complete_url)
            x = response.json()
            try:
                y=x["main"]
                curr_temp = y["temp"]
                if x["cod"] != "404":
                    temperature = curr_temp - 273.15
                    print(curr_temp)
            except:
                print("Please enter a different location")


        #print("This will change the tank temp to: "+tempEntry.get()+" when working, to tank: "+tempNameEntry.get())
        # IP of pi2
        host = "169.254.164.162"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = 1027
        server_address = (host, port)
        try:
            print("send json of new tank temperature")
            toSend = {"tank_id": int(tempNameEntry.get()), "targetTemp": temperature, "fed": 0, "packetType": "arduinoVal"}
            s.sendto(str(json.dumps(toSend)).encode('utf-8'), server_address)
            s.close()
        except:
            print("There was an error in sending the new temperature for tank "+tempNameEntry.get()+", please try again")

    #This function obtains the records of sensor values for a given time interval. it does this by first starting a thread
    #which will wait to receive udp packets. Once this thread is started the function sends requests as json through udp
    #to the main database, where the records are obtained from if they exist
    def fetchRecords(self, tank, year, month, day, hour, minute1, minute2):
        # REQUEST FOR SENSOR VALS
        # self.sensorValReceive = ReceiveMessage()
        self.sensorValReceiveThread = Thread(target=self.sensorValReceive.run)
        self.sensorValReceiveThread.start()
        self.sensorValReceive.numReceived = 0
        self.sensorValReceive.running = True
        if self.sensorValReceive.running:
            # first clear the existing values stored
            del sensorXValues[:]
            del sensorYTempValues[:]
            del sensorYMotionValues[:]
            #INIIALIZE UDP
            host = "169.254.164.162"
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            port = 1025
            server_address = (host, port)

            # the number of entries (x values) to be expected based on the range of time given
            numToReceive = int(minute2.get()) - int(minute1.get())
            # self.sensorValReceive = ReceiveMessage()
            self.sensorValReceive.numToReceive = (numToReceive*2)
            # self.sensorValReceiveThread = Thread(target=self.sensorValReceive.run)
            # self.sensorValReceiveThread.start()

            for x in range(int(minute1.get()), int(minute2.get())):
                if x<10:
                    time = year.get() + "-" + month.get() + "-" + day.get() + " " + hour.get() + ":" + "0" + str(x)
                else:
                    time = year.get() + "-" + month.get() + "-" + day.get() + " " + hour.get() + ":" + str(x)
                print(time)
                toSend = {"packetType" : "requestSensVal", "timeRequested" : time}
                try:
                    s.sendto(str(json.dumps(toSend)).encode('utf-8'), server_address)
                    print("sending request for values...")
                    #s.close()
                except:
                    print("There was an error sending the request for sensor values at time: " + time)

        else:
            print("The sensor records are already in the process of being fetched")

    #this function is used to draw the graphs of the sensor value records once they have been obtained from the database
    def drawRecordGraphs(self, tempFrame, motionFrame):
        #MIGHT NEED TO CHANGE, CURRENTLY IF WE DONT HAVE CORRECT # OF RECORDS, IT WONT DRAW
        #terminate thread
        #self.sensorValReceive.terminate()
        self.sensorValReceive.running = False
        if len(sensorXValues) == len(sensorYTempValues):
            self.drawTempGraph(tempFrame, sensorXValues, sensorYTempValues)
            self.drawTempGraph(motionFrame, sensorXValues, sensorYMotionValues)
            print("There were "+str(len(sensorXValues))+" records found")
        else:
            print("There was an error in the sensor data and the graphs could not be printed")

    #Arguements:
    #frame: The frame where the graph should be drawn
    #xVals: The values to be used during plotting for the x axis
    #yVals: The values to be used during plotting for the y axis
    #this function draws a graph using matplotlib. If the xVals and yVals are not the same length the graph cnanot be drawn
    def drawTempGraph(self, frame, xVals, yVals):
        try:
            #TEMPERATURE GRAPH
            tempGraph = Figure(figsize=(5, 5), dpi=75)
            tempPlot = tempGraph.add_subplot(111)
            tempPlot.plot(xVals, yVals)
            tempCanvas = FigureCanvasTkAgg(tempGraph, frame)
            tempCanvas.draw()
            tempCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        except:
            print("An error occurred and the graph with x and y values of", xVals,"and", yVals, "could not be printed")

    def drawHumidGraph(self, plot, xVals, yVals):
        # HUMIDITY GRAPH
        # humidGraph = Figure(figsize=(5, 5), dpi=75)
        # humidPlot = humidGraph.add_subplot(111)
        plot.clear()
        plot.plot(xVals, yVals)
        # humidCanvas = FigureCanvasTkAgg(humidGraph, frame)
        # humidCanvas.draw()
        # humidCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def drawMotionGraph(self, tab, xVals, yVals):
        # MOTION GRAPH
        motionGraph = Figure(figsize=(5, 5), dpi=75)
        motionPlot = motionGraph.add_subplot(111)
        motionPlot.plot(xVals, yVals)
        motionCanvas = FigureCanvasTkAgg(motionGraph, motionFrame)
        motionCanvas.draw()
        motionCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def drawIRGraph(self, tab, xVals, yVals):
        # IR GRAPH
        irGraph = Figure(figsize=(5, 5), dpi=75)
        irPlot = irGraph.add_subplot(111)
        irPlot.plot(xVals, yVals)
        irCanvas = FigureCanvasTkAgg(irGraph, irFrame)
        irCanvas.draw()
        irCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    #determine if the current temperature of tank is within acceptable range (+-1 of targetTemp)
    def temperatureControl(self, currTemp, targetTemp):
        if ((currTemp > targetTemp+1) or (currTemp < targetTemp-1)):
            return 0#failed check
        else:
            return 1#within range, check passed

    # this function is used by matplotlib to animate the plot in real time
    def animate(self, i, xs, ys, myPlot):
        myPlot.clear()
        myPlot.plot(xs, ys)


    #this function is used to start a thread to wait to receive values forwarded by the main database which will be used
    #as a live feed to update the graphs
    def startLiveFeed(self):
        if not self.sensorValReceiveThread.isAlive():
            print("go")
            self.liveValueReceiverThread = Thread(target=self.liveValueReceiver.run)
            self.liveValueReceiverThread.start()
        else:
            print("The thread to receive live values is already running")




    #TESTING FUNCTIONS --------------------------------------------------------------------
    def testGraphs(self, frame1, xVals1, yVals1, frame2, xVals2, yVals2, frame3, xVals3, yVals3):
        self.drawTempGraph(frame1, ['2019-11-30 16:10', '2019-11-30 16:11', '2019-11-30 16:12'], [30,35,37])
        #self.drawTempGraph(frame2, xVals2, yVals2)
        #self.drawTempGraph(frame3, xVals3, yVals3)

    def testThreading(self):
        udpReceive = ReceiveMessage()
        udpReceiveThread = Thread(target=udpReceive.run)
        udpReceiveThread.start()
        for x in range(0,10):
            print("Message from main thread")
            time.sleep(1.5)
        udpReceive.terminate()

    def testTemperatureControl(self, currTemp1, targetTemp1, currTemp2, targetTemp2, currTemp3, targetTemp3):
        result = self.temperatureControl(currTemp1, targetTemp1)
        if result==1:
            print("The current temperature ", currTemp1, " is within the acceptable range")
        else:
            print("The current temperature ", currTemp1, " is not within the acceptable range")
        result2 = self.temperatureControl(currTemp2, targetTemp2)
        if result2 == 1:
            print("The current temperature ", currTemp2, " is within the acceptable range")
        else:
            print("The current temperature ", currTemp2, " is not within the acceptable range")
        result3 = self.temperatureControl(currTemp3, targetTemp3)
        if result2 == 1:
            print("The current temperature ", currTemp3, " is within the acceptable range")
        else:
            print("The current temperature ", currTemp3, " is not within the acceptable range")

def drawLiveGraphs(self, xs, ys, myPlot):
    myPlot.clear()
    myPlot.plot(xs, ys)

root = Application()
root.mainloop()
