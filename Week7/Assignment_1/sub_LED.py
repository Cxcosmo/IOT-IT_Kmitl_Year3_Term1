import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode (GPIO.BCM)
LIGHT = 4

GPIO.setup(LIGHT, GPIO.OUT)

def on_message(client, userdata, msg):
	payload = msg.payload.decode()

	print("-----------------")
	print("userdata =", userdata)
	print("topic =", msg.topic)
	print("payload =", payload)
	print("QoS :", msg.qos)
	print("Retain :", msg.retain)

	if payload == "ON":
		GPIO.output(LIGHT, True)
	elif payload == "OFF":
		GPIO.output(LIGHT, False)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
	client_id="panwit-sub",
	protocol=mqtt.MQTTv5)

mqttc.will_set(
	"67070066/sub_status",
	payload="offline",
	qos=1,
	retain=True
)

mqttc.publish(
	"67070066/sub_status",
	payload="online",
	qos=1,
	retain=True
)

mqttc.on_message = on_message

properties = mqtt.Properties(mqtt.PacketTypes.CONNECT)
properties.SessionExpiryInterval = 3600

mqttc.connect("mqtt-dashboard.com", 1883,
	clean_start=False ,properties=properties)

mqttc.subscribe("67070066/pub_status", qos=1)
mqttc.subscribe("67070066/pub", qos=1)

mqttc.loop_forever()
