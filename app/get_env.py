# common environment non-specific to this app
# This file can be used in other metminiwx projects

import os


def get_version():
    if 'VERSION' in os.environ:
        version = os.environ['VERSION']
    else:
        version = 'IDE-1.0.0'       # i.e. running in PyCharm

    return version


def get_verbose():
    if 'VERBOSE' in os.environ:
        verbose = os.environ['VERBOSE']
        if verbose == 'True':
            verbose = True
        else:
            verbose = False
    else:
        verbose = False

    return verbose


def get_stage():
    if 'STAGE' in os.environ:
        stage = os.environ['STAGE']
    else:
        stage = 'DEV'               # i.e. running in PyCharm

    return stage


def get_mqtt_name():
    '''
    Added to MQTT messages
    :return:
    '''
    if 'MQTT_NAME' in os.environ:
        mqtt_name = os.environ['MQTT_NAME']
    else:
        mqtt_name = 'DISPLAY_GENERATOR'               # i.e. running in PyCharm

    return mqtt_name
