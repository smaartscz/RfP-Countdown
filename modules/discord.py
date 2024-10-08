from discord_webhook import DiscordWebhook, DiscordEmbed
import modules.configuration as configuration
import modules.colors as colors
from modules.f_time import remaining_time
import modules.streak as streak
import modules.logs as logs


def send_webhook(type="None", days=0, gif_url="None", unix_time="None", userid = "None", manual = False):
    role = configuration.get_value("General", "role_id")
    webhook_url = configuration.get_value("General", "webhook")
    unix_time = configuration.get_value("RockForPeople", "unix_date")
    type = type.lower()

    logs.logger.info("Starting discord webhook function")

    #Startup message
    if type == "startup":
        #Create Webhook class
        webhook = DiscordWebhook(url=webhook_url, content=f'<:peepoHey:925562717778104321>📣 ZDENOOOOOOOOOOOOOO')

        #Attach gif
        with open(f"gifs/{type}.gif", "rb") as f:
            webhook.add_file(file=f.read(), filename="startup.gif")

        #Send webhook
        response = webhook.execute()
        logs.logger.info(f"Webhook sent! Response: {response}. Args: type={type}")
        print(colors.green + f"Webhook sent! Response: {response}" + colors.reset)
        return
    
    #Manual ping
    if type == "user_ping":
        #Special message for manual ping
        message = f"Čau <@{userid}>! <a:rabbitvibe:1213174868669890601> Rock For People 2025 je za {days} dní. (Podle discordu: <t:{unix_time}:R>)"

        #Create Webhook class with message
        webhook = DiscordWebhook(url=webhook_url, content=message)  

        #Send webhook
        response = webhook.execute()
        logs.logger.info(f"Webhook sent! Response: {response}. Args: days={days}, type={type}, userId={userid}")
        print(colors.green + f"Webhook sent! Response: {response}" + colors.reset)
        return response
        
    #Countdown message
    if type == "countdown":
        if gif_url == "gif":

            #Special message for day 0
            if days == 0:
                message = f'PRÁVĚ TO VŠECHNO ZAČÍNÁ <@&{role}> **ENJOY** (Podle discordu: <t:{unix_time}:R>)'

            #Normal message
            else:
                message = f'Dobré FUCKIN poledne!<:LETSFUCKINGGOOO:917692819320233994> <@&{role}> je za {days} dní. (Podle discordu: <t:{unix_time}:R>)'

            #Create Webhook class with message
            webhook = DiscordWebhook(url=webhook_url, content=message)

            #Attach gif
            with open(f"gifs/{days}.{gif_url}", "rb") as f:
                webhook.add_file(file=f.read(), filename=f"{days}.{gif_url}")

            #Send webhook
            response = webhook.execute() 
            logs.logger.info(f"Webhook sent! Response: {response}. Args: days={days}, type={type}")
            print(colors.green + f"Webhook sent! Response: {response}" + colors.reset)
        else:

            #Normal message
            message = f'Dobré poledne a dobrou chuť, <@&{role}> je za {days} dní. (Podle discordu: <t:{unix_time}:R>)'

            #Create Webhook class with message
            webhook = DiscordWebhook(url=webhook_url, content=message)  

            #Send webhook
            response = webhook.execute()
            
            print(colors.green + f"Sending webhook!" + colors.reset)
        if(manual == False):
            #Check if sending was successful
            if str(response) == "<Response [200]>":
                streak.check(day=days)
                logs.logger.info(f"Webhook sent successfully! Response: {response}. Args: days={days}, type={type}")
                print(colors.green + f"Webhook sent! Response: {response}" + colors.reset)
            else:
                logs.logger.critical(f"Webhook sent! Response: {response}. Full details: {response.json()} Args: days={days}, type={type}")
                print(colors.red + f"Error sending webhook. Error: {response}, details: {response.json()}" + colors.reset)     
        return response

def prepare_webhook(manual=False):
    #Load RfP date
    unix_date = configuration.get_value("RockForPeople","unix_date")

    #Calculate days until event
    days, hours = remaining_time(unix_time=unix_date)
    print(colors.yellow + f"Remaining days: {days}" + colors.reset)
    
    #Check if there are any gif
    gif_url = configuration.get_value("SpecialDays", str(days))

    #Get color based if its today or no
    print(colors.yellow + "Sending webhook!" + colors.reset)
    if(manual):
        response = send_webhook(type="countdown", days=days, gif_url=gif_url, unix_time=unix_date, manual = True)
        return response
    send_webhook(type="countdown", days=days, gif_url=gif_url, unix_time=unix_date)

def manual(everyone="False", userid="None"):
    if everyone == "True" and userid != "None":
        print(colors.red + "Select only one option!" + colors.reset)
    elif everyone == "True":
        response = prepare_webhook(manual=True)
        return response
    elif userid != "None":
        unix_date = configuration.get_value("RockForPeople", "unix_date")
        days, hours = remaining_time(unix_time=unix_date)
        response = send_webhook(type="user_ping",days=days, userid=userid, manual = True)
        return response
