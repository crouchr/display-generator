# common environment non-specific to this app
# This file can be used in other metminiwx projects


# Use j1900 for live
def get_mqttd_host():
    """
    Determine the hostname that hosts the MQTT Daemon
    :return:
    """
    # if 'STAGE' in os.environ and os.environ['STAGE'] == 'PRD':
    #     mqttd_host = 'j1900'
    # # elif 'STAGE' in os.environ and os.environ['STAGE'] == 'TEST':
    # #     mqttd_host = 'mr-dell'
    # else:
    mqttd_host = 'j1900'

    return mqttd_host


def get_mqttd_port():
    mqttd_port = 1883

    return mqttd_port


def get_display_topic():
    """
    CumulusMX writes data to this topic
    :return:
    """
    topic = "MetminiWX/Display"

    return topic


def get_cumulus_topic():
    """
    CumulusMX writes data to this topic
    :return:
    """
    topic = "CumulusMX/Interval"

    return topic
