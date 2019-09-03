//Variables to be used throughout the program for the user and computers rock/paper/scissors selection (as 1, 2, or 3)
//and global integers to keep track of the wins/losses
int userRPS;
int compRPS;
int wins = 0;
int losses = 0;

void setup() {

  //starts the serial monitor (useful for debugging)
  Serial.begin(9600);

  //Sets each pin used as output (for LED/piezo)
  for ( int i = 2; i <= 5; i++) {
    pinMode(i, OUTPUT);
  }
  //or input for the resistor ladder
  pinMode(6, INPUT);
}

//helper function that plays the "Game over" song from classic Super Mario Bros games
void playGameOver() {
  /*I dont think commenting every line here is necessary since its the same idea in every stanza.
   * Set the tone of the piezo (on pin 6) to the notes used in the game over song from Super Mario
   * Bros. With delays in between such that the song plays at about the same speed, with the same
   * note articulation as in the original song. I would like to say I transcribed tbe song and worked 
   * from there, but I actually got the sheet music for the song from www.mariopiano.com
   * I then converted each note into a frequency using pages.mtu.edu's note to frequency conversion chart.
   * I have a music background so the conversion was easy for me
   */
  tone(6, 330);
  delay(150);
  
  noTone(6);
  delay(333);
  
  tone(6, 262);
  delay(150);
  
  noTone(6);
  delay(333);
  
  tone(6, 196);
  delay(333);

  tone(6, 440);
  delay(222);
  tone(6, 493);
  delay(222);
  tone(6, 440);
  delay(222);

  tone(6, 415);
  delay(333);
  tone(6, 466);
  delay(333);
  tone(6, 415);
  delay(333);

  tone(6, 330);
  delay(150);
  tone(6, 294);
  delay(150);
  tone(6, 330);
  delay(666);

  //turns off the piezo when the song is done
  noTone(6);
}

//Another helper function that compares the user and computer's selections
void compare() {
  //If there is a tie, light up the yellow LED, keep it on for two second, then turn it off
  if (userRPS == compRPS) {
    digitalWrite(5, HIGH);
    delay(2000);
    digitalWrite(5, LOW);
  }

  //if the user wins (in this case RPS -> rock paper scissors, and the number represents
  //the according selection in that list, so paper beats rock, scissors beats paper.
  else if (1 == userRPS - compRPS) {
    //turn on the smiley face for two seconds then turn it off
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    delay(2000);
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    //add one to the wins counter since the user won
    wins += 1;
  }
  //if the computer wins, play a low note on the piezo for 2 seconds then turn it off
  else if (1 == compRPS - userRPS) {
    tone(6, 50);
    delay(2000);
    noTone(6);
    //increment the loss counter since the computer won that round
    losses += 1;
  }
  //same clause as the user winning above since rock beats scissors, but this wasnt as easy a math problem
  else if (userRPS == 1 && compRPS == 3) {
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    delay(2000);
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    wins += 1;
  }
  //same clause as the computer winning above since scissors beats rock. Again, not as easy a calculation so
  //it got its own stanza 
  else if (userRPS == 3 && compRPS == 1) {
    tone(6, 50);
    delay(2000);
    noTone(6);
    losses += 1;
  }
}

void loop() {

  //read the voltage from the resistor ladder
  int volt = analogRead(A0);

  //if the ladder has over 1000  then the "first" selection is chosen. 
  if (volt >= 1000) {
    //users selection is 1, computers is generated, and then the compare function is called on the values
    userRPS = 1;
    compRPS = random(1, 4);
    compare();
  }
  //if the ladder has less than 1000 but more than 450, then the "second" selection is chosen
  else if (volt > 450 && volt < 1000) {
    //users selection is 2, computer's is randomly generated, then the compare function is called
    userRPS = 2;
    compRPS = random(1, 4);
    compare();
  }
  //Same logic as the previous stanza. if the voltage is less than 450, then the "third" selection is chosen
  else if (volt <= 450 && volt != 0) {
    //user selection is 3, computer's is generated, and then they are compared
    userRPS = 3;
    compRPS = random(1, 4);
    compare();    
  }

  //When there as ten losses, the mario gmae over theme is played and the win/loss counters are reset
  if (losses == 10) {
    playGameOver();
    losses = 0;
    wins = 0;  
  }
  //Then there are 10 wins, the smiley face flashes 5 times in a second, then the win/loss counters are reset to 0
  if (wins == 10) {
    for (int i = 0; i < 5; i++){
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    delay(100);
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    delay(100);
    }
    losses = 0;
    wins = 0;
  }

  //displays the win/loss numbers in the serial monitor
  Serial.print("Wins: ");
  Serial.print(wins);
  Serial.print(" Losses: ");
  Serial.println(losses);
  
}
