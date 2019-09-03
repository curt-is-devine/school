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

void setup() {
  //initialize the serial monitor as is protocol
  Serial.begin(9600);

  //set the LED pins as outputs for the Arduino circuit
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
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

  //calculates how brightly to set the output voltages for each dolored pin of the LED
  greenValue = greenSensorValue/4;
  redValue = redSensorValue/4;
  blueValue = blueSensorValue/4;

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
