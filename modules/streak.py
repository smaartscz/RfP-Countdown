import modules.configuration as configuration
from modules.f_time import get_time
import modules.colors as colors

def increase():
    print(colors.yellow + "Wow, good job! Increasing streak." + colors.reset)
    current_streak = int(configuration.get_value(section="Statistics", key="streak"))
    new_streak = int(current_streak) + 1
    if new_streak >= current_streak:
        configuration.save(section="Statistics",key="highest_streak", value=str(new_streak))
        configuration.save(section="Statistics",key="highest_streak_date", value=get_time())
    configuration.save(section="Statistics",key="streak", value=str(new_streak))
    configuration.save(section="Statistics",key="last_ping", value=get_time())

def reset():
    streak = int(configuration.get_value(section="Statistics", key="streak"))
    print(colors.red + f"Too bad! You have lost your streak of {streak} days." + colors.reset)
    configuration.save(section="Statistics", key="streak", value="0")