import modules.colors as colors
import modules.discord as discord
import modules.configuration as configuration
import schedule
scheduled_job = None

def update(time="None"):
    global scheduled_job
    print(colors.yellow + "Setting up schedule!" + colors.reset)

    #Get time if value is None
    if time == "None":
        time = configuration.get_value("General", "ping_at")

    #Remove old job
    if scheduled_job:
        print(colors.red + f"Canceling existing scheduled job: {scheduled_job}" + colors.reset)
        schedule.cancel_job(scheduled_job)

    scheduled_job = schedule.every().day.at(time).do(discord.prepare_webhook)
    print(colors.green + f"Scheduled job set for {time}: {scheduled_job}" + colors.reset)