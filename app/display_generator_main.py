# https://techtutorialsx.com/2017/04/14/python-publishing-messages-to-mqtt-topic/

import random
import paho.mqtt.client as mqttClient
import get_env_app
from pprint import pprint
import ast
import generate_weather_display_text
import mqtt_client


# subscribe to Cumulus Topic to read forecast
def subscribe(client: mqttClient):
    def on_message(client, userdata, msg):
        """
        Code that gets performed when a new message is received in the Topic
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        # print('entered on_message()')
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # print(msg.payload.decode())
        mqtt_dict = ast.literal_eval(msg.payload.decode())
        pprint(mqtt_dict)

        # ******** SPECIFIC CODE ********************************
        display_topic = get_env_app.get_display_topic()
        generate_weather_display_text.process_in_msg(client, display_topic, mqtt_dict)
        # *******************************************************


    cumulus_topic = get_env_app.get_cumulus_topic()
    # print('cumulus_topic=' + cumulus_topic.__str__())
    client.subscribe(cumulus_topic)
    client.on_message = on_message


def main():

    display_topic = get_env_app.get_display_topic()
    cumulus_topic = get_env_app.get_cumulus_topic()

    print('display_topic=' + display_topic.__str__())
    print('cumulus_topic=' + cumulus_topic.__str__())

    # generate client ID with pub prefix randomly
    client_id = f'display-generator-{random.randint(0, 100)}'
    print('client_id=' + client_id.__str__())

    client = mqtt_client.connect_mqtt(client_id)
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    main()