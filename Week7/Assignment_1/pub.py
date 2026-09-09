import paho.mqtt.client as mqtt
import time
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)

mqttc.will_set(
	"67070066/pub_status",
	payload="offline",
	qos=1,
	retain=True
)

def on_message(client, userdata, msg):
	status = msg.payload.decode()

	if status == "offline":
		print("SUB Offline")
	elif status == "online":
		print("SUB Online")

mqttc.connect("mqtt-dashboard.com", 1883)
mqttc.on_message = on_message
mqttc.subscribe("67070066/sub_status", qos=1)
mqttc.loop_start()

index = 1
while True:
	mqttc.publish("67070066/pub", "Hello" + str(index) , qos=1)
	time.sleep(2)
	index += 1
