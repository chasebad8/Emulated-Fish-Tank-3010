// Chase Fridgen 
// SYSC 3310
// hardware stub for the Temperature sensor

String tempStr = "25"; // temperature to me compared with

// setup() initializes all pins and the serial UART connection with the RPI's
void setup() {
   Serial.begin(9600); // begin transmission
   pinMode(2, OUTPUT);
   digitalWrite(2, LOW);
}

// loop() constantly polls for a users input to decide what the
// desired funtion to run is and the temp to be compared with
void loop() {
  String val;
  while (Serial.available() > 0) { // reding in values
    val = val + (char)Serial.read(); // read data byte by byte and store it
   
  }
  
  
 
  String choiceStr = val.substring(0,1);
  int choice = choiceStr.toInt(); //first character in sent string is funtion choice
  
  int tempRec = val.toInt() - 200; // second character in sent string is temp
  int tempSame = val.toInt() - 300;
  int tempCompare = val.toInt() - 400;
 
  
  if(choice == 1){
    testSendTemp(); 
  }
  if(choice == 2){
    testRecieveTemp(tempRec);
  }
  if(choice == 3){
    testTempisSame(tempSame); 
  }
  if(choice == 4){
    testCompareTemp(tempCompare);
  }
  delay(1000);
}

// tests if the arduino can send a temperature through UART to the RPI
void testSendTemp(){
  Serial.println(tempStr); 
}

// tests if the arduino can recdieve a value from the RPI through UART
void testRecieveTemp(int input){
  if(input == 25){
    Serial.println(tempStr);
  }
  else{
    Serial.println("0");
  }
}

// tests if the recieved temp is the same and the stored temp in the arduino
void testTempisSame(int input){
  if(input == 25){
    Serial.println("True");
  }
  else{
    Serial.println("False");
  }
   
}

// compares recived temp to see if is greater, equal to, or less than
// stored temperature
void testCompareTemp(int input){
  if(input > 25){
    Serial.println("Greater");
  }
  else if(input < 25){
    Serial.println("Less");
  }
  else{
    Serial.println("Equal");
  }
}
