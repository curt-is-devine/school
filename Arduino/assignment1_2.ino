/*This project is intended to function as a basic weather reading circuit.
 * If the weather is sunny, the user will know by the fact that the multi-color led will be shining brightly as white(ish)
 * light. In addition to reading sunlight, the circuit will also read the temperature of the location. If it is warmer
 * than the inside of a typical home, then the red LED will light to indicate that it is hot out.  
 * Such a circuit allows for a user to tell not only if it is bright out (from the dimness/brightness of the 
 * multi-colored LED), but also if it is at least hot based off of the lighting of the red LED.
 * 
 * I would have liked to include a blue and yellow LED as well to indicate cooler temperatures, but I did not have 
 * enough wiring to set up such a circuit. Had I worked with someone else, maybe this could have been a reality. 
 * However, I feel comfortable in knowing that this circuit does what it is designed to do and proves useful in the 
 * real world.
 */


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

//set the temperature sensor pin, base temp of the room (as in the previous exercise) and a variable to store the temperature sensor's reading
const int tempSensor = A3;
const int baseTemp = 20.0;
const int LED = 8;
int tempValue = 0;

void setup() {
  //initialize the serial monitor as is protocol
  Serial.begin(9600);

  //sets all of the applicable pins as outputs for the Arduino circuit
  for (int i = 8; i <= 11; i++) {
    pinMode(i, OUTPUT);
    //sets pin 8, the LED, to being off initially
    if (i == 8) digitalWrite(i, LOW);
  }
}

void loop() {

  //read the temperature sensor's value
  tempValue = analogRead(tempSensor);

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

  //Print in the serial monitor information regarding the temperature sensor and values that can be derived from it
  Serial.print("Temperature Sensor Values: ");
  Serial.print(tempValue);
  //calculates the voltage on the temperature sensor on the breadboard
  float volt = 5.0 * tempValue/1024.0;
  //displays the above mentioned voltage
  Serial.print(", Voltage: ");
  Serial.print(volt);
  //calculates the temperature on the temperature sensor based on the applied voltage
  float temp = (volt - .5) * 100;
  //displays the temperature that the sensor "reads"
  Serial.print(", degrees C: ");
  Serial.println(temp);

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

  //if the location is 5 degrees celsius hotter than the ambient temperature at my grandma's house,
  //then print a message in the Serial monitor and turn the LED on to indicate that it is hot!
  if (temp >= baseTemp + 5) {
    Serial.println("You are in a hot location!");
    digitalWrite(LED, HIGH);
  }
  //If the temperature is cooler than the aforementioned value, print a message about it being cold 
  //and turn off the red LED 
  else {
    Serial.println("Why is it so cold?");
    digitalWrite(LED, LOW);
  }
  
  //iterate infinitely
  }
