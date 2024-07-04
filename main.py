import modules.configuration as configuration
import modules.discord as discord
from modules.basic import clear
import modules.colors as colors
import modules.streak as streak
import os, schedule, time
import modules.web as web
import threading

if os.name != "nt":
     os.environ.get("TERM")
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

#Start Web UI
print(colors.yellow + "Starting web" + colors.reset)
web_thread = threading.Thread(target=web.start)
web_thread.daemon = True  # Daemonize thread to exit when main thread exits
web_thread.start()

#Send startup message
discord.send_webhook(type="startup", gif_url=startup_gif)

#Setup schedule
print(colors.yellow + "Setting up schedule!"+ colors.reset)
schedule.every().day.at(scheduled_time).do(discord.prepare_webhook)

#Reset streak
streak.reset()

print(colors.green + "Startup successful!" + colors.reset)

while True:
     schedule.run_pending()
     time.sleep(10)  # Sleep to avoid high CPU usage
