# Dummy gateway

Dummy gateway that runs on a Raspberry Pi

Only intended as a way to connected to the test Arduino

Will hopefully connect via Bluetooth

Tested on HypriotOS (based on Debian 9.8)

Mosquitto is currently run via:

```
    docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto
```

