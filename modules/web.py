from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import modules.configuration as configuration
import modules.colors as colors
import modules.schedule_handler as schedule_handler
import modules.discord as discord
import os, datetime
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

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%B %d, %Y at %I:%M %p'):
    """Format a datetime string to a more readable format, ignoring microseconds."""
    dt = datetime.datetime.strptime(value.split('.')[0], '%Y-%m-%d %H:%M:%S')
    return dt.strftime(format)

#Update values
@app.route('/update', methods=['POST'])
def update_settings():
    '''Handle the submitted form data'''
    data = {
        "action" : None,
        "details": {}
    }
    data['action'] = "Modifying settings"
    for key, value in request.form.items():
        if value:
            key_parts = key.split('%%')
            section = key_parts[0]
            key = key_parts[1]

            if section not in data['details']:
                data['details'][section] = {}  # Initialize the section dictionary if it doesn't exist

            data['details'][section][key] = value
            configuration.modify(action="modify", section=section, key=key, value=value )
            if section == "General" and key == "ping_at":
                schedule_handler.update(time=value)
        pass
    return render_template('success.html', data=data )

# Add this route to serve static files from the gifs directory
@app.route('/gifs/<filename>')
def serve_gifs(filename):
    return send_from_directory(os.path.join(app.root_path, '../gifs'), filename)

# Routes for managing Special Days
@app.route('/special-days', methods=['GET', 'POST'])
def special_days():
    if request.method == 'POST':
        day = request.form['day']
        image = request.files['image']
        if image:
            extension = image.filename.split('.')[-1]
            filename = f"{day}.{extension}"
            image_path = os.path.join('gifs', filename)
            image.save(image_path)
            configuration.save("SpecialDays", day, extension)
        return redirect(url_for('special_days'))

    keys = configuration.get_key("SpecialDays").strip().split('\n')
    days = {}
    for key in keys:
        if key and key not in ["created", "modified"]:
            extension = configuration.get_value("SpecialDays", key)
            image_path = f"gifs/{key}.{extension}"
            days[key] = image_path
    return render_template('special_days.html', days=days)

@app.route('/delete-day/<day>', methods=['POST'])
def delete_day(day):
    path = os.path.join("gifs")
    extension = configuration.get_value(section="SpecialDays", key=day)
    image_path = f"{path}/{day}.{extension}"
    if image_path and os.path.exists(image_path):
        os.remove(image_path)
        configuration.modify(action="remove_key",section="SpecialDays",key=day)
    return redirect(url_for('special_days'))

#Show Manual ping page.
@app.route('/manual_ping', methods=['POST', 'GET'])
def manual_ping():
    '''Generate and process data for manual_ping HTML'''
    data = {
        "action" : None,
        "details": {}
    }

    if request.method == "GET":
        return render_template('manual_ping.html')
    if request.method == "POST":
        for key, value in request.form.items():
            if key == "everyone" and value == "on":
                data['action'] = "Global Discord ping"
                response = discord.manual(everyone="True")
                data['details']['response'] = response
                data['details']['response_details'] = response.json()
            elif key == "userId":
                data['action'] = "User ping Discord ping"
                data['details']['userId'] = value
                data['details']['response'] = discord.manual(userid=value)
        if str(data['details']['response']) == "<Response [200]>":
            return render_template('success.html', data=data )
        else:
            return render_template('error.html', data=data )

def start():
    enabled = configuration.get_value(section="Web", key="enabled")
    port = configuration.get_value(section="Web", key="port")
    host = configuration.get_value(section="Web", key="host")
    debug = configuration.get_value(section="Web", key="debug")
    if debug == "True":
        debug = True
    else: 
        debug = False
    if enabled == "True":
        app.run(debug=debug, use_reloader=False, port=port, host=host)
        print(colors.green + "Web started" + colors.reset)