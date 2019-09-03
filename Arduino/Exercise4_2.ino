#include <Servo.h>
//Above line includes a header file to use functions attributed to the servo motor

//this line initializes a Servo motor called "myServo"
Servo myServo;

//Declare variables for the angle of the sevo motor and the state of the button
int angle = 0;
int switchState = 0;

void setup() {

  //Set the pin of the servo motor to be pin 9 
  myServo.attach(9);

  //Set the button to be an input pin and set the servo motor to be at angle 0
  pinMode(8, INPUT);  
  myServo.write(0);
}

void loop() {

  //read the state of the button
  switchState = digitalRead(8);

  //if the button is pressed and the angle is zero:
  if (switchState == HIGH && angle == 0) {
    //set the servomotor to all angles 0-179 with 1 ms delays in between each movement
    for (int i=0; i <= 179; i++) {
      myServo.write(i);
      delay(1);
    }
    //set the new angle to be 179
    angle = 179;
    //if the button is pressed, but the motor is already at the 179 degrees, just wait a millisecond
  } else if (switchState == HIGH && angle == 179) {
    delay(1);
    //if the button is not pressed and the angle of the motor is 179 degrees, 
  }else if (switchState == LOW && angle == 179) {
    //set the servomotor backwards to all angles 179-0 with 1 ms delays in between each movement
    for (int i = 179; i >= 0; i--) {
      myServo.write(i);
      delay(1);
    }
    //set the new angle as 0 degrees;
    angle = 0;
  } else {
    //if the button is decompressed and the motor isalready at the 0 degree, wait a millisecond betore iterating
    delay(1);
  }

}

