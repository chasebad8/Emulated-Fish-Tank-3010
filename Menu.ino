// Chase Fridgen 101077379
// SYSC 3310
// Menu for all functions coming from the arduino system

#include "dht.h"


//defining the pins for the motor
int bluePin = 2;
int pinkPin = 3;
int yellowPin = 4;
int orangePin = 5;

//defining variables for the temperature sensor
dht DHT;
#define DHT11_PIN 7

//defining the pin number for the IR sensor
int sensor = 8;
int sensorVal = 0;

int currStep = 0; // for counting the steps of the motor
int resetStep = 0;
const int time0 = 10000; // defie the time to be 3 seconds
static char menuOption = 0;
long interrupt;
//boolean reset = false;

int stepCount = 0;

// setup() is where all the pins are initialized as input or outputs and given
// their initial values.
void setup() {
    Serial.begin(9600);
    while (!Serial) ; 
    Serial.println("start");

    //Initialize thes pins at the ports as outputs
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


   menuOption = menu();
}

// loop() is the main funtion in the menu as it takes in the input from the 
// serial monitor (1-4) and runs the desired suntion based on that
void loop() {
  if (menuOption == '1'){
    runMotor();
  }  

  else if (menuOption == '2'){
    resetMotor();
  }
  else if (menuOption == '3'){
    getTemp();
  }
  else if (menuOption == '4'){
    runIr();
  }

  if (millis() - interrupt > time0)
    {
      if (menuOption == '4'){
        Serial.print("The animal moved ");
        Serial.print(stepCount);
        Serial.println(" times in the last 10 seconds ");
        stepCount = 0;
        menuOption = menu();
      }
      else{
        menuOption = menu();
      }
    }

  
}

// runMotor() actiavtes the stepper motor in a clockwise direction
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

// resetMotor() actiavtes the stepper motor in a counter-clockwise direction
// therefore reseting it
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

// getTemp() reads the temerature in from the DHT11
// Temperature sensor
void getTemp(void){
  int temp = DHT.read11(DHT11_PIN);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  delay(5000);
}

// runIr() is the funtion for the PIR sensor,
// it increments 1 every time motion is detected
void runIr(void){
  sensorVal = digitalRead(sensor);

  if(sensorVal == HIGH){
    Serial.println("Motion Detected");
    stepCount++;
    delay(500);
  }
  else{
    Serial.println("0");
    delay(800);
  }
  
  
}

// menu() is the interface that promptes the user for an input on the serial
// monitor and waits for the input, then changes the menuoption for the desired
// funtion depending on said input
char menu()
{

    Serial.println(F("\nWhich component would you like to test?"));
    Serial.println(F("(1) Run Motor"));
    Serial.println(F("(2) Reset Motor"));
    Serial.println(F("(3) Get Temperature"));
    Serial.println(F("(4) Run PIR Sensor \n"));
    while (!Serial.available());

    // Read data from serial monitor if received
    while (Serial.available()) 
    {
        char c = Serial.read();
        if (isAlphaNumeric(c)) 
        {   
            
            if(c == '1') {
              Serial.println(F("Now Running motor for 10 seconds"));
            }
            else if(c == '2'){
              Serial.println(F("The motor is returning to its original position"));
            }
            else if(c == '3'){
              Serial.println(F("The temperature is being read"));
            }
            else if(c == '4'){
              Serial.println(F("Motion is being detected"));
            }
            else
            {
                Serial.println(F("illegal input!"));
                return 0;
            }
            interrupt = millis();
            return c;
        }
    }
}
