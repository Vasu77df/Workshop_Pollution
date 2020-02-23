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
pressure_uuid = btle.UUID("2d19")
temp_value = pollution_service.getCharacteristics(temperature_uuid)[0]
humidity_value = pollution_service.getCharacteristics(humidity_uuid)[0]
pressure_value = pollution_service.getCharacteristics(humidity_uuid)[0]



# Read sensor
while True:
    temp = temp_value.read()
    humidity = humidity_value.read()
    pressure = pressure_value.read()
    print(type(temp))
    print(type(humidity))
    sensor_data = {"Temperature": temp, "Humidity": humidity, "Pressure": pressure}
    print(sensor_data)
