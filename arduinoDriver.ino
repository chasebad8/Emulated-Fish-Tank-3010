#include "dht.h"

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

//defining the pin for the Relay module
int relay = 12;

//Defining the time between sending information
const int time0 = 30000;
long interrupt;

//Defining pin to RBG color for heater simulation
int coolBlue = 10;
int sameGreen = 11;
int heatRed = 12;


void setup() {
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

void loop() {
  runIr();
  recieveValues();
  heater();
  
  if (millis() - interrupt > time0){
    motion =(String) motionCount;
    sendValues();
    fed = "0";
    motionCount = 0;
  }
}

void sendValues(){
  getTemp();
  
  Serial.println(tank);
  Serial.println(motion);
  Serial.println(temp);
  Serial.println((String) targTemp);
  Serial.println(fed);
  interrupt = millis();
}

void runMotor(void){
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

void resetMotor(void){
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

void getTemp(void){
  int temperature = DHT.read11(DHT11_PIN);
  temp = (String) DHT.temperature;
  tempInt =(int) DHT.temperature;
  delay(500);
}

void runIr(void){
  sensorVal = digitalRead(sensor);

  if(sensorVal == HIGH){
    motionCount++;
    delay(500);
  }
  else{
    delay(800);
  }
}

void heater(void){
  if (targTemp > tempInt){
    digitalWrite(heatRed, HIGH);
    digitalWrite(coolBlue, LOW);
    digitalWrite(sameGreen, LOW);
  }
  else if (targTemp < tempInt){
    digitalWrite(heatRed, LOW);
    digitalWrite(coolBlue, HIGH);
    digitalWrite(sameGreen, LOW);
  }
  else{
    digitalWrite(heatRed, LOW);
    digitalWrite(coolBlue, LOW);
    digitalWrite(sameGreen, HIGH);
  }
}

void recieveValues(void){
  String val;
  while (Serial.available() > 0) {
    val = val + (char)Serial.read(); // read data byte by byte and store it
  }

  String motorStr = val.substring(0,1);
  motor = motorStr.toInt();
  int targTempFake = val.toInt() - (motor * 100);
  
  if (targTempFake > 0){
    targTemp = targTempFake;
  }

  if(motor == 1){
    for (int i = 0; i < 1000; i++){
      runMotor();
    }
    fed = "1";
    motor = 0;
    motorCount++;

    if(motorCount == 4){
      for (int i = 0; i < 5000; i++){
      resetMotor();
      motorCount = 0;
      }
    }
  }
}
