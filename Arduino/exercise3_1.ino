
//Declare the global constants for the analog pin number and the base temperature (at my grandma's house) in degrees celsius
const int analogPin = A0;
const float baseTemp = 23.0;

//initialize the variables we need for this project
void setup() {
  //This command just sets up the connection between the arduino and the computer
  Serial.begin(9600);
  //a for loop that sets up the mode for every digital pin LED to be outputs and sets them to the off status
  for (int i = 2; i < 5; i++) {
    pinMode(i, OUTPUT); 
    digitalWrite(i, LOW);
  }
}

void loop() {
  //set a variable on the analog input from the temperature sensor
  int analogVal = analogRead(analogPin);
  //I initially did not split these commands up due to confusion about types. Will not make that mistake again!
  //displays the analog value from the temperature sensor
  Serial.print("Sensor Value: ");
  Serial.print(analogVal);
  //calculates the voltage on the temperature sensor on the breadboard
  float volt = 5.0 * analogVal/1024.0;
  //displays the above mentioned voltage
  Serial.print(", Voltage: ");
  Serial.print(volt);
  //calculates the temperature on the temperature sensor based on the applied voltage
  float temp = (volt - .5) * 100;
  //displays the temperature that the sensor "reads"
  Serial.print(", degrees C: ");
  Serial.println(temp);

  //if the temperature read by the sensor is less than the base temperature established above
  //then turn off all LEDs
  if (temp < baseTemp) {
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    //if the temperature read by the sensor is greater than the ambient temperature but less than the temperature + 2 degrees
    //then turn on the first LED only.
  } else if (temp >= baseTemp && temp < baseTemp + 2.0) {
    digitalWrite(2, HIGH);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    //if the temperature read by the sensor is greater than the ambient temperature + 2 degrees but less than the ambient 
    //temperature + 4 degrees then turn on the first and second LEDs only.
  } else if (temp >= baseTemp + 2.0 && temp < baseTemp + 4.0) {
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
    //for all other temperature inputs (must be greater than the ambient temperature + 4 degrees celsius), turn on all LEDs because you are hot.
  } else {
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
  }    
  //repeat this loop every millisecond
  delay(1);
}
