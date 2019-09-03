//initializing pins ofr the motor and switch
const int switchPin = 2; 
const int motorPin =  9; 

//variable for the state of the switch
int switchState = 0;  

void setup() {
  //initialize the motor as output and the switch as input
  pinMode(motorPin, OUTPUT);
  pinMode(switchPin, INPUT);
}

void loop() {
  //read the state of the switch
  switchState = digitalRead(switchPin);

  //If the switch is pressed:
  if (switchState == HIGH) {
    // turn on the motor
    digitalWrite(motorPin, HIGH);
    //otherwise:
  } else {
    // turn off the motor
    digitalWrite(motorPin, LOW);
  }
}
