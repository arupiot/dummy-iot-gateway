# Dummy gateway

Dummy gateway that runs on a Raspberry Pi

Only intended as a way to connected to the test Arduino

Will hopefully connect via Bluetooth

Tested on HypriotOS (based on Debian 9.8)

Mosquitto is currently run via:

```
    docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto
```

## Getting started with the UDMIduino

### Steps

- Plug in the UDMIduino via USB into the 'Pi
- On the 'Pi, start mosquitto: `docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto`
- Run serial_mon.py: `sudo python3 serial_mon.py`
    - This converts serial UDMI messages from the Arduino into MQTT
    - Messages are published on topic = 'arup-8-fitzroy-street/UDMIduino-000/events'

```
$ sudo python3 serial_mon.py 
Connecting to broker  localhost
In wait loop
connected OK
in Main Loop
Publishing...
```
 
- Sanity check communications are happening correctly:
    - With the mosquitto docker container _still running_ on the 'Pi, enter the 'ash' shell. (No, it's not bash, the mosquitto image uses Alpine linux): `docker exec -it --name-of-image-- ash`. Find the name of your mosquitto image with `docker ps` e.g. `docker exec -it amazing_wright ash`
    - Check that packets are coming through with `mosquitto_sub -t arup-8-fitzroy-street/UDMIduino-000/events`

e.g.

```
$ docker exec -it amazing_wright /bin/ash
/ # mosquitto_sub -t arup-8-fitzroy-street/UDMIduino-000/events
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":165},"lum_value":{"present_value":100},"dimmer_value":{"present_value":90}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":48},"lum_value":{"present_value":100},"dimmer_value":{"present_value":207}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":107},"lum_value":{"present_value":100},"dimmer_value":{"present_value":148}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":128},"lum_value":{"present_value":100},"dimmer_value":{"present_value":127}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":48},"lum_value":{"present_value":100},"dimmer_value":{"present_value":207}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":145},"lum_value":{"present_value":100},"dimmer_value":{"present_value":110}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":84},"lum_value":{"present_value":100},"dimmer_value":{"present_value":171}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":51},"lum_value":{"present_value":100},"dimmer_value":{"present_value":204}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":166},"lum_value":{"present_value":100},"dimmer_value":{"present_value":89}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":48},"lum_value":{"present_value":100},"dimmer_value":{"present_value":207}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":111},"lum_value":{"present_value":100},"dimmer_value":{"present_value":144}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":130},"lum_value":{"present_value":100},"dimmer_value":{"present_value":125}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":47},"lum_value":{"present_value":100},"dimmer_value":{"present_value":208}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":146},"lum_value":{"present_value":100},"dimmer_value":{"present_value":109}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":88},"lum_value":{"present_value":100},"dimmer_value":{"present_value":167}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":51},"lum_value":{"present_value":100},"dimmer_value":{"present_value":204}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":165},"lum_value":{"present_value":100},"dimmer_value":{"present_value":90}}}\r\n'
b'{"version":1,"timestamp":"0","points":{"lux_level":{"present_value":47},"lum_value":{"present_value":100},"dimmer_value":{"present_value":208}}}\r\n'
```


## Other helpful commands

Subscribe to _all_ topics with `mosquito_sub`:

```
mosquitto_sub -v -h localhost -p 1883 -t '#'
```

Mount the code on the 'Pi gateway to your local machine, e.g.

```
sudo sshfs -o allow_other  pirate@10.8.0.62:/home/pirate/WPitC ./mnt
```