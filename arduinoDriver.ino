//Chase Fridgen 101077379
//SYSC 3010
//Driver to be flashed onto the arduino for animal enclosure functionality

#include "dht.h"

//defining static variables
static String tank = "0";
static String motion;
static String temp;
static int tempInt;
static int targTemp;
static String fed = "0";
static int motionCount = 0;
static int motor = 0;
static int motorCount = 0;
static int motorResetCount = 0;


//defining the pins and variables for the motor componant
int bluePin = 2;
int pinkPin = 3;
int yellowPin = 4;
int orangePin = 5;
int currStep = 0; // for counting the steps of the motor
int resetStep = 0;

//defining pins variables for the temperature sensor
dht DHT;
#define DHT11_PIN 7

//defining the pin and variable numbers for the IR sensor
int sensor = 8;
int sensorVal = 0;

//Defining the time between sending information
const int time0 = 30000;
long interrupt;

//Defining pin to RBG color for heater simulation
int coolBlue = 10;
int sameGreen = 11;
int heatRed = 12;

// setup() is where all the pins are initialized as input or outputs and given
// their initial values.
void setup() 
{
  Serial.begin(9600); // begin transmission
  
  //Initialize pins at the ports as outputs for the motor 
  pinMode(bluePin, OUTPUT);
  pinMode(pinkPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(orangePin, OUTPUT);
  //Initialize all the motors steps to 0
  digitalWrite(bluePin, LOW);
  digitalWrite(pinkPin, LOW);
  digitalWrite(yellowPin, LOW);
  digitalWrite(orangePin, LOW);

  //Initializing the IR sensor
  pinMode(sensor, INPUT); //setting the sensor as an input

  //Initializing RBG Led for heater simulation
  pinMode(coolBlue, OUTPUT);
  pinMode(sameGreen, OUTPUT);
  pinMode(heatRed, OUTPUT);
  digitalWrite(coolBlue, LOW);
  digitalWrite(sameGreen, HIGH);
  digitalWrite(heatRed, LOW);

  getTemp();
  targTemp = 25;
}

// loop() is the main funtion in the arduino driver as it is constantly looping and
//reeading-in/sending the sensor values
void loop() 
{
  runIr(); // constantly running PIR
  recieveValues(); // constanlty waiting to recieve from RPI's
  heater(); // constantly compariong values for heater
  
  if (millis() - interrupt > time0){ // every 30 seconds this if statements sends the sensor values through UART
    motion =(String) motionCount;
    sendValues();
    fed = "0";
    motionCount = 0;
  }
}

// sendValues() sends all the values to the RPI' through UART
void sendValues() 
{
  getTemp();
  
  Serial.println(tank);
  Serial.println(motion);
  Serial.println(temp);
  Serial.println((String) targTemp);
  Serial.println(fed);
  interrupt = millis();
}

// runMotor() actiavtes the stepper motor in a clockwise direction
void runMotor(void)
{
   if(currStep == 0){
    digitalWrite(bluePin, HIGH);
    digitalWrite(pinkPin, LOW);
    digitalWrite(yellowPin, LOW);
    digitalWrite(orangePin, LOW);
    currStep++;
  }
  else if(currStep == 1){
    digitalWrite(bluePin, LOW);
    digitalWrite(pinkPin, HIGH);
    digitalWrite(yellowPin, LOW);
    digitalWrite(orangePin, LOW);
    currStep++;
  }
  else if(currStep == 2){
    digitalWrite(bluePin, LOW);
    digitalWrite(pinkPin, LOW);
    digitalWrite(yellowPin, HIGH);
    digitalWrite(orangePin, LOW);
    currStep++;
  }
  else {
    digitalWrite(bluePin, LOW);
    digitalWrite(pinkPin, LOW);
    digitalWrite(yellowPin, LOW);
    digitalWrite(orangePin, HIGH);
    currStep = 0;
  }
  delay(4);
}

// resetMotor() actiavtes the stepper motor in a counter-clockwise direction
// therefore reseting it 
void resetMotor(void)
{
   if(resetStep == 0){
    digitalWrite(bluePin, LOW);
    digitalWrite(pinkPin, LOW);
    digitalWrite(yellowPin, LOW);
    digitalWrite(orangePin, HIGH);
    resetStep++;
  }
  else if(resetStep == 1){
    digitalWrite(bluePin, LOW);
    digitalWrite(pinkPin, LOW);
    digitalWrite(yellowPin, HIGH);
    digitalWrite(orangePin, LOW);
    resetStep++;
  }
  else if(resetStep == 2){
    digitalWrite(bluePin, LOW);
    digitalWrite(pinkPin, HIGH);
    digitalWrite(yellowPin, LOW);
    digitalWrite(orangePin, LOW);
    resetStep++;
  }
  else {
    digitalWrite(bluePin, HIGH);
    digitalWrite(pinkPin, LOW);
    digitalWrite(yellowPin, LOW);
    digitalWrite(orangePin, LOW);
    resetStep = 0;
  }
  delay(4);
}

// getTemp() reads the temerature in from the DHT11
// Temperature sensor
void getTemp(void)
{
  int temperature = DHT.read11(DHT11_PIN);
  temp = (String) DHT.temperature;
  tempInt =(int) DHT.temperature;
  delay(500);
}

// runIr() is the funtion for the PIR sensor,
// it increments 1 every time motion is detected
void runIr(void){
  sensorVal = digitalRead(sensor);

  if(sensorVal == HIGH){ // motion is detected
    motionCount++; // count up
    delay(500);
  }
  else{
    delay(800);
  }
}

// heater() is the funtion that simulates what a heater
// would do to the enclosure with an RBG LED light
void heater(void)
{
  if (targTemp > tempInt){       // if the target temp is higher than the real temp
    digitalWrite(heatRed, HIGH); //set to heat (RED)
    digitalWrite(coolBlue, LOW);
    digitalWrite(sameGreen, LOW);
  }
  else if (targTemp < tempInt){ // if the target temp is less than the real temp
    digitalWrite(heatRed, LOW); //set to cool (BLUE)
    digitalWrite(coolBlue, HIGH);
    digitalWrite(sameGreen, LOW);
  }
  else{
    digitalWrite(heatRed, LOW); // if the target temp and real temp are the same
    digitalWrite(coolBlue, LOW);// keep the same (GREEN)
    digitalWrite(sameGreen, HIGH);
  }
}

// receieveValues() is the funtion that recieves input from the RPI's
// through UART connection. it then takes in the values and breaks them into
// the proper componants and runs motor or changes the target temp of the
// system
void recieveValues(void)
{
  String val;
  while (Serial.available() > 0) { 
    val = val + (char)Serial.read(); // read data byte by byte and store it
  }

  String motorStr = val.substring(0,1);
  motor = motorStr.toInt();// geting the portion sent indicating whether the motor should run or not
  int targTempFake = val.toInt() - (motor * 100); // Getting the portion sent indicating the target temperature
  
  if (targTempFake > 0){ // ensureing the sent target temp is above 0 degrees (for safety reasons)
    targTemp = targTempFake;
  }

  if(motor == 1){ // if user sent a 1 the motor will run for 5 seconds
    for (int i = 0; i < 1000; i++){
      runMotor();
    }
    fed = "1"; // fed gets set to 1
    motor = 0;
    motorCount++;

    if(motorCount == 4){ // after being fed 4 times the motor resets back to original feediung state
      for (int i = 0; i < 5000; i++){
      resetMotor();
      motorCount = 0;
      }
    }
  }
}
