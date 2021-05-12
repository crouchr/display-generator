# See https://www.yoctopuce.com/EN/products/yocto-meteo-v2/doc/METEOMK2.usermanual.html#CHAP5SEC1

from yoctopuce.yocto_humidity import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_pressure import *


# SerialNumber: METEOMK2-18FD45
def register_meteo2_sensor(target='any'):
    try:
        print('entered register_meteo2_sensor()')

        errmsg = YRefParam()

        # Setup the API to use local USB devices
        if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
            msg = "Error : Meteo sensor init error : " + errmsg.value
            print(msg)
            return None, None, None, msg

        if target == 'any':
            # retrieve any sensor
            hum_sensor = YHumidity.FirstHumidity()
            if hum_sensor is None:
                msg = 'Error : check Meteo sensor USB cable'
                print(msg)
                return None, None, None, msg
        else:
            hum_sensor = YHumidity.FindHumidity(target + '.humidity')
            press_sensor = YPressure.FindPressure(target + '.pressure')
            temp_sensor = YTemperature.FindTemperature(target + '.temperature')

        if not (hum_sensor.isOnline()):
            msg = 'Error : Meteo sensor not connected'
            print(msg)
            return None, None, None, msg

        print('Meteo sensor registered OK')
        return hum_sensor, press_sensor, temp_sensor, 'Meteo sensor registered OK'

    except Exception as e:
        print(e.__str__())
        YAPI.FreeAPI()
        return None, None, None, e.__str__()


def get_meteo_values(hum_sensor, press_sensor, temperature_sensor):
    """

    :param hum_sensor:
    :param press_sensor:
    :param temperature_sensor:
    :return:
    """

    if hum_sensor.isOnline():
        humidity = hum_sensor.get_currentValue()
        pressure = press_sensor.get_currentValue()
        temperature = temperature_sensor.get_currentValue()
    else:
        humidity = None
        pressure = None
        temperature = None

    return humidity, pressure, temperature


# Simple test loop
if __name__ == '__main__':
    hum_sensor, temperature_sensor, press_sensor, status_msg = register_meteo2_sensor()
    if status_msg != 'Meteo sensor registered OK':
        sys.exit('Exiting, unable to register Meteo sensor')

    while True:
        humidity, pressure, temperature = get_meteo_values(hum_sensor, press_sensor, temperature_sensor)
        print('humidity=' + humidity.__str__())
        print('pressure=' + pressure.__str__())
        print('temperature=' + temperature.__str__())
        time.sleep(15)
