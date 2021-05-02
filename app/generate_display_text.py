import json
import time

import get_env

# artifacts (metfuncs)
import mean_sea_level_pressure

import ptendency


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
    pressure_msl = round(pressure_absolute + mean_sea_level_pressure.msl_k_factor(site_height_m, temp_c), 1)

    if presstrendval > 0:
        presstrend_str = '+'
    else:
        presstrend_str = ''

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
        alert_str = time.ctime() # TODO - strip the seconds and leading space

    tendency, pressure_forecast = ptendency.get_tendency(presstrendval)

    line_pressure = pressure_msl.__str__() + \
                   ' ' + presstrend_str + presstrendval.__str__() + ' ' + pressure_forecast

    line_metrics = temp_c.__str__() + 'C' +\
                   ' ' + humidity.__str__() + '%' + \
                   ' ' + rrate.__str__() + \
                   ' ' + wind_str

    line_fcast = 'Z:' + forecast
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