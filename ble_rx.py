from bluepy import btle
print("Connecting....")
dev = btle.Peripheral("E2:B4:50:FA:1D:D9")

for svc in dev.services:
    print(svc)