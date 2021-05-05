# common environment non-specific to this app
# This file can be used in other metminiwx projects
import os

# Use j1900 for live
def get_mqttd_host():
    """
    Determine the hostname that hosts the MQTT Daemon
    :return:
    """
    if 'STAGE' in os.environ and os.environ['STAGE'] == 'PRD':
        mqttd_host = 'mqttd'    # name of container
    else:
        mqttd_host = 'j1900'    # IP of mqttd

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


# Actual wind vane height to allow for multiplier
def get_vane_height_m():
    if 'VANE_HEIGHT' in os.environ:
        vane_height = os.environ['VANE_HEIGHT']
    else:
        vane_height = 3.7       # value in Ermin Street

    return vane_height
