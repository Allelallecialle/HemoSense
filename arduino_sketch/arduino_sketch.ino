/*
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)
*/
// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
uint8_t pin_out_8 = 8; //pin for buzzer, led and motor
uint8_t pin_out_9 = 9; //pin for buzzer
uint8_t pin_out_10 = 10; //pin for led
long randNumber;
long python_input;
int i = 0;

void setup() {
  Serial.begin(9600);
  lcd.clear();
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  pinMode(pin_out_9, OUTPUT);
  pinMode(pin_out_8, OUTPUT);
  pinMode(pin_out_10, OUTPUT);
}

void loop() {
  while(Serial.available() > 0){
    // Serial read from python to set the LCD number
    python_input = Serial.read();

    //serial communication with the python script. Python sends a random number to trigger the alarm
    if(python_input != 0){
      Serial.print(python_input);
      //generate random number for the patient's seat number with the serial input
      randomSeed(python_input);
      randNumber = random(1, 20);


      // Print a message to the LCD.
      lcd.print("Patient's seat:");
      // set the cursor to column 0, line 1
      // (note: line 1 is the second row, since counting begins with 0):
      lcd.setCursor(0, 1);
      // print the number of seconds since reset:
      lcd.print(randNumber);

      //activate buzzer, led and motor
      while(i!=6){
        digitalWrite(pin_out_8, HIGH);
        //digitalWrite(pin_out_9, HIGH);
        tone(pin_out_9, 1000, 500);
        digitalWrite(pin_out_10, HIGH);
        delay(500);
        digitalWrite(pin_out_8, LOW);
        //digitalWrite(pin_out_9, LOW);
        //noTone(pin_out_9);
        digitalWrite(pin_out_10, LOW);
        delay(700);
        i++;
      }

      // set the python_input to 0 to exit the loop
      python_input = 0;
      lcd.clear();
    }
  }
  
}