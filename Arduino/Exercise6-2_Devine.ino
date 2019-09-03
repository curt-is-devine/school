//sets the pins that each pin of the LED is attached to with respect to color
const int greenLED = 9;
const int redLED = 11;
const int blueLED = 10;

//sets the analog pins that each photoresistor is attached to based on color
const int greenSensor = A1;
const int redSensor = A0;
const int blueSensor = A2;

//setting integers to describe how brightly to light up the LED pins later
int greenValue = 0;
int redValue = 0;
int blueValue = 0;

//setting a value for the reading of the photoresistor values for each color
int greenSensorValue = 0;
int redSensorValue = 0;
int blueSensorValue = 0;

//Additional constants for calibration, decided to do calibration for each color
//since placement of the filter is flimsy (at least in my setup) and I wanted to
//account for if each sensor has a unique succesptibility to light.
int redSensorLow = 1023;
int redSensorHigh = 0;
int greenSensorLow = 1023;
int greenSensorHigh = 0;
int blueSensorLow = 1023;
int blueSensorHigh = 0;

void setup() {
  //initialize the serial monitor as is protocol
  Serial.begin(9600);

  //set the LED pins as outputs for the Arduino circuit
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(blueLED, OUTPUT);

  //The calibration loop. While the time is less than 5 seconds:
  while (millis() < 5000) {
    //read the photoresistor values
    redSensorValue = analogRead(redSensor);
    greenSensorValue = analogRead(greenSensor);
    blueSensorValue = analogRead(blueSensor);
    //if the maximum photoresistor value for a color reads higher than the high variable for that color, 
    //then set that value as the respective high variable
    if (redSensorValue > redSensorHigh) {
      redSensorHigh = redSensorValue;
    }
    if (greenSensorValue > greenSensorHigh) {
      greenSensorHigh = greenSensorValue;
    }
    if (blueSensorValue > blueSensorHigh) {
      blueSensorHigh = blueSensorValue;
    }
    //If the minimum photoresistor value for a color reads lower than the low variable for that color, 
    //then set that value as the respective low variable
    if (redSensorValue < redSensorLow) {
      redSensorLow = redSensorValue;
    }
    if (greenSensorValue < greenSensorLow) {
      greenSensorLow = greenSensorValue;
    }
    if (blueSensorValue < blueSensorLow) {
      blueSensorLow = blueSensorValue;
    }
  }
}

void loop() {

  //read the analog values of each photoresistor and assign the value to the "___Sensorvalue" to be used later
  greenSensorValue = analogRead(greenSensor);
  //wait 5 ms before reading the next value
  delay(5);
  redSensorValue = analogRead(redSensor);
  delay(5);
  blueSensorValue = analogRead(blueSensor);
  delay(5);

  //Print in the serial monitor what the values of each photoresistor's voltage are from the previous step
  Serial.print("Color sensor values: \t Red: ");
  Serial.print(redSensorValue);
  Serial.print("\t Green: ");
  Serial.print(greenSensorValue);
  Serial.print("\t Blue: ");
  Serial.println(blueSensorValue);

  //calculates how brightly to set the output voltages for each dolored pin of the LED based on 
  //mappings from the high and low voltage values to the range 0 to 225
  greenValue = map(greenSensorValue/4, greenSensorLow/4, greenSensorHigh/4, 0, 255);
  redValue = map(redSensorValue/4, redSensorLow/4, redSensorHigh/4, 0, 255);
  blueValue = map(blueSensorValue/4, blueSensorLow/4, blueSensorHigh/4, 0, 255);

  //Print in the serial monitor what the output voltages for each pin of the LED are by color
  Serial.print("Output LED  values: \t Red: ");
  Serial.print(redValue);
  Serial.print("\t Green: ");
  Serial.print(greenValue);
  Serial.print("\t Blue: ");
  Serial.println(blueValue);

  //Set the LED pins to the appropriate voltage values
  analogWrite(greenLED, greenValue);
  analogWrite(redLED, redValue);
  analogWrite(blueLED, blueValue);

  //iterate infinitely
  }
