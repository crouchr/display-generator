import json
import time

import get_env

# artifacts (metfuncs)
import mean_sea_level_pressure

# Pure meteorology based
def process_in_msg(client, display_topic, mqtt_dict):
    msg = {}

    site_height_m = 50
    alert_str = '*'

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

    # Testing variables
    # temp_c = -1
    # rrate = 3.3
    # beaufort = 'F6'

    # Burt says to record pressure adjusted to MSL (Mean Sea Level)
    pressure = round(float(pressure_absolute), 1)
    pressure = pressure + mean_sea_level_pressure.msl_k_factor(site_height_m, temp_c)

    if presstrendval > 0:
        presstrend_str = 'R'
    elif presstrendval < 0:
        presstrend_str = 'F'
    else:
        presstrend_str = 'S'

    if beaufort == 'F0':
        wind_str = 'F0'
    else:
        wind_str = beaufort.__str__() + ' ' + wdir.__str__()

    # ALERTS
    if temp_c < 0:
        alert_str += 'FREEZE+'
    if int(beaufort.replace('F', '')) >= 5:
        alert_str += 'WIND+'
    if rrate > 0:
        alert_str += 'RAIN+'
    alert_str = alert_str.rstrip('+')
    alert_str += '*'

    # if no alerts, then display local time
    if alert_str == '**':
        alert_str = time.ctime()

    line_pressure = 'Barometer:' + pressure.__str__() + \
                   ' ' + presstrend_str

    line_metrics = temp_c.__str__() + 'C' +\
                   ' ' + humidity.__str__() + '%' + \
                   ' ' + rrate.__str__() + \
                   ' ' + wind_str

    line_fcast = 'Forecast:' + forecast
    line_fcast = forecast
    # line_alert = 'Rain in 34 minutes...'
    line_alert = alert_str

    display_text = [line_pressure, line_metrics, line_fcast, line_alert]

    msg['msg_type'] = 'DISPLAY_DATA'
    msg['publisher'] = get_env.get_mqtt_name()
    msg['version'] = version
    msg['display_text'] = display_text
    msg['beep'] = 0

    jsonString = json.dumps(msg)

    # print('simulate sent to display_topic=' + display_topic)
    print(jsonString)
    client.publish(display_topic, jsonString)