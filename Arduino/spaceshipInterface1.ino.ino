//sets a global variable that stores the state of the switch
int switchstate;

void setup() {
  /*initializes all of the pins accordingly. 
   * These lines say that pin 2 is the input pin (the one we read to determine what happens) 
   * and the others are outputs (what changes as a result of the input's state). 
   */
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
}

void loop() {
  //on every iteration of the loop, checks what the switch's state is and sets the variable appropriately
  switchstate = digitalRead(2);

  //If the switch is not clicked, then turn/keep the green light on, while turning/keeping others off
  if (switchstate == LOW) {
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
  }

  //If the switch is clicked:
  else {
    //turn off the green LED, turn on the middle red one
    digitalWrite(3, LOW);
    digitalWrite(4, HIGH);
    
    //wait 1/4 of a second
    delay(250);

    //turn off the middle LED and turn on the farthest red one
    digitalWrite(5, HIGH);
    digitalWrite(4, LOW);

    //wait another 1/4 of a second
    delay(250);

    //turn off the farthest red LED and repeat the else statement until the switch is released
    digitalWrite(5, LOW);
  }
}
