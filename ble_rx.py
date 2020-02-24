from bluepy import btle
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time 
from time import sleep

#authentication information and topic name 
rootCAPath = "root-CA.crt"
certificatePath = "c5ffe0127c-certificate.pem.crt"
privateKeyPath = "c5ffe0127c-private.pem.key"
topic = "poll/tracking"

myAWSIoTMQTTClient = AWSIoTMQTTClient("myClientID")
myAWSIoTMQTTClient.configureEndpoint("a1jgcb96hr49vu-ats.iot.us-east-2.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTClient.connect()

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
        milli = int(round(time.time()*1000))
        sensor_data = {"Sensor_time": milli, "Temperature": temp_int, "Humidity": humidity_int}
        sensor_json = json.dumps(sensor_data)
        myAWSIoTMQTTClient.publish(topic, sensor_json, 1)
        print('Published Topic %s: %s \n' % (topic, sensor_json))
        sleep(1)
