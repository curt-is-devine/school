//sets global variables that store the state of the switch as well as which iteration of the loop it is when called in a loop
int switchstate;
int looper = 1;

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

  //If the switch is not clicked, then turn/keep the green light on, while turning/keeping others off. Reset the loop iterator in case the switch was just unclicked
  if (switchstate == LOW) {
    looper = 1;
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
  }

  //if the switch is clicked
  else {
    //and if this is some 3rd iteration of the loop:
    if (looper % 3 == 0 && looper/3 >= 1) {
      //turn on the green and middle red LEDs and turn off the red
      digitalWrite(3, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(5, LOW);

      //wait 1/4 of a second
      delay(250);

      //turn off the lit LEDs and light up the farthest red one
      digitalWrite(3, LOW);
      digitalWrite(5, HIGH);
      digitalWrite(4, LOW);

      //wait another 1/4 of a second before moving to the next loop
      delay(250);
    }

    //if this isnt a 3rd iteration of the loop:
    else {
      //turn the middle red LED on and turn the others off
    digitalWrite(3, LOW);
    digitalWrite(4, HIGH);
    digitalWrite(5, LOW);

    //wait 1/4 of a second 
    delay(250);

    //turn on the farthest red LED and turn off the middle one
    digitalWrite(5, HIGH);
    digitalWrite(4, LOW);

    //wait 1/4 a second before iterating appropriately
    delay(250);
    }
    //increment the counter that keeps track of which iteration of the loop we are on
    looper++;
  }
}
