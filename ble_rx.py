from bluepy import btle
print("Connecting....")
dev = btle.Peripheral("E2:B4:50:FA:1D:D9")
for svc in dev.services: 
    print(str(svc))

pollution_sensor = btle.UUID("190f")
pollution_service = dev.getServiceByUUID(pollution_sensor)
for ch in pollution_service.getCharacteristics():
    print(str(ch))

