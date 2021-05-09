import json
import time

import get_env
import get_env_app
import definitions

# artifacts (metfuncs)
import mean_sea_level_pressure
import wind_calibration
import metfuncs

# dew_point and  wet_bulb calculations
import temp_derived_values
import simple_fog
import cloud_base

import ptendency
import moving_list

Forecasts = moving_list.MovingList(7)   # make 7 an env var
LastForecast = '---'


def log_display_to_file(pressure_msl, presstrend_str, presstrendval,
                        cumulus_forecast, pressure_forecast,
                        temp_c, dew_point, humidity,
                        rrate, beaufort, wdir, winddeg, gust,
                        is_lightning_possible_str,
                        fog_str,
                        line_pressure,
                        line_metrics1, line_metrics2, line_metrics3, line_metrics4, line_metrics5, line_metrics6,
                        alert_str):
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
    log_filename = definitions.DISPLAY_ROOT + '/' + 'ptendency.tsv'
    log_rec = time.ctime() + '\t' + \
        pressure_msl.__str__() + '\t' + \
        presstrend_str + presstrendval.__str__() + '\t' + \
        pressure_forecast + '\t' + \
        temp_c.__str__() + '\t' + \
        dew_point.__str__() + '\t' + \
        humidity.__str__() + '\t' + \
        rrate.__str__() + '\t' + \
        beaufort.__str__() + '\t' + \
        gust.__str__() + '\t' + \
        wdir + '\t' + \
        winddeg.__str__() + '\t' + \
        is_lightning_possible_str.__str__() + '\t' + \
        fog_str.__str__() + '\t' + \
        '"' + line_pressure + '"' + '\t' + \
        '"' + line_metrics1 + '"' + '\t' + \
        '"' + line_metrics2 + '"' + '\t' + \
        '"' + line_metrics3 + '"' + '\t' + \
        '"' + line_metrics4 + '"' + '\t' + \
        '"' + line_metrics5 + '"' + '\t' + \
        '"' + line_metrics6 + '"' + '\t' + \
        alert_str + '\t' + \
        cumulus_forecast + '\t' + \
        '\n'

    fp_out = open(log_filename, 'a')
    fp_out.write(log_rec)
    fp_out.close()

    print(log_rec.rstrip())

    return


# Pure meteorology based
def process_in_msg(client, display_topic, mqtt_dict):
    msg = {}
    global LastForecast

    site_height_m = 50
    alert_str = '*'

    version = get_env.get_version()

    vane_height_m = get_env_app.get_vane_height_m()
    wind_speed_multiplier = wind_calibration.calc_vane_height_to_10m_multiplier(vane_height_m)

    # The fundamental metrics
    pressure_absolute = mqtt_dict['pressure']
    temp_c = mqtt_dict['temp']
    humidity = mqtt_dict['humidity']

    cumulus_forecast = mqtt_dict['zambretti_forecast']
    wdir = mqtt_dict['wdir']
    winddeg = mqtt_dict['winddeg']
    wind_knots = float(mqtt_dict['wspeed'])     # averaged over 10 mins
    gust_knots = float(mqtt_dict['wgust'])     # averaged over 10 mins
    rrate = mqtt_dict['rrate']
    presstrendval = mqtt_dict['presstrendval']
    # beaufort = mqtt_dict['beaufort']
    # dew_point_cumulus = mqtt_dict['dew']

    wind_knots_corrected = round(wind_speed_multiplier * wind_knots, 1)
    wind_speed_corrected_kph = metfuncs.knots_to_kph(wind_knots_corrected)
    beaufort_corrected = 'F' + metfuncs.kph_to_beaufort(wind_speed_corrected_kph).__str__()

    gust_knots_corrected = round(wind_speed_multiplier * gust_knots, 1)
    gust_corrected_kph = metfuncs.knots_to_kph(gust_knots_corrected)
    gust_corrected = 'F' + metfuncs.kph_to_beaufort(gust_corrected_kph).__str__()

    cloud_base_ft = cloud_base.calc_cloud_base_ft(temp_c, humidity)
    print('cloud_base_ft=' + cloud_base_ft.__str__())

    dew_point_c = temp_derived_values.get_dew_point(temp_c, humidity)
    print('dew_point_c (derived)=' + dew_point_c.__str__())
    # print('dew_point_cumulus=' + dew_point_cumulus.__str__())

    # see https://www.weather.gov/source/zhu/ZHU_Training_Page/thunderstorm_stuff/Thunderstorms/thunderstorms.htm
    if dew_point_c >= 12:
        is_lightning_possible_str = 'LTNG?'
    else:
        is_lightning_possible_str = 'NO_LTNG'

    wet_bulb_c = temp_derived_values.get_wet_bulb(temp_c, pressure_absolute, dew_point_c)

    fog_possible = simple_fog.fog_algo_yocto(temp_c, dew_point_c, wet_bulb_c, humidity, permitted_range=0.1)
    if fog_possible:
        fog_str = 'FOG?'
    else:
        fog_str = 'NO_FOG'

    sunrise = '07:02'
    sunset = '21:29'

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

    if beaufort_corrected == 'F0':
        wind_str = 'F0'
    else:
        wind_str = beaufort_corrected + '>' + gust_corrected.lstrip('F') + ' ' + wdir.__str__()

    # ALERTS
    if temp_c < 0:
        alert_str += 'FREEZE+'
    if int(gust_corrected.replace('F', '')) >= 5:
        alert_str += 'WIND+'
    if rrate > 0:
        alert_str += 'RAIN+'
    alert_str = alert_str.rstrip('+')
    alert_str += '*'

    # if no alerts, then display local time
    if alert_str == '**':
        alert_str = 'No Alerts'

    tendency, pressure_forecast = ptendency.get_tendency(presstrendval)
    print('pressure_forecast=' + pressure_forecast)
    print('tendency=' + tendency)
    # Choose the mode (most common) of the last n values of the pressure_forecast
    Forecasts.add(pressure_forecast)
    print('Forecasts=' + Forecasts.get_values().__str__())
    most_common_forecast = Forecasts.get_most_common()
    print('most_common_forecast=' + most_common_forecast)
    print('LastForecast=' + LastForecast)
    if most_common_forecast != LastForecast:
        forecast_changed_str = '*'
    else:
        forecast_changed_str = ''

    # forecast in UPPER CASE implies it is STABLE
    all_same = Forecasts.all_same_value()
    if all_same:
        most_common_forecast_display = most_common_forecast.upper()
    else:
        most_common_forecast_display = most_common_forecast.lower()

    line_pressure = pressure_msl.__str__() + \
                   ' ' + presstrend_str + presstrendval.__str__() + ' ' + forecast_changed_str + most_common_forecast_display

    line_metrics1 = temp_c.__str__() + 'C' +\
                   ' ' + dew_point_c.__str__() + 'C' +\
                    ' ' + humidity.__str__() + '%'

    line_metrics2 = 'Twb=' + wet_bulb_c.__str__() + 'C'

    line_metrics3 = 'Cbase=' + cloud_base_ft.__str__() + ' ft'

    line_metrics4 = 'r=' + sunrise + ' ' + 's=' + sunset

    line_metrics5 = fog_str + \
                   ' ' + is_lightning_possible_str

    line_metrics6 = rrate.__str__() + \
                   ' ' + wind_str

    line_fcast = cumulus_forecast
    line_alert = alert_str
    line_time = time.ctime()    # TODO - strip the seconds and leading space

    display_text = [line_pressure,
                    line_metrics1, line_metrics2, line_metrics3, line_metrics4, line_metrics5, line_metrics6,
                    line_alert, line_fcast, line_time]

    log_display_to_file(pressure_msl, presstrend_str, presstrendval,
                        cumulus_forecast, pressure_forecast,
                        temp_c,
                        dew_point_c,
                        humidity, rrate,
                        beaufort_corrected, wdir, winddeg, gust_corrected,
                        is_lightning_possible_str,
                        fog_str,
                        line_pressure,
                        line_metrics1,
                        line_metrics2,
                        line_metrics3,
                        line_metrics4,
                        line_metrics5,
                        line_metrics6,
                        alert_str)

    msg['msg_type'] = 'DISPLAY_DATA'
    msg['publisher'] = get_env.get_mqtt_name()
    msg['version'] = version
    msg['display_text'] = display_text
    msg['beep'] = 0

    jsonString = json.dumps(msg)

    print(jsonString)
    client.publish(display_topic, jsonString)

    LastForecast = most_common_forecast
