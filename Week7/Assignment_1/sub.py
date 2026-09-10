import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
	print("-----------------")
	print("userdata =", userdata)
	print("topic =", msg.topic)
	print("payload =", msg.payload.decode())
	print("QoS :", msg.qos)
	print("Retain :", msg.retain)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
	client_id="67070066_sub",
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
