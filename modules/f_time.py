from datetime import datetime
from time import time

def get_time():
    return str(datetime.now())

def remaining_time(unix_time):
    #Get remaining time
    current_time = int(time())
    remaining_time = int(unix_time) - current_time

    #Get remaining days, hours and seconds
    days = remaining_time // (24 * 60 * 60)
    remaining_seconds = remaining_time % (24 * 60 * 60)
    hours = remaining_seconds // (60 * 60)

    return days, hours
