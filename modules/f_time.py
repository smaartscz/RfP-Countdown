from datetime import datetime
from time import time
import math
import modules.logs as logs

def get_time():
    return str(datetime.now())

def remaining_time(unix_time):
    #Get remaining time
    current_time = int(time())
    remaining_time = int(unix_time) - current_time

    #Get remaining days, hours and seconds
    fdays = remaining_time / (24 * 60 * 60)
    days = math.ceil(fdays)
    remaining_seconds = remaining_time % (24 * 60 * 60)
    hours = remaining_seconds // (60 * 60)
    logs.logger.debug(f"Calculating remaining time. Args: unix_time: {unix_time}, current_time: {current_time}, remaining_time: {remaining_time}, fdays: {fdays}, days: {days}, hours: {hours}, remaining_seconds: {remaining_seconds} ")
    return days, hours
