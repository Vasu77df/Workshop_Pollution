from bluepy import btle
print("Connecting....")
dev = btle.Peripheral("E2:B4:50:FA:1D:D9")

for svc in dev.services:
    print(str(svc))

sensor = btle.UUID("0000190f-0000-1000-8000-00805f9b34fb")

service = dev.getServiceByUUID(sensor)
for ch in service.getCharacteristics():
    print(str(ch))

