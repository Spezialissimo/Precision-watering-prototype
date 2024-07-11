/*
  SoilWatch 10 soil moisture sensor example - Simple

  Reads analog value of soil moisture sensor and displays it
  on the serial port.

  The circuit:
  Sensor output (white wire) connect to Analog A0 on Arduino.
  Connect VCC (brown wire) to 3.3V or 5V on Arduino (3.3V gives more stable readings)
  Connect GND (green wire) to GND on Arduino.

  created 30 Aug. 2017
  last updated 9 Feb 2018
  by Piotr Trembecki
  https://pino-tech.eu/sw10

  This example code is in the public domain.

*/

/*
******** SETUP ********

  For 1.1V version set is1V1Output to true. The usual maxADC value will be around 1000.
  For 3V version set is1V1Output to false. The usual maxADC value will be around 600.

***********************
*/
const int analogInPin_sx_sensor = A1;    
const int analogInPin_dx_sensor = A5;       // Analog input pin that the sensor output is attached to (white wire)
int minADC = 0;                       // replace with min ADC value read in air
int maxADC = 600;                     // replace with max ADC value read fully submerged in water
bool is1V1Output = false;             // set true if 1.1V output sensor is used for 3V set to false
String test = "";

int moistureValue_sx, moistureValue_dx, mappedValue_sx, mappedValue_dx;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(A1, INPUT);
  pinMode(A5, INPUT);
  if (is1V1Output == true)
    analogReference(INTERNAL); //set ADC reference to internal 1.1V
}

void loop() {
  // Leggi il valore di umidità:
  moistureValue_sx = analogRead(analogInPin_sx_sensor);
  moistureValue_dx = analogRead(analogInPin_dx_sensor);

  // Mappa il valore tra 0 e 100
  mappedValue_sx = map(moistureValue_sx, minADC, maxADC, 0, 100);
  mappedValue_dx = map(moistureValue_dx, minADC, maxADC, 0, 100);

  String output = String(mappedValue_sx) + "," + String(mappedValue_dx);
  // Stampa i risultati sul monitor seriale
  Serial.println(output);

  // Attendi 500 millisecondi prima del prossimo ciclo
  delay(500);
}
