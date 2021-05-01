import json
import time

import get_env

# artifacts (metfuncs)
import mean_sea_level_pressure

# Pure meteorology based
def process_in_msg(client, display_topic, mqtt_dict):
    msg = {}

    site_height_m = 50

    version = get_env.get_version()
    temp_c = mqtt_dict['temp']
    forecast = mqtt_dict['zambretti_forecast']
    pressure_absolute = mqtt_dict['pressure']
    dew_point = mqtt_dict['dew']
    humidity = mqtt_dict['humidity']
    beaufort = mqtt_dict['beaufort']
    wdir = mqtt_dict['wdir']
    rrate = mqtt_dict['rrate']
    presstrendval = mqtt_dict['presstrendval']

    # Burt says to record pressure adjusted to MSL (Mean Sea Level)
    pressure = round(float(pressure_absolute), 1)
    pressure = pressure + mean_sea_level_pressure.msl_k_factor(site_height_m, temp_c)

    line_local_time = time.ctime()
    line_metrics = 'pressure:' + pressure.__str__() + ' mbar' + \
                   ' (' + presstrendval.__str__() + ')'\
                   ' temp:' + temp_c.__str__() + \
                   ' humidity:' + humidity.__str__() + \
                   ' dew:' + dew_point.__str__() + \
                   ' wind:' + beaufort.__str__() + \
                   ' from ' + wdir.__str__() + \
                   ' rain:' + rrate.__str__() + ' mm/h'
    line_fcast = forecast
    line_alert = 'Rain in 34 minutes...'

    display_text = [line_local_time, line_metrics, line_fcast, line_alert]

    msg['display_text'] = display_text
    msg['mode'] = 'main'
    msg['version'] = version

    jsonString = json.dumps(msg)

    # print('simulate sent to display_topic=' + display_topic)
    print(jsonString)
    client.publish(display_topic, jsonString)