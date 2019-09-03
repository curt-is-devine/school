//Define a variable to hold the value that the photoresistor receives
int sensorValue;

//set logical variables for the calibration of the photoresistor
int sensorLow = 1023;
int sensorHigh = 0;

//set a variable for the pin of the LED that shows when the circuit is calibrating
const int ledPin = 13;

void setup() {

  //set the LED pin as output and turn on the LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  //The calibration loop. While the time is less than 5 seconds:
  while (millis() < 5000) {
    //read the photoresistor value
    sensorValue = analogRead(A0);
    //if the photoresistor reads higher than the high variable, then set that value as the high variable
    if (sensorValue > sensorHigh) {
      sensorHigh = sensorValue;
    }
    //If the photoresistor reads lower than the low variable, then set that value as the low variable
    if (sensorValue < sensorLow) {
      sensorLow = sensorValue;
    }
  }

  //turn off the LED when calibration is done
  digitalWrite(ledPin, LOW);

}

void loop() {
  // put your main code here, to run repeatedly:
  sensorValue = analogRead(A0);

  //set the pitch to be the sensor's value, with the range of high/low values in the ambient setting
  //mapped to the highs and lows of the piezzo
  int pitch = map(sensorValue, sensorLow, sensorHigh, 50, 4000);

  //have the piezzo output the pitch to the 8th pin every 20 ms
  tone(8, pitch, 20);

  //wait 10 ms before reiterating
  delay(10);

}
