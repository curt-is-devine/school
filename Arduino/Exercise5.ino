
//Declaration of variables for the pins of the potentiometer and the switch
const int potPin = A0;
const int switchPin = 2;

//variables to store values of the potentiometer's stored voltage, the output value to the color
//changing led, the state of the switch, and an index for what iteration of the color cycle we are on.
//by default set to the green setting
int potValue = 0;
int ledValue = 0;
int switchState = 0;
int switchTurn = 3;


//helper function that takes three inputs: a minimum  and maximum pin number and the setting they
//should all be. the function simply sets them appropriately and returns a 0 to signal that it is done
int setPins(int pinMin, int pinMax, int io) {
  for (int pin = pinMin; pin <= pinMax; pin++) {
    pinMode(pin, io);
  }

  return 0;
}


void setup() {

  //sets the switch to be an input, sets all of the LED pins, and sets the pin for the apotentiometer
  pinMode(2, INPUT);
  setPins(3, 5, OUTPUT);
  setPins(9, 11, OUTPUT);
  pinMode(A0, INPUT);

  //writes the LED pin of the first color in the loop to be on
  digitalWrite(switchTurn, HIGH);
  
}

//helper function to change color of the LEDs being controlled. takes no inputs
int changeColor() {
  //writes the previous static LED to be off
  digitalWrite(switchTurn, LOW);

  //changes which color the circuit is now focusng on
  if (switchTurn == 5) switchTurn=3;
  else switchTurn++;

  //wirtes the appropriate LED on and waits for 1/4 of a second before allowing the user to continue
  digitalWrite(switchTurn, HIGH);
  delay(250);

  //returns 0 simply to return something
  return 0;
}

void loop() {

  //reads the value of charge store din the potentiometer and the state of the switch
  potValue = analogRead(potPin);
  switchState = digitalRead(switchPin);

  //if the switch is pressed, change colors using the helper function defined above
  if (switchState == HIGH) changeColor();

  //set the value of the LED to be proportional to the value of charge in the pot
  ledValue = potValue/4;

  //write the color changing LED pin appropriately (+6 since the pins are 6 away form each other in my setup
  analogWrite(switchTurn + 6, ledValue);

  //wait 15ms before reiterating
  delay(15);
  
}
