from flask import Flask, render_template, request, redirect, url_for
import modules.configuration as configuration
import modules.colors as colors
app = Flask(__name__, template_folder='../web/', static_folder='../web/static')

#Print basic Index.html that will show us redirects.
@app.route('/')
def index():
    '''Show default page'''
    return render_template('index.html')

#Show settings and it's values.
@app.route('/settings', methods=['POST', 'GET'])
def settings():
    '''Generate data for settings HTML'''
    sections = configuration.get_section().strip().split('\n')
    data = []
    for section in sections:
        if section and section not in ["SpecialDays", "Statistics"]:  # Check to avoid empty section names and few specific sections
            keys = configuration.get_key(section).strip().split('\n')
            section_data = {
                'section': section,
                'items': []
            }
            for key in keys:
                if key and key not in ["created", "modified"]:  # Check to avoid empty key names and few specific keys
                    old_value = configuration.get_value(section, key)
                    section_data['items'].append({
                        'key': key,
                        'old_value': old_value,
                        'new_value': ''
                    })
            data.append(section_data)

    return render_template('settings.html', data=data)

#Show statistics.
@app.route('/statistics', methods=['POST', 'GET'])
def statistics():
    '''Generate data for statistics HTML'''
    data = []
    keys = configuration.get_key("Statistics").strip().split('\n')
    section_data = {
        'section': "Statistics",
        'items': []
    }

    # Check if this is highest streak
    highest_streak = int(configuration.get_value("Statistics", "highest_streak"))
    streak = int(configuration.get_value("Statistics", "streak"))
    is_highest_streak = streak >= highest_streak
    
    for key in keys:
        if key and key not in ["created", "modified", "highest_streak"]:  # Check to avoid empty key names and specific keys
            value = configuration.get_value("Statistics", key)
            section_data['items'].append({
                'key': key,
                'value': value,
                'highest_streak': is_highest_streak and key == "streak"
            })
    
    if not is_highest_streak:
        section_data['items'].append({
            'key': "highest_streak",
            'value': highest_streak,
            'highest_streak': False  # Ensure this entry is not mistakenly highlighted
        })
    
    data.append(section_data)
    return render_template('statistics.html', data=data)

#Update values
@app.route('/update', methods=['POST'])
def update_settings():
    '''Handle the submitted form data'''

    for key, value in request.form.items():
        if value:
            #Format data for saving
            key = key.split('%%')
            print(key)
            section = key[0]
            key = key[1]
            configuration.modify(action="modify", section=section, key=key, value=value )
        pass
    return redirect(url_for('index'))

def start():
    enabled = configuration.get_value(section="Web", key="enabled")
    port = configuration.get_value(section="Web", key="port")
    debug = configuration.get_value(section="Web", key="debug")
    if debug == "True":
        debug = True
    else: 
        debug = False
    if enabled == "True":
        app.run(debug=debug, use_reloader=False, port=port)
        print(colors.green + "Web started" + colors.reset)