from configparser import ConfigParser
from modules.f_time import get_time
import modules.colors as colors
config = ConfigParser()


#Create config
def create():
    config.read("config.cfg")

    webhook_url = input("Webhook URL: ")
    role_id = input("Role id: ")
    rfp_date = input("Unix date for RfP: ")
    ping_at = input("Ping at: ")
    startup_gif = input("Type of startup image(png/jpg/gif):")
    web_enabled = input(f"Do you wanna enable WebUI? {colors.red} Before enabling please make sure nobody can access it without your permission! For more informations visit my github {colors.reset}: ") or False
    if(web_enabled == "y" or web_enabled == "yes"):
        web_enabled = True
    web_port = input("Please specify webport to use:") or 5000

    #Add basic information
    config.add_section("General")
    config.set("General", "created", get_time())
    config.set("General", "modified", get_time())
    
    config.set("General", "name", "General")

    config.set("General", "webhook", webhook_url)
    config.set("General", "role_id", role_id)
    config.set("General", "ping_at", ping_at)
    config.set("General", "startup", startup_gif)

    #Web section
    config.add_section("Web")
    config.set("Web", "created", get_time())
    config.set("Web", "modified", get_time())
    config.set("Web", "enabled", str(web_enabled))
    config.set("Web", "port", web_port)

    #Rock for People Section
    config.add_section("RockForPeople")
    config.set("RockForPeople", "unix_date", rfp_date)
    config.set("RockForPeople", "created", get_time())
    config.set("RockForPeople", "modified", get_time())
    config.set("RockForPeople", "300", "None")
    config.set("RockForPeople", "250", "None")
    config.set("RockForPeople", "200", "None")
    config.set("RockForPeople", "150", "None")
    config.set("RockForPeople", "100", "None")
    config.set("RockForPeople", "50", "None")
    config.set("RockForPeople", "31", "None")
    config.set("RockForPeople", "14", "None")
    config.set("RockForPeople", "7", "None")
    config.set("RockForPeople", "5", "None")
    config.set("RockForPeople", "4", "None")
    config.set("RockForPeople", "3", "None")
    config.set("RockForPeople", "2", "None")
    config.set("RockForPeople", "1", "None")
    config.set("RockForPeople", "0", "None")
    
    #Save config
    with open("config.cfg", "w") as f:
        config.write(f)
    
    print(colors.green + "Config successfully generated!" + colors.reset)


def load():
    config.read("config.cfg")
    content = {}
    for section in config.sections():
        content[section] = dict(config.items(section))
    print(colors.green + "Config loaded successfully!" + colors.reset)
    return content

def save(section, key, value):
    print(colors.yellow + "Saving config!" + colors.reset)
    config.read("config.cfg")
    section_name = section.replace(" ","_")
    try:
        config.set(section_name, "modified", get_time())
        config.set(section_name, key, value)
        with open("config.cfg", "w") as f:
          config.write(f)
    except:
        config.add_section(section_name)
        config.set(section_name, "created", get_time())
        config.set(section_name, "modified", get_time())
        config.set(section_name, "has_finished", "False")
        config.set(section_name, "name", section)
        config.set(section_name, key, value)
        with open("config.cfg", "w") as f:
            config.write(f)   
    print(colors.green + "Config saved!" + colors.reset) 

def modify(action="", section=None, key="", value=""):
    config.read("config.cfg")
    action = action.lower()
    if section != None:
        #Delete section
        if action == "remove":
            print(colors.yellow + f"Removing section: {section}" + colors.reset)
            config.remove_section(section)
            print(colors.green + "Section removed!" + colors.reset)
        #Modify section
        if action == "modify":
            print(colors.yellow + f"Modifing section: {section}, key: {key}, value: {value}" + colors.reset)
            save(section, key, value)
        else:
            print(colors.red + f"Unknown action!{action}" + colors.reset)
    else:
        print(colors.red + f"You did not specify section!" +colors.reset)

def get_section():
    sections = "\n"
    for section in config:
        if section != "DEFAULT":
            sections += section + "\n"
    return sections

def get_key(section):
    keys = "\n"
    for key in config[section]:
        keys += key + "\n"
    return keys

def get_value(section, key):
    try:
        value = config[section][key]
        return value
    except:
        error_message = f"Error: Value can not be found in {section}/{key}"
        return None