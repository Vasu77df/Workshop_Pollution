#include <ArduinoBLE.h>
#include <Arduino_HTS221.h>
#include <Arduino_LPS22HB.h>
// BLE battery characteristics
BLEService pollutionService("190f");

//BLE Pollution Characteristics 
BLEUnsignedCharCharacteristic temperatureLevelChar("2b19", BLERead | BLENotify);
BLEUnsignedCharCharacteristic humidityLevelChar("2c19", BLERead | BLENotify);
BLEUnsignedCharCharacteristic pressureLevelChar("2b19", BLERead | BLENotify);// standard 16-bit characteristic UUID
// remote clients will be able to get notifications if this characteristic changes

void setup() {
    Serial.begin(9600);
    while(!Serial);
    if (!BLE.begin()) {
        Serial.println("Staring BLE Failed!");
        while(1);
    }

    if (!HTS.begin()) {
    Serial.println("Failed to initialize humidity temprature sensor!");
    while (1);
    }
    if (!BARO.begin()){
    Serial.println("Failed to initialize pressure sensor!");
    while (1);
    }
    /* Set a local name for the BLE device
     This name will appear in advertising packets
     and can be used by remote devices to identify this BLE device
     The name can be changed but maybe be truncated based on space left in advertisement packet
    */

    BLE.setLocalName("PollutionMonitor");
    BLE.setAdvertisedService(pollutionService);
    pollutionService.addCharacteristic(temperatureLevelChar);
    pollutionService.addCharacteristic(humidityLevelChar);
    pollutionService.addCharacteristic(pressureLevelChar);
    BLE.addService(pollutionService);
 
    /* Start advertising BLE.  It will start continuously transmitting BLE
     advertising packets and will be visible to remote BLE central devices
     until it receives a new connection */

    // start advertising
    BLE.advertise();

    Serial.println("Bluetooth device active, waiting for connections ... ");
}

void loop() {
    // wait for a BLE central
    BLEDevice central = BLE.central();

    if(central) {
        Serial.print("Connected to central: ");
        // print the central's BT address:
        Serial.println(central.address());
        // turn on the LED to indicate the connection
        digitalWrite(LED_BUILTIN, HIGH);
        //while central is connected: 
        while (central.connected()) {
            while (true){
                float pressure = BARO.readPressure();
                float temperature = HTS.readTemperature();
                float humidity = HTS.readHumidity();
                temperatureLevelChar.writeValue(temperature);
                humidityLevelChar.writeValue(humidity);
                pressureLevelChar.writeValue(pressure);   
                delay(1000);     
            }
        }
        digitalWrite(LED_BUILTIN, LOW);
        Serial.print("Disconnected from central: ");
        Serial.println(central.address());
    }
}