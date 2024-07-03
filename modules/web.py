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
    '''Generate data for HTML'''
    if request.method == 'POST':
        # Handle form submission here if necessary
        pass

    sections = configuration.get_section().strip().split('\n')
    data = []
    for section in sections:
        if section:  # Check to avoid empty section names
            keys = configuration.get_key(section).strip().split('\n')
            section_data = {
                'section': section,
                'items': []
            }
            for key in keys:
                if key:  # Check to avoid empty key names
                    if key != "created" and key != "modified":
                        old_value = configuration.get_value(section, key)
                        section_data['items'].append({
                            'key': key,
                            'old_value': old_value,
                            'new_value': ''
                        })
            data.append(section_data)

    return render_template('settings.html', data=data)


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
    if enabled == "True":
        app.run(debug=True, use_reloader=False, port=port)
        print(colors.green + "Web started" + colors.reset)