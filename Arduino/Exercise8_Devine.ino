// named constant for the switch pin
const int switchPin = 8;

 // store the last time an LED was updated
unsigned long previousTime = 0;
// the current switch state
int switchState = 0; 
// the previous switch state
int prevSwitchState = 0; 
 // a variable to refer to the LEDs
int led = 2;
// interval at which to light the next LED
long interval = 600000; 

void setup() {
  // set the LED pins as outputs
  for (int x = 2; x < 8; x++) {
    pinMode(x, OUTPUT);
  }
  // set the tilt switch pin as input
  pinMode(switchPin, INPUT);
}

void loop() {
  // store the time since the Arduino started running
  unsigned long currentTime = millis();

  // compare the current time to the previous time an LED turned on, if the difference is larger than the interval
  if (currentTime - previousTime > interval) {
    // save the current time as the last time you changed an LED
    previousTime = currentTime;
    // Turn the LED on
    digitalWrite(led, HIGH);
    // increment the led
    led++;

    //when the last LED has been on and the interval passes, turn off all LEDs except for #2
    if (led == 9) {
        for (int x = 3; x < 8; x++) {
          digitalWrite(x, LOW);
        }
        //"start" the process all over again with the second LED already lit (I didnt think that
        //it was necessary to turn off the first LED since there are supposed to be at least 6 incorporated and
        //there woul dbe no need for the 6th otherwise
        led = 3;
      }
    }

  // read the switch value
  switchState = digitalRead(switchPin);

  // if the switch has changed
  if (switchState != prevSwitchState) {
    // turn all the LEDs low
    for (int x = 2; x < 8; x++) {
      digitalWrite(x, LOW);
    }

    // reset the LED variable to the first one
    led = 2;

    //reset the timer
    previousTime = currentTime;
  }
  // set the previous switch state to the current state
  prevSwitchState = switchState;
}
