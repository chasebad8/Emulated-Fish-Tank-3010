import serial
port = "/dev/ttyACM0"#put your port here
baudrate = 9600
ser = serial.Serial(port, baudrate) #initializing the serial connection

testTemp = 25 #set temp in Rpi2
tempTrue = "True" #reference for testing 

#This funtion encodes and sends to the arduino through the serial connection
def tell(msg): 
    msg = msg + '\n'
    x = msg.encode('ascii') # encode n send
    ser.write(x)

#This funtion retrieves from the arduino and encodes it to a string
def hear():
    msg = ser.read_until() # read until a new line
    mystring = msg.decode('ascii')  # decode n return 
    return mystring

#this function takes care of excess unwanted characters coming when retrieving strings from hear()
def encodeString(msg):
    i = len(msg) #takes length of string
    newString = ""
    for i in range (0, (i - 2)): #traverses and inserts characters into a new String excluding the last two chars (unwanted chars)
        newString = newString + msg[i]
    
    return newString #returns new string

#this loops so user can test as many times as needed or until they want to finish
while True:
    print("which test would you like to run?\n\n")
    print("(1) testSendTemp\n")
    print("(2) testRecieveTemp\n")
    print("(3) testTempisSame\n")
    print("(4) testCompareTemp\n\n")
    print("(0) Finish Testing\n\n")
    
    choice = input() #input variable for user requested test
    
    
    #This block tests testSendTemp from tempStub
    if choice == "1":
        print("Testing if the temperature was sent from the Arduino to Rpi2\n")
        
        tell(choice) #sends choice to tempStub so the arduino knows what test to run
        test = hear() #recieves from tempStub, the temp sent from arduino
        temp = int(test) #convert from a string to a int
        if temp == testTemp: #checks if the correct temp was sent from the arduino (25)
            print("Rpi recieved ",temp, " degrees celcius from the arduino\n")
            print ("[TEST SUCCESFUL]\n")
        else:
            print("[TEST FAILED]\n")
            
            
    #This block tests testRecieveTemp from tempStub      
    if choice == "2":
        print("Testing if the arduino recieved a temperature from Rpi2\n")
        
        tell("225") #225 is the choice and the temperature combined, 2 being the choice and 25 being the temp, must be done this way for proper sending and retrieval
        test = hear() #recieves back the value sent to the arduino. 25 if 25 and 0 if not meaning test has failed
        temp = int(test)
        if temp == testTemp: #checks if the correct temp was sent to the arduino
            print("Arduino recieved ",temp, " degrees celcius from Rpi2\n")
            print("[TEST SUCCESFUL]\n")
        else:
            print("[TEST FAILED]\n")
        
    
    #This block tests testTempisSame from tempStub
    if choice == "3":
        print("Testing if the Temperature found by the arduino is the same as the stored Temperature in Rpi2")
        
        tell("325") #325 is the choice and the temperature, 3 being the choice and 25 being the temp, must be done this way for proper sending and retrieval
        test = hear() #retrives results from tempStrub
        test = encodeString(test) #encodes retrival to be in proper form
        if test == tempTrue: #if true was retrieved the test passes, fails if not
            print("Both temperatures are the same, the heater dose not need to be activated\n")
            print("[TEST SUCCESFUL]\n")
        else:
            print("[TEST FAILED]\n")
            
            
    #This block tests testCompareTemp from tempStub
    if choice == "4":
        print("Testing if the Temperature found by the arduino is greater than, less then, or equal to the stored Temperature in Rpi2")
        
        tell("425") #425 is the choice and the temperature, 4 being the choice and 25 being the temp, must be done this way for proper sending and retrieval
        test = hear() #retrieves resuts from tempStub
        test = encodeString(test) #encodes retrival to be in proper form
        if test == "Greater" or test == "less":
            print("The temperature found by the Arduino is ",test, " then the temperture stored in Rpi2")
            print("[TEST SUCCESFUL]\n")
            
        elif test == "Equal":
            print("The temperature found by the Arduino is",test, " to the temperture stored in Rpi2\n")
            print("[TEST SUCCESFUL]\n")
        else:
            print("[TEST FAILED]\n")
            
            
    if choice == "0": #end testing
        break
    
    
            
            
    
            
    
            
    
            
            
            
            

    
    