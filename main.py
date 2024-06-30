import modules.configuration as configuration
import modules.discord as discord
from modules.f_time import get_time
from modules.basic import clear
import modules.colors as colors

import os, schedule, time, sys

if os.name != "nt":
     os.environ.get("TERM")

print("PoC" + get_time())

clear()
# Check if config already exists or it's first time running this app
if not os.path.isfile("config.cfg"):
     print(colors.red + "Running for first time! Creating new config" + colors.reset)
     configuration.create()


#Load config and set up schedule
print(colors.yellow + "Loading configuration!" + colors.reset)
config = configuration.load()
scheduled_time = configuration.get_value("General", "ping_at")
startup_gif = configuration.get_value("General", "startup")
print(colors.green + "Configuration loaded!" + colors.reset)

#Send startup message
discord.send_webhook(type="startup", gif_url=startup_gif)

#Setup schedule
print(colors.yellow + "Setting up schedule!"+ colors.reset)
schedule.every().day.at(scheduled_time).do(discord.prepare_webhook)


print(colors.green + "Startup successful!" + colors.reset)
discord.prepare_webhook()
while True:
     schedule.run_pending()
     time.sleep(1)  # Sleep to avoid high CPU usage
