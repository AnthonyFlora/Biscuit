import paho.mqtt.client as mqtt

def on_receive(client, userdata, message):
    print(message.topic)
    client.publish(message.topic, None, qos=0, retain=True)

if __name__ == '__main__':
    client = mqtt.Client()
    client.connect('iot.eclipse.org', 1883)
    client.on_message = on_receive
    client.subscribe('/biscuit/#')
    client.loop_forever()