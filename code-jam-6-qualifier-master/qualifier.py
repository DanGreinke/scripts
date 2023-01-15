import datetime
import re
import time
from datetime import timedelta, tzinfo


def parse_iso8601(timestamp: str) -> datetime.datetime:
    """Parse an ISO-8601 formatted time stamp."""
    regexp = re.compile(r"(?P<year>\d{4})"
                        r"-?"
                        r"(?P<month>\d{2})"
                        r"-?"
                        r"(?P<day>\d{2})"
                        r"T?"
                        r"(?P<hour>\d{2})?"
                        r":?"
                        r"(?P<minute>\d{2})?"
                        r":?"
                        r"(?P<second>\d{2})?"
                        r"(?P<microsec>.\d+)?"
                        r"(?P<tz_hour>(Z|(\+|-)\d{2}))?"
                        r":?"
                        r"(?P<tz_minute>\d{2})?"
                        )

    result = regexp.search(timestamp)
    if result == None:
        raise ValueError("Input value is not a timestamp")
    else:
        year = result.group('year') #returns string
        month = result.group('month')
        day = result.group('day')
        hour = result.group('hour')
        minute = result.group('minute')
        second = result.group('second')
        microsec = result.group('microsec')
        if microsec != None:
            if len(microsec) < 7:
                microsec += ("0" * (6 - len(microsec)))
            else:
                microsec_list = list(microsec)
                microsec_list[6:] = []
                microsec = "".join(microsec_list)

        tz_hour = result.group('tz_hour')
        if tz_hour != None:
            if tz_hour == 'Z':
                tz_hour = 0
            else:
                tz_hour = int(tz_hour)

        tz_minute = result.group('tz_minute')
        if tz_minute != None:
            if tz_hour < 0:
                tz_minute = int(tz_minute) * -1
            else:
                tz_minute = int(tz_minute)
        elif tz_hour != None and tz_minute == None:
            tz_minute = 0

        if tz_hour != None:
            tz_delta = datetime.timezone(timedelta(hours=tz_hour, minutes=tz_minute))
        else:
            tz_delta = None

    my_time = []
    #print(my_time)
    for result in year, month, day, hour, minute, second, microsec:
        if result != None:
            my_time.append(int(result))
        else:
            my_time.append(0)
    #print(my_time)
    max_time = [9999, 12, 31, 23, 59, 59, 999999]
    for time in range(len(my_time)):
        if my_time[time] > max_time[time]:
            raise ValueError("Input timestamp is not valid. " + str(my_time[time])
             + " > " + str(max_time[time]))

    my_dt = datetime.datetime(my_time[0], my_time[1], my_time[2], my_time[3],
                            my_time[4], my_time[5], my_time[6], tzinfo=tz_delta)
    print(my_dt)
    return my_dt


test_string = input("Enter a timestamp: ")
parse_iso8601(test_string)

#add timezone support
