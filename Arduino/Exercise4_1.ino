#include <Servo.h>
//Above line includes a header file to use functions attributed to the servo motor

//this line initializes a Servo motor called "myServo"
Servo myServo;

//Declare variables for the pin of the potentiometer (the pot), the pot's voltage value, 
//and the angle that the potentiometer has been turned. Also sets the pin of the pot to be A0
const int potPin = A0;
int potValue;
int angle;

void setup() {

  //Set the pin of the servo motor to be pin 9 
  myServo.attach(9);

  //Set the serial port up for monitoring
  Serial.begin(9600);
}

void loop() {
  //Read the voltage value of the pot and store it in potValue. Then print the stored value
  potValue = analogRead(potPin);
  Serial.print("Potentiometer reading: \t");
  Serial.print(potValue);

  //Map the available values of the pot to angles that could be attributed to these values. Print the angle
  //that will be used for the servo motor
  angle = map(potValue, 0, 1023, 0, 179);
  Serial.print("\t Angle: \t");
  Serial.print(angle);

  //set the servo motor's pin to the above calculated angle
  myServo.write(angle);

  //wait 15ms and then repeat the loop
  delay(15);

}
