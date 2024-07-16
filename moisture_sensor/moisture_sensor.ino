#include <ArduinoJson.h>

const int Sensors[3][2] = {{A0, A1}, {A2, A3}, {A4, A5}};
const String JsonNames[3][2] = {{"ms_10_10", "ms_10_30"}, {"ms_20_10", "ms_20_30"}, {"ms_30_10", "ms_30_30"}};
const int PumpPin = 2;

int minADC = 0;
int maxADC = 600;
int values[3][2];

void setup() {
  Serial.begin(9600);
  pinMode(A1, INPUT);
  pinMode(A5, INPUT);
}

void loop() {
  JsonDocument doc;

  for (int i=0; i<3; i++) {
    for (int j=0; j<2; j++) {
      doc[JsonNames[i][j]] = map(analogRead(Sensors[i][j]), minADC, maxADC, 0, 100);
    }
  }


  String output;
  serializeJson(doc, output);
  Serial.println(output);

  if( Serial.available() > 0 ) {
    int pumpState = Serial.read();
    if( pumpState == '1' ) {
      digitalWrite(PumpPin, HIGH);
    } else {
      digitalWrite(PumpPin, LOW);
    }
  }

  delay(500);
}
