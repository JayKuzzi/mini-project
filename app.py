from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
import requests
import requests_cache


requests_cache.install_cache('weather_api_cache', backend='sqlite', expire_after=36000)

cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

weather_url_template = 'https://api.breezometer.com/weather/v1/current-conditions?lat={lat}&lon={lon}&key={key}'
MY_API_KEY = app.config['MY_API_KEY']


# Welcome Page
@app.route('/')
def hello_world():
    return 'Hello,This is a mini project about database operation,for example: quiring and saving weather data to database from website, you can use REST API including GET, POST and DELETE methods!'


# Quire all users
@app.route('/quire', methods=['GET'])
def quire():
    rows = session.execute("""Select * From mini.user""")
    for user in rows:
        return ('<h2>This is all users : {} </h2>'.format(rows.current_rows))
    return ('<h1>That data does not exist!</h1>')


# Quire user by name
@app.route('/quire/<name>', methods=['GET'])
def profile(name):
    rows = session.execute("""Select * From mini.user where name = '{}' ALLOW FILTERING""".format(name))
    for user in rows:
        return ('<h2>This is info : {} by name: {}</h2>'.format(rows.current_rows, name))
    return ('<h1>That data does not exist!</h1>')


# Add user
@app.route('/add_user', methods=['POST'])
def create_a_record():
    if not request.json or not 'name' in request.json or not 'id' in request.json or not 'age' in request.json:
        return jsonify({'error': 'Incomplete data'}), 400
    new_record = {
        'id': request.json['id'],
        'age': request.json['age'],
        'name': request.json['name'],
        'password': request.json['password']
    }
    session.execute(
        """insert into mini.user(id, name, age, password) values ({}, '{}',{},'{}')""".format(new_record['id'],
                                                                                              new_record['name'],
                                                                                              new_record['age'],
                                                                                              new_record['password']))
    return jsonify({'message': 'Record has created: {}'.format(new_record['name'])}), 201


# Delete user
@app.route('/delete/<deletename>', methods=['DELETE'])
def delete(deletename):
    rows = session.execute("""Select * From mini.user where name = '{}' ALLOW FILTERING""".format(deletename))
    for item in rows.current_rows:
        id = item.id
        if item.name == deletename:
            session.execute("""Delete From mini.user where id = {}""".format(id))
            return jsonify({'success': True})
    return jsonify({'error': 'name not found!'}), 404


# Get weather information in Datatabase
@app.route('/quireweather', methods=['GET'])
def quireweather():
    rows = session.execute("""Select * From mini.weather""")
    for user in rows:
        return ('<h2>This is all weather data : {} </h2>'.format(rows.current_rows))
    return ('<h1>That data does not exist!</h1>')


# Get weather information on Internet and save in Database
@app.route('/weather', methods=['GET'])
def weatherchart():
    my_latitude = request.args.get('lat', '51.52369')
    my_longitude = request.args.get('lon', '-0.0395857')
    weather_url = weather_url_template.format(lat=my_latitude, lon=my_longitude, key=MY_API_KEY)

    # get weather on Internet
    resp = requests.get(weather_url)
    time = resp.json()['data']['datetime']
    temperature = str(resp.json()['data']['temperature']['value']) + resp.json()['data']['temperature']['units']
    wind_speed = str(resp.json()['data']['wind']['speed']['value']) + resp.json()['data']['wind']['speed']['units']
    # get current max(id)on mini.weather
    rows = session.execute("""select max(id) from mini.weather""")
    for item in rows.current_rows:
        my_id = item.system_max_id + 1
    if resp.ok:
        # save data
        session.execute(
            """insert into mini.weather(id, datetime, temperature, wind_speed) values ({}, '{}','{}','{}')""".format(
                my_id,
                time,
                temperature,
                wind_speed))
        return ('<h1>Datas have saved!</h1>')
    else:
        return ('<h1>Datas have not saved!</h1>')
    return ("Done!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
