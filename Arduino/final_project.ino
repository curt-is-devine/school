//Inlcuding the library used for microphones to measure frequency
#include <AudioFrequencyMeter.h>

//Starting an instance of a frequency meter (the microphone)
AudioFrequencyMeter meter;

//Variables for the voltage on the switches so that we use the right procedure and
//an integer to store the pots value, a calculation integer to determine length of recording, and
//Notes that will be used by the piezo as output,
int switch1;
int switch2;
int s1loc = 6;
int s2loc = 4;
int led = 5;
int piezo = 7;
int mic = A0;
int notes[200];

void setup() {
  Serial.begin(9600);
  pinMode(s1loc, INPUT);
  pinMode(piezo, OUTPUT);
  pinMode(s2loc, INPUT);
  pinMode(led, OUTPUT);
  pinMode(mic, INPUT);
  //Initialize the notes array
  for (int i = 0; i < 200; i++) {
    notes[i] = 100;
  }

  //Setting the mininum and maximum bandwidth of the sound that the arduino will register
  meter.setBandwidth(70.00, 1500);
  //Start the microphone on analog 0 and __________
  meter.begin(A0, 45000);
}

void loop() {

  //read the voltage on the voltage ladder
  switch1 = digitalRead(s1loc);
  switch2 = digitalRead(s2loc);
  //If switch 1 is clicked:
  if (switch1 == HIGH) {
    //Turn on the "Recording" LED
    digitalWrite(led, HIGH);
    //and record the notes read by the microphone every 25 ms for as long as the user specified in the pot
    for (int i = 0; i < 200; i++) {
      notes[i] = meter.getFrequency();
      delay(50);
    }
    //Once recording is done, turn of the recording LED
    digitalWrite(led, LOW);
    //If the second switch is clicked
  } else if (switch2 == HIGH) {
    //read the array of notes recorded by the microphone in the user determined time range and output them to the piezo
    for (int i = 0; i < 200; i++) {
        Serial.println(notes[i]);
        tone(piezo, 300, 50);
    }
  }

  delay(50);

}
