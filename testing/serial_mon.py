import serial
from time import sleep
from serial import Serial
import paho.mqtt.client as mqtt  # import the client1

SERIAL_CONN = '/dev/ttyACM0'
SERIAL_BAUD = 9600
ser = Serial(SERIAL_CONN, baudrate=SERIAL_BAUD, timeout=None)

# To become a generic mapping function
# mqtt2bacnet could feature BAC0?

def mqtt2serial(message, ser):
    ser.write(b't')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    print("message received " ,payload)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    mqtt2serial(payload, ser)


mqtt.Client.connected_flag = False  # create flag in class
broker = "localhost"
client = mqtt.Client("WPitC Dummy Gateway")  # create new instance
client.on_connect = on_connect  # bind call back function
client.on_message = on_message #attach function to callback
client.loop_start()

print("Connecting to broker ", broker)
client.connect(broker)  # connect to broker

# Subscribe to the topic from ditto (or elsewhere)

while not client.connected_flag:  # wait in loop
    print("In wait loop")
    sleep(1)

print("Subscribing to LED toggle topic... ")
client.subscribe("arup-8-fitzroy-street/UDMIduino-000/lum-value")

print("in Main Loop")
print("Publishing...")

while(True):
    line = ser.readline()   # read a '\n' terminated line
    try:
        decodedLine = line.decode('utf-8').rstrip()
        ret = client.publish("arup-8-fitzroy-street/UDMIduino-000/events", decodedLine)
    except:
        print('Serial is a bit janky, retrying...')
        sleep(0.5)

client.loop_stop()  # Stop loop
client.disconnect()  # disconnect
