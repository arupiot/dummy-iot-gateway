import serial
from time import sleep
from serial import Serial
import paho.mqtt.client as mqtt  # import the client1


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


mqtt.Client.connected_flag = False  # create flag in class
broker = "localhost"
client = mqtt.Client("WPitC Dummy Gateway")  # create new instance
client.on_connect = on_connect  # bind call back function
client.loop_start()

print("Connecting to broker ", broker)
client.connect(broker)  # connect to broker

while not client.connected_flag:  # wait in loop
    print("In wait loop")
    sleep(1)


print("in Main Loop")
print("Publishing...")


with Serial('/dev/ttyACM0', baudrate=9600, timeout=None) as ser:
    while(True):
        line = ser.readline()   # read a '\n' terminated line
        ret = client.publish(
            "arup-8-fitzroy-street/UDMIduino-000/events", str(line))

client.loop_stop()  # Stop loop
client.disconnect()  # disconnect