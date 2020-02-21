/* Sensor data collector code 
 * This code exists on the arduino nano ble 
 * collecting all the sensor data and parsing it into a json object
 * 
 */

#include <Arduino_HTS221.h>
#include <Arduino_LPS22HB.h>
#include <ArduinoJson.h>


void setup() {
  Serial.begin(9600);
  while(!Serial) continue;

  if (!HTS.begin()) {
    Serial.println("Failed to initialize humidity temprature sensor!");
    while (1);
  }
  if (!BARO.begin()){
    Serial.println("Failed to initialize pressure sensor!");
    while (1);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  float pressure = BARO.readPressure();
  float temperature = HTS.readTemperature();
  float humidity = HTS.readHumidity();
  
  StaticJsonDocument<200> doc;

  doc["pressure"] = pressure;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;

  serializeJson(doc, Serial);

  Serial.println();
 
  
   delay(1000); 
  }

  