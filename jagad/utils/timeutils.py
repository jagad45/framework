import time
from datetime import datetime

FORMAT_GET_TIME = "%H:%M:%S"
FORMAT_CALENDAR = "%d/%m/%Y"
FORMAT_FULL     = f"{FORMAT_CALENDAR} {FORMAT_GET_TIME}"

def calculate_time(current_time, toRound = False, toInt = False, toFloat = True):
    end_time = get_timestamp()
    if toRound is True:
        return round(end_time - current_time)
    elif toInt is True:
        return int(end_time - current_time)
    elif toFloat is True:
        return float(end_time - current_time)
    else:
        result = end_time - current_time
        return result

def get_timestamp():
    return time.time()

def get_timenow(__format=FORMAT_GET_TIME):
    now = datetime.now()
    return now.strftime(__format)
