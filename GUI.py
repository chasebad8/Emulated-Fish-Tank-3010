from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import tkinter.ttk as ttk
import sqlite3
from functools import partial
import socket, sys, time
import json
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from threading import Thread


class ReceiveMessage():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 1025
        self.server_address = ('localhost', self.port)
        self.s.bind(self.server_address)
        self.running = True
        self.values = {}

    def terminate(self):
        self.running = False

    def run(self):
        # do stuff
        while self.running:
            print("Hello world, threading is working")
            time.sleep(1)
            # print("Waiting to receive on local port %d" % port)
            # buf, address = s.recvfrom(port)
            # if not len(buf):
            #     break
            #
            # print("Received from %s %s: " % (address, buf))
            #
            # self.values = json.loads(buf)
            #
            # self.running = False


class Application(Tk):
    def __init__(self):
        # Initializations for the GUI
        super(Application, self).__init__()
        self.title("Strawberri E-tank system interface")
        self.minsize(800, 650)
        self.create_widgets()

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

        # SECOND TAB CONTENTS ------------------------------------------------------------------------------------------
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text="Records")

        # SUBMIT LABELS
        labelRecords = ttk.Label(tab2, text="Enter the date and time range of the records you would like as numbers")
        labelRecords.grid(row=3, column=0)
        labelTank = ttk.Label(tab2, text="The tank name")
        labelTank.grid(row=4, column=0)
        labelYear = ttk.Label(tab2, text="year to year")
        labelYear.grid(row=5, column=0)
        labelMonth = ttk.Label(tab2, text="month to month")
        labelMonth.grid(row=6, column=0)
        labelDay = ttk.Label(tab2, text="day to day")
        labelDay.grid(row=7, column=0)
        labelHour = ttk.Label(tab2, text="hour to Hour")
        labelHour.grid(row=8, column=0)
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
        # SUBMIT ENTRIES TWO
        entryTank2 = ttk.Entry(tab2)
        entryTank2.grid(row=4, column=1, sticky=W)
        entryYear2 = ttk.Entry(tab2)
        entryYear2.grid(row=5, column=1, sticky=W)
        entryMonth2 = ttk.Entry(tab2)
        entryMonth2.grid(row=6, column=1, sticky=W)
        entryDay2 = ttk.Entry(tab2)
        entryDay2.grid(row=7, column=1, sticky=W)
        entryHour2 = ttk.Entry(tab2)
        entryHour2.grid(row=8, column=1, sticky=W)

        # TEMPERATURE LABEL
        tempLabel = ttk.Label(tab2, text="Temperature")
        tempLabel.grid(row=0, column=0)
        # HUMIDTY LABEL
        humidLabel = ttk.Label(tab2, text="Humidity")
        humidLabel.grid(row=0, column=1)
        # MOTION LABEL
        motionLabel = ttk.Label(tab2, text="Motion")
        motionLabel.grid(row=0, column=2)
        # IR LABEL
        irLabel = ttk.Label(tab2, text="Motion")
        irLabel.grid(row=0, column=2)

        # GRAPH FRAMES
        # TEMP FRAME
        tempFrame = ttk.Frame(tab2, width=150, height=150)
        tempFrame.grid(row=1, column=0)
        # HUMID FRAME
        humidFrame = ttk.Frame(tab2, width=150, height=150)
        humidFrame.grid(row=1, column=1)
        # MOTION FRAME
        motionFrame = ttk.Frame(tab2, width=150, height=150)
        motionFrame.grid(row=1, column=2)
        # IR FRAME
        irFrame = ttk.Frame(tab2, width=150, height=150)
        irFrame.grid(row=1, column=3)

        # submitRecordsButton = ttk.Button(tab2, text="Submit", command=partial(self.fetchRecords, tab2))
        submitRecordsButton = ttk.Button(tab2, text="Submit",
                                         command=partial(self.drawTempGraph, tempFrame, [3,2,5,4,6,1,8,7],
                                                         [1, 2, 3, 4, 5, 6, 7, 8]))
        submitRecordsButton.grid(row=9, column=0)

        # THIRD TAB CONTENTS -------------------------------------------------------------------------------------------
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text="Current System Status")

        tabControl.pack(expan=1, fill="both")

        labelTemp = ttk.Label(tab3, text="The current temperature is X degrees")
        labelTemp.grid(row=0, column=0, padx=120)
        labelHumid = ttk.Label(tab3, text="The current Humidity is X degrees")
        labelHumid.grid(row=0, column=1, padx=120)
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
        host = 'localHost'
        textport = 1025

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = int(textport)
        server_address = (host, port)

        data = {"tank_id": int(entryID.get()), "name": entryName.get(), "location": entryLocation.get(),
                "petType": entryType.get(), "packetType": "tank"}

        sendIt = json.dumps(data)
        s.sendto(str(sendIt).encode('utf-8'), server_address)

        s.close()

    def fetchRecords(self, tab):
        # REQUEST FOR SENSOR VALS

        # start a thread for a udpReceiver which will wait for the sensor values to be sent
        udpReceive = ReceiveMessage()
        udpReceiveThread = Thread(target=udpReceive.run)
        udpReceiveThread.start()
        # while udpReceive.running:
        #     #do nothing
        # sensorRecords = udpReceive.values
        # udpReceive.terminate()
        #return sensorRecords

    def drawTempGraph(self, frame, xVals, yVals):
        # TEMPERATURE GRAPH
        tempGraph = Figure(figsize=(5, 5), dpi=75)
        tempPlot = tempGraph.add_subplot(111)
        tempPlot.plot(xVals, yVals)
        tempCanvas = FigureCanvasTkAgg(tempGraph, frame)
        tempCanvas.draw()
        tempCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def drawHumidGraph(self, frame, xVals, yVals):
        # HUMIDITY GRAPH
        humidGraph = Figure(figsize=(5, 5), dpi=75)
        humidPlot = humidGraph.add_subplot(111)
        humidPlot.plot(xVals, yVals)
        humidCanvas = FigureCanvasTkAgg(humidGraph, frame)
        humidCanvas.draw()
        humidCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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


root = Application()
root.mainloop()
