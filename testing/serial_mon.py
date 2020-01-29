import serial
from time import sleep
from serial import Serial
import paho.mqtt.client as mqtt
from UDumMI import UDumMI

DUMMY_MODE = False
SERIAL_CONN = '/dev/ttyACM0'
SERIAL_BAUD = 9600
BROKER = "localhost"
BROKER_PORT = 3389
DUMMY_DEVICE = UDumMI()
UDMIDUINO_PUB_TOPIC = 'dittick/UDMIduino-000/events'
UDMIDUINO_SUB_TOPIC = 'dittick/UDMIduino-000/lum-value'

try:
    ser = Serial(SERIAL_CONN, baudrate=SERIAL_BAUD, timeout=None)
except:
    print("Could not connect to the serial line, activating DUMMY_MODE")
    DUMMY_MODE = True

# To become a generic mapping function
# mqtt2bacnet could feature BAC0?

def mqtt2serial(message, ser):
    try:
        ser.write(b't')
    except:
        print("Problem writing back to the serial line, you might be in DUMMY_MODE")

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
client = mqtt.Client("DitTICK Dummy Gateway")  # create new instance
client.on_connect = on_connect  # bind call back function
client.on_message = on_message #attach function to callback
client.loop_start()

print("Connecting to broker ", BROKER)
client.connect(BROKER, BROKER_PORT, 60)  # connect to broker

# Subscribe to the topic from ditto (or elsewhere)

while not client.connected_flag:  # wait in loop
    print("In wait loop")
    sleep(1)

print("Subscribing to LED toggle topic... ")
client.subscribe(UDMIDUINO_SUB_TOPIC)

print("in Main Loop")
print("Publishing...")

while(True):
    if not DUMMY_MODE:
        line = ser.readline()   # read a '\n' terminated line
        try:
            decodedLine = line.decode('utf-8').rstrip()
            ret = client.publish(UDMIDUINO_PUB_TOPIC, decodedLine)
        except:
            print('Serial is a bit janky, retrying...')
            sleep(0.5)
    elif DUMMY_MODE:
        ret = client.publish(UDMIDUINO_PUB_TOPIC, DUMMY_DEVICE.generateMessage())
        sleep(0.4)

client.loop_stop()  # Stop loop
client.disconnect()  # disconnect
