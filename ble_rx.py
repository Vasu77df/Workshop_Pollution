from bluepy import btle
import json
print("Connecting....")
dev = btle.Peripheral("E2:B4:50:FA:1D:D9")
for svc in dev.services: 
    print(str(svc))

pollution_sensor = btle.UUID("190f")
pollution_service = dev.getServiceByUUID(pollution_sensor)
for ch in pollution_service.getCharacteristics():
    print(str(ch))

temperature_uuid = btle.UUID("2b19")
humidity_uuid = btle.UUID("2c19")
temp_value = pollution_service.getCharacteristics(temperature_uuid)[0]
humidity_value = pollution_service.getCharacteristics(humidity_uuid)[0]

def converter(data):
    data = str(data)
    data = data.strip('b')
    data = data.strip("'")
    data = data.strip('\\r\\n')
    data = data.strip("x")
    data = int(data, 16)

    return data

# Read sensor
if __name__ == "__main__":
    while True:
        temp = temp_value.read()
        humidity = humidity_value.read()
        temp_int = converter(temp)
        humidity_int = converter(humidity)
        sensor_data = {"Temperature": temp_int, "Humidity": humidity_int}
        sensor_json = json.dumps(sensor_data)
        print(sensor_json)
