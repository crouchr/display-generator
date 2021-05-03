import json
import time

import get_env
import get_env_app

# artifacts (metfuncs)
import mean_sea_level_pressure
import wind_calibration
import metfuncs

import ptendency


def log_display_to_file(pressure_msl, presstrend_str, presstrendval, pressure_forecast, temp_c, dew_point, humidity, rrate, beaufort, wdir, winddeg, alert_str):
    """
    Log the critical variables to file for analysis
    :param pressure_msl:
    :param presstrend_str:
    :param presstrendval:
    :param pressure_forecast:
    :param temp_c:
    :param dew_point:
    :param rrate:
    :param beaufort:
    :param wdir:
    :param alert_str:
    :return:
    """
    log_filename = 'ptendency.tsv'
    log_rec = time.ctime() + '\t' + \
        pressure_msl.__str__() + '\t' + \
        presstrend_str  + presstrendval.__str__() + '\t' + \
        pressure_forecast + '\t' + \
        temp_c.__str__() + '\t' + \
        dew_point.__str__() + '\t' + \
        humidity.__str__() + '\t' + \
        rrate.__str__() + '\t' + \
        beaufort.__str__() + '\t' + \
        wdir + '\t' + \
        winddeg.__str__() + '\t' + \
        alert_str + '\t' + \
        '\n'

    fp_out = open(log_filename, 'a')
    fp_out.write(log_rec)
    fp_out.close()

    print(log_rec)

    return


# Pure meteorology based
def process_in_msg(client, display_topic, mqtt_dict):
    msg = {}

    site_height_m = 50
    alert_str = '*'

    version = get_env.get_version()

    vane_height_m = get_env_app.get_vane_height_m()
    wind_speed_multiplier = wind_calibration.calc_vane_height_to_10m_multiplier(vane_height_m)


    temp_c = mqtt_dict['temp']
    forecast = mqtt_dict['zambretti_forecast']
    pressure_absolute = mqtt_dict['pressure']
    dew_point = mqtt_dict['dew']
    humidity = mqtt_dict['humidity']
    beaufort = mqtt_dict['beaufort']
    wdir = mqtt_dict['wdir']
    winddeg = mqtt_dict['winddeg']
    wind_knots = float(mqtt_dict['wspeed'])     # averaged over 10 mins
    rrate = mqtt_dict['rrate']
    presstrendval = mqtt_dict['presstrendval']

    wind_knots_corrected = round(wind_speed_multiplier * wind_knots, 1)
    wind_speed_corrected_kph = metfuncs.knots_to_kph(wind_knots_corrected)
    beaufort_corrected = 'F' + metfuncs.kph_to_beaufort(wind_speed_corrected_kph).__str__()

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

    line_metrics = temp_c.__str__() +\
                   ' ' + dew_point.__str__() + \
                   ' ' + rrate.__str__() + \
                   ' ' + wind_str

    line_fcast = forecast
    # line_alert = 'Rain in 34 minutes...'
    line_alert = alert_str

    display_text = [line_pressure, line_metrics, line_fcast, line_alert]

    log_display_to_file(pressure_msl, presstrend_str, presstrendval, pressure_forecast, temp_c, dew_point, humidity, rrate, beaufort_corrected, wdir, winddeg, alert_str)

    msg['msg_type'] = 'DISPLAY_DATA'
    msg['publisher'] = get_env.get_mqtt_name()
    msg['version'] = version
    msg['display_text'] = display_text
    msg['beep'] = 0

    jsonString = json.dumps(msg)

    # print('simulate sent to display_topic=' + display_topic)
    print(jsonString)
    client.publish(display_topic, jsonString)