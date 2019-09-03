
//Declare the global constants for the analog pin number and the base temperature (at my grandma's house) in degrees celsius
const int analogPin = A0;
const float baseTemp = 23.0;
//In addition, declare a variable for the state of an implemented switch
int switchState = 0;

//initialize the variables we need for this project
void setup() {
  //This command just sets up the connection between the arduino and the computer
  Serial.begin(9600);
  //a for loop that sets up the mode for every digital pin LED to be outputs and sets them to the off status
  for (int i = 2; i <= 6; i++) {
    //if statement to set pin 6 as the switch input
    if (i == 6) {
      pinMode(i, INPUT);
    }
    //all other digital pins are set as output and turned off
    else {
      pinMode(i, OUTPUT); 
      digitalWrite(i, LOW);    
    }
  }  
}

void loop() {
  //set a variable on the analog input from the temperature sensor as well as the state of the switch
  int analogVal = analogRead(analogPin);
  switchState = digitalRead(6);
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

  //if the temperature read by the sensor is less than the base temperature established above and the switch is clicked down,
  //then turn off all LEDs except for the blue (ice) one. display an appropriate message in the serial monitor
  if (temp < baseTemp && switchState != LOW) {
    Serial.println("Brrr... you are ice cold!");
    digitalWrite(2, HIGH);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    //if the temperature read by the sensor is greater than the ambient temperature but less than the temperature + 2 degrees
    //while also having the switch clicked down, then turn on the first LED only.
  } else if (temp >= baseTemp && temp < baseTemp + 2.0 && switchState != LOW) {
    //displays an appropriate message about the temperature
    Serial.println("You are slightly hotter than 'lukewarm'");
    //for loop to make sure that the green LED lights up twice per second when the temperature is in this range
    for (int i = 1; i < 3; i++) {
      digitalWrite(2, LOW);
      digitalWrite(3, HIGH);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      delay(250);
      digitalWrite(3, LOW);
      delay(250);
    }
    //if the temperature read by the sensor is greater than the ambient temperature + 2 degrees but less than the ambient 
    //temperature + 4 degrees and the switch is clicked, then turn on the first and second LEDs only.
  } else if (temp >= baseTemp + 2.0 && temp < baseTemp + 4.0 && switchState != LOW) {
    //displays a message in the serial monitor about the measured temperature
    Serial.println("You are so mildly warm its ridiculous.");
    //for loop that iterates such that the yellow LED will light up four times per second that the temperature is in the desired range
    //the green LED stays lit the entire time
    for (int i = 0; i < 5; i++){
      digitalWrite(2, LOW);
      digitalWrite(3, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(5, LOW);
      delay(125);
      digitalWrite(4, LOW);
      delay(125);
    }
    //for all other temperature inputs (must be greater than the ambient temperature + 4 degrees celsius), turn on all LEDs because you are hot.
  } else if(temp >= baseTemp + 4.0 && switchState != LOW){
    //display in the serial monitor how hot you are.
    Serial.println("You are so hot, you're making me sweat!");
    //for loop that iterates such that the red (hot) LED will light up eight times per second that the temperature is in the desired range
    //the green and yellow LEDs stay lit the entire time
      for (int i = 1; i < 9; i++) {
        digitalWrite(2, LOW);
        digitalWrite(3, HIGH);
        digitalWrite(4, HIGH);
        digitalWrite(5, HIGH);
        delay(62.5);
        digitalWrite(5, LOW);
        delay(62.5);
      }
      //else statement to handle if the switch is not pressed
  } else {
    //tell the user what to do in the serial monitor and turn off all LEDs
    Serial.println("You need to push the button to see how hot you are.");
    for (int i = 2; i <= 5; i++) {
      digitalWrite(i, LOW);    
    }
  }
        
  //repeat this loop every millisecond
  delay(1);
}
