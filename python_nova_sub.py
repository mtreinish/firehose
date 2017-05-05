import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('gerrit/openstack/nova/comment-added')

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# Create a websockets client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the firehose
client.connect('firehose.openstack.org', port=1883)
# Listen forever
client.loop_forever()
