from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import subprocess as subprocess
from time import sleep

#authentication information and topic name 
rootCAPath = "root-CA.crt"
certificatePath = "c5ffe0127c-certificate.pem"
privateKeyPath = "c5ffe0127c-private.pem.key"
topic = "poll/tracking"

myAWSIoTClient = AWSIoTMQTTClient("myClientID")
myAWSIoTMQTTClient = AWSIoTMQTTClient("myClientID")
myAWSIoTMQTTClient.configureEndpoint("a1jgcb96hr49vu-ats.iot.us-east-2.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTClient.connect()

message = {"temperature": 35}
messageJson = json.dumps(message)
myAWSIoTClient.publish(topic, messageJson, 1)
print('Published Topic %s: %s \n' % (topic, messageJson))

