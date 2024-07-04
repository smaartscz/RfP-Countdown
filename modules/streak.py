import modules.configuration as configuration
from modules.f_time import get_time

def increase():
    current_streak = int(configuration.get_value(section="Statistics", key="streak"))
    new_streak = int(current_streak) + 1
    if new_streak >= current_streak:
        configuration.save(section="Statistics",key="highest_streak", value=str(new_streak))
        configuration.save(section="Statistics",key="highest_streak_date", value=get_time())
    configuration.save(section="Statistics",key="streak", value=str(new_streak))
    configuration.save(section="Statistics",key="last_ping", value=get_time())

def reset():
    configuration.save(section="Statistics", key="streak", value="0")