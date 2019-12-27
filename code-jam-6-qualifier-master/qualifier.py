import datetime
import re
import time


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

    my_time = []
    #print(my_time)
    for result in year, month, day, hour, minute, second:
        if result != None:
            my_time.append(int(result))
        else:
            my_time.append(0)
    #print(my_time)
    max_time = [9999, 12, 31, 23, 59, 59]
    for time in range(len(my_time)):
        if my_time[time] > max_time[time]:
            raise ValueError("Input timestamp is not valid. " + str(my_time[time])
             + " > " + str(max_time[time]))

    time_str = ""
    for time in range(len(my_time)):
        time_str += str(my_time[time]) + ","
    #print(time_str)

    # print("Year: " + str(year) + "\n"
    #       "Month: " + str(month) + "\n"
    #       "Day: " + str(day) + "\n"
    #       "Hour: " + str(hour) + "\n"
    #       "Minute: " + str(minute) + "\n"
    #       "Second: " + str(second)
    # )
    my_dt = datetime.datetime(my_time[0], my_time[1], my_time[2], my_time[3],
                            my_time[4], my_time[5])
    #print(my_dt)
    return my_dt


test_string = input("Enter a timestamp: ")
parse_iso8601(test_string)
#add functionality to check for valid date, timestamp

#add fractional seconds
