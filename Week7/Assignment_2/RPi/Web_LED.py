import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json

GPIO.setmode (GPIO.BCM)

Red = 17
Green = 27
Blue = 22

GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)
GPIO.setup(Blue, GPIO.OUT)

def on_message(client, userdata, msg):
	payload = json.loads(msg.payload.decode())

	print("-----------------")
	print("topic =", msg.topic)
	print(
    		f"RED = {'ON' if payload['red'] else 'OFF'} | "
    		f"GREEN = {'ON' if payload['green'] else 'OFF'} | "
    		f"BLUE = {'ON' if payload['blue'] else 'OFF'}"
	)

	GPIO.output(Red, not payload["red"])
	GPIO.output(Green, not payload["green"])
	GPIO.output(Blue, not payload["blue"])

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
	client_id="67070066_sub",
	protocol=mqtt.MQTTv5)

mqttc.will_set(
	"67070066/LED_status",
	payload="offline",
	qos=1,
	retain=True
)

mqttc.publish(
	"67070066/LED_status",
	payload="online",
	qos=1,
	retain=True
)

mqttc.on_message = on_message

properties = mqtt.Properties(mqtt.PacketTypes.CONNECT)
properties.SessionExpiryInterval = 3600

mqttc.connect("mqtt-dashboard.com", 1883,
	clean_start=False ,properties=properties)

mqttc.subscribe("67070066/LED", qos=1)

mqttc.loop_forever()
