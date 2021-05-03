# https://techtutorialsx.com/2017/04/14/python-publishing-messages-to-mqtt-topic/
import time
import random
import paho.mqtt.client as mqttClient
import get_env_app
from pprint import pprint
import ast
import generate_display_text

# import moving_averages

# generate client ID with pub prefix randomly
client_id = f'display-generator-{random.randint(0, 100)}'
print('client_id=' + client_id.__str__())

Connected = False   # global variable for the state of the connection

# Pressure_m_avg = moving_averages.MovingAverage(5)


def connect_mqtt() -> mqttClient:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected to MQTT Broker OK")
        else:
            print("failed to connect !, return code %d\n", rc)

    broker_host = get_env_app.get_mqttd_host()
    broker_port = get_env_app.get_mqttd_port()

    print('broker_host=' + broker_host.__str__())
    print('broker_port=' + broker_port.__str__())

    client = mqttClient.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker_host, broker_port)

    return client

# common funcs
def on_connect(client, userdata, flags, rc):
    # print('entered on_connect()')
    if rc == 0:
        print(time.ctime() + " : connected to MQTT Broker OK")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("connection to MQTT Broker failed !")


# subscribe to Cumulus Topic to read forecast
def subscribe(client: mqttClient):
    def on_message(client, userdata, msg):
        # print('entered on_message()')
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # print(msg.payload.decode())
        mqtt_dict = ast.literal_eval(msg.payload.decode())
        pprint(mqtt_dict)
        display_topic = get_env_app.get_display_topic()
        generate_display_text.process_in_msg(client, display_topic, mqtt_dict)

    cumulus_topic = get_env_app.get_cumulus_topic()
    # print('cumulus_topic=' + cumulus_topic.__str__())
    client.subscribe(cumulus_topic)
    client.on_message = on_message


def main():
    # broker_host = get_env_app.get_mqttd_host()
    # broker_port = get_env_app.get_mqttd_port()
    display_topic = get_env_app.get_display_topic()
    cumulus_topic = get_env_app.get_cumulus_topic()

    # print('broker_host=' + broker_host.__str__())
    # print('broker_port=' + broker_port.__str__())

    print('display_topic=' + display_topic.__str__())
    print('cumulus_topic=' + cumulus_topic.__str__())

    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    main()