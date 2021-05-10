# https://www.daniweb.com/programming/software-development/code/216727/moon-phase-calculator
# Determine the moon phase of a date given
# Python code by HAB

# web-site calculator : https://www.timeanddate.com/moon/phases/uk/witney

import time

# What Tide Corresponds With a Solar Eclipse?
#
# Ocean tides are caused by the complex interplay of three astronomical bodies: the Sun, the Earth and the Moon.
# Both the Sun and the Moon exert a gravitational pull on the Earth's water.
# The resulting force of the Moon's gravity creates two tidal bulges on opposite sides of the Earth.
# Depending on the relative position of the Sun, the tidal bulges will change slightly as the Moon experiences its phases.

# Full Moon and New Moon
# At both full moon and new moon, tides are at their most drastic.
# High tides are very high, and low tides are very low.
# At full moon, the Moon and Sun are in a straight line on opposite sides of the Earth.
# Their gravitational forces combine to create larger tidal bulges. At new moon, the Moon and Sun are in a straight line on the same side of the Earth.
# In this case, their gravitational forces still combine to create large tidal bulges.
# These situations are called spring tides.

# Quarter Moons
# At quarter moons, the Earth's tides are at their least drastic.
# When the Moon is at a quarter phase, it forms a right angle with the Sun (with the Earth at the vertex).
# The gravitational forces from each body act at perpendicular angles, diminishing the overall tidal bulge.
# The Moon is still exerting a stronger gravitational force than the Sun, so there is still a net tidal bulge.
# However, this bulge is at its smallest.
# These situations are called neap tides.


# https://www.programiz.com/python-programming/time
def get_moon_phase_now():
    # current_time = time.ctime()
    utc_epoch = time.time()
    # local_time = time.ctime(utc_epoch)
    time_struct = time.gmtime(utc_epoch)    # gm = UTC

    month = time_struct.tm_mon
    year = time_struct.tm_year
    day = time_struct.tm_mday

    _, status, light_percent = moon_phase(month, day, year)

    return status, light_percent


def moon_phase(month, day, year):
    ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
    # description = ["New Moon, spring tides",
    #                "Waxing crescent (increasing to full)",
    #                "First Quarter (increasing to full), neap tides",
    #                "Waxing gibbous (increasing to full)",
    #                "Full Moon, spring tides",
    #                "Waning gibbous (decreasing from full)",
    #                "Last Quarter (decreasing from full), neap tides",
    #                "Waning crescent (decreasing from full)"]
    description = ["New Moon, spring tides",
                   "Waxing crescent (increasing to full)",
                   "First Quarter (increasing to full), neap tides",
                   "Waxing gibbous (increasing to full)",
                   "Full Moon, spring tides",
                   "Waning gibbous (decreasing from full)",
                   "Last Quarter (decreasing from full), neap tides",
                   "Waning crescent (decreasing from full)"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if day == 31:
        day = 1
    days_into_phase = ((ages[(year + 1) % 19] + ((day + offsets[month - 1]) % 30) + (year < 1900)) % 30)
    index = int((days_into_phase + 2) * 16 / 59.0)
    if index > 7:
        index = 7
    status = description[index]

    # light should be 100% 15 days into phase
    light = int(2 * days_into_phase * 100 / 29)
    if light > 100:
        light = abs(light - 200)
    date = "%d %s %d" % (day, months[month - 1], year)

    return date, status, light


if __name__ == '__main__':
    # put in a date you want ...
    day = 23
    month = 5
    year = 2021     # use yyyy format

    date, status, light_percent = moon_phase(month, day, year)
    print("moon phase on %s is '%s', light = %d%s" % (date, status, light_percent, '%'))

    status, light_percent = get_moon_phase_now()
    print('moon status for now : status=' + status + ', light_percent=' + light_percent.__str__())
