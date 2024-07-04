from discord_webhook import DiscordWebhook, DiscordEmbed
import modules.configuration as configuration
import modules.colors as colors
from modules.f_time import remaining_time, get_time
import modules.streak as streak
def send_webhook(type="None", days=0, gif_url="None", unix_time="None"):
    role = configuration.get_value("General", "role_id")
    webhook_url = configuration.get_value("General", "webhook")
    unix_time = configuration.get_value("RockForPeople", "unix_date")
    #Create new instance

    #Startup message
    if type == "startup":
        webhook = DiscordWebhook(url=webhook_url, content=f'<:peepoHey:925562717778104321>📣 ZDENOOOOOOOOOOOOOO')
        with open(f"gifs/{type}.gif", "rb") as f:
            webhook.add_file(file=f.read(), filename="startup.gif")
        response = webhook.execute()
        print(colors.green + f"Webhook sent! Response: {response}" + colors.reset)
        return
    
    #Countdown message
    if type == "countdown":
        if gif_url != None:
            if gif_url == "gif":
                if days == 0:
                    message = f'PRÁVĚ TO VŠECHNO ZAČÍNÁ <@&{role}> **ENJOY** (Podle discordu: <t:{unix_time}:R>)'
                else:
                    message = f'Dobré FUCKIN poledne!<:LETSFUCKINGGOOO:917692819320233994> <@&{role}> je za {days} dní. (Podle discordu: <t:{unix_time}:R>)'
                webhook = DiscordWebhook(url=webhook_url, content=message)
                with open(f"gifs/{days}.{gif_url}", "rb") as f:
                    webhook.add_file(file=f.read(), filename=f"{days}.{gif_url}")
                response = webhook.execute() 
                print(colors.green + f"Webhook sent! Response: {response}" + colors.reset)
        else:
            message = f'Dobré poledne a dobrou chuť, <@&{role}> je za {days} dní. (Podle discordu: <t:{unix_time}:R>)'
            webhook = DiscordWebhook(url=webhook_url, content=message)  

            #Send webhook
            response = webhook.execute()
            print(colors.green + f"Webhook sent! Response: {response}" + colors.reset)
            if str(response) == "<Response [200]>":
                streak.increase()
            else:
                print(colors.red + f"Error sending webhook. Error: {response}" + colors.reset)

def prepare_webhook():
    #Load RfP date
    unix_date = configuration.get_value("RockForPeople","unix_date")

    #Calculate days until event
    days, hours = remaining_time(unix_time=unix_date)
    print(colors.yellow + f"Remaining days: {days}" + colors.reset)
    
    #Check if there are any gif
    gif_url = configuration.get_value("SpecialDays", str(days))

    #Get color based if its today or no
    print(colors.yellow + "Sending webhook!" + colors.reset)
    send_webhook(type="countdown", days=days, gif_url=gif_url, unix_time=unix_date)