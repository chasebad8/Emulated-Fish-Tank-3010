String tempStr = "25";

void setup() {
   Serial.begin(9600); // begin transmission
   pinMode(2, OUTPUT);
   digitalWrite(2, LOW);
}
void loop() {
  String val;
  while (Serial.available() > 0) {
    val = val + (char)Serial.read(); // read data byte by byte and store it
   
  }
  
  
 
  String choiceStr = val.substring(0,1);
  int choice = choiceStr.toInt();
  
  int tempRec = val.toInt() - 200;
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

void testSendTemp(){
  Serial.println(tempStr); 
}

void testRecieveTemp(int input){
  if(input == 25){
    Serial.println(tempStr);
  }
  else{
    Serial.println("0");
  }
}

void testTempisSame(int input){
  if(input == 25){
    Serial.println("True");
  }
  else{
    Serial.println("False");
  }
   
}

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
