/*
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, version 2 of the License, and
 only version 2.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
 
/*
  This is the I/O program for the Bloominglabs/Wonderlab Laser Maze.
  
  The sensor pins are connected to vibration sensors connected to ground.  The buttons are
  also connected between the pin and ground.
 */

// Sensor Pins
#define SENSOR03  3
#define SENSOR04  4
#define SENSOR05  5
#define SENSOR06  6
#define SENSOR07  7
#define SENSOR08  8
#define SENSOR09  9
#define SENSOR10  10

// Buttons
#define RESET_BUTTON  2
#define RED_BUTTON    11
#define GREEN_BUTTON  12

void setup() {
  Serial.begin(9600);

  // Set all pins to inputs
  pinMode(SENSOR03,INPUT_PULLUP);
  pinMode(SENSOR04,INPUT_PULLUP);
  pinMode(SENSOR05,INPUT_PULLUP);
  pinMode(SENSOR06,INPUT_PULLUP);
  pinMode(SENSOR07,INPUT_PULLUP);
  pinMode(SENSOR08,INPUT_PULLUP);
  pinMode(SENSOR09,INPUT_PULLUP);
  pinMode(SENSOR10,INPUT_PULLUP);

  pinMode(RESET_BUTTON,INPUT_PULLUP);
  pinMode(RED_BUTTON,INPUT_PULLUP);
  pinMode(GREEN_BUTTON,INPUT_PULLUP);
}
 
void loop() {
  // Check sensors
  if ( ! digitalRead(SENSOR07) ) {
    Serial.println("6");
    delay(100);
  }
  if ( ! digitalRead(SENSOR08) ) {
    Serial.println("5");
    delay(100);
  }
  if ( ! digitalRead(SENSOR09) ) {
    Serial.println("4");
    delay(100);
  }
  if ( ! digitalRead(SENSOR10) ) {
    Serial.println("3");
    delay(100);
  }
  if ( ! digitalRead(SENSOR06) ) {
    Serial.println("2");
    delay(100);
  }
  if ( ! digitalRead(SENSOR05) ) {
    Serial.println("1");
    delay(100);
  }
  if ( ! digitalRead(SENSOR04) ) {
    Serial.println("7");
    delay(100);
  }
  if ( ! digitalRead(SENSOR03) ) {
    Serial.println("8");
    delay(100);
  }
  if ( ! digitalRead(RESET_BUTTON) ) {
    int i = 0;
    do {
      delay(100);
      i++;
    } while ( (i < 20) && (! digitalRead(RESET_BUTTON)) );
    if (i == 20 ) {
      Serial.println("r");
    }
    while ( ! digitalRead(RESET_BUTTON) )
      ;
  }
  if ( ! digitalRead(RED_BUTTON) ) {
    delay(50);
    if ( ! digitalRead(RED_BUTTON) ) {
      Serial.println("a");
    }
    while ( ! digitalRead(RED_BUTTON) )
      ;
  }
  if ( ! digitalRead(GREEN_BUTTON) ) {
    delay(50);
    if ( ! digitalRead(GREEN_BUTTON) ) {
      Serial.println("d");
    }
    while ( ! digitalRead(GREEN_BUTTON) )
      ;
  }
}

