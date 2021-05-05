# CRHUDA model https://www.researchgate.net/publication/337236701_Algorithm_to_Predict_the_Rainfall_Starting_Point_as_a_Functio
def get_chruda_metrics(s1_m_avg, s2_m_avg, humidity, pressure, dew_point_c, rain_rate, rain_k_factor):

    if dew_point_c < 1.0:
        crhuda_dew = 1.0
    else:
        crhuda_dew = dew_point_c

    s1 = humidity
    s2 = round(rain_k_factor * (pressure / crhuda_dew), 1)
    if s2 > 150.0:
        s2 = 150.0

    s1_m_avg.add(s1)
    s2_m_avg.add(s2)

    s1_avg = s1_m_avg.get_moving_average()
    s2_avg = s2_m_avg.get_moving_average()

    # in phase waiting for S2 to increase and cross S1
    if s2_avg < s1_avg:
        crhuda_primed = 10.0
    else:
        crhuda_primed = 0.0

    if rain_rate > 0.0:
        crhuda_rain = 15  # if any rain then indicate this on graph - not interested in rain intensity
    else:
        crhuda_rain = 0
    # end of CRHUDA model

    return s1_avg, s2_avg, crhuda_primed, crhuda_rain
