
# forecast can only be 8 chars or less
def get_tendency(pressure_trend):
    """
    Return a string describing predicted weather based on pressure (mb) trend in last 3 hours
    See 'Weather at Sea' book  page 36
    :param pressure_trend:
    :return:
    """
    forecast = 'None'

    # If pressure is steady or rising then simplify to 'Fair' weather
    # Possibly more info needed - what if pressure is rapidly rising ?
    if pressure_trend >= 0.1:
        tendency = 'r'     # Rising
        forecast = 'Fair'
        return tendency, forecast
    elif pressure_trend > -0.1:
        tendency = 's'
        forecast = 'Settled'
        return tendency, forecast

    if pressure_trend <= -0.1 and pressure_trend > -1.5:
        tendency = 'f'
        forecast = 'Change'
    elif pressure_trend <= -1.5 and pressure_trend > -3.5:
        tendency = 'F'
        forecast = 'F6-7 12h'
    elif pressure_trend <= -3.5 and pressure_trend > -6.0:
        tendency = 'F!'
        forecast = 'F6-8 6h'
    elif pressure_trend <= - 6.0:
        tendency = 'F!!'
        forecast = 'F7-9 3h'
    else:
        tendency = 'ERROR'
        forecast = 'ERROR'






    return tendency, forecast
