from typing import List, Dict
import mysql.connector
import simplejson as json
import requests
import configparser
from flask import Flask, Response
from flask import render_template, request

app = Flask(__name__)


def cities_import() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'citiesData'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


@app.route('/')
def index():
    user = {'username': 'Miguel'}
    cities_data = cities_import()

    return render_template('index.html', title='Home', user=user, cities=cities_data)


@app.route('/api/cities')
def cities() -> str:
    js = json.dumps(cities_import())
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route(`/api/openweathermap`)
def weather_dashboard():
    return render_template(`index.html`)

@app.route('/results', methods=['POST'])
def render_results():
    city_name = request.form['CityName']

    api_key = get_api_key()
    data = get_weather_results(city_name, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('#',
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results(city_name, api_key):
   api_url = "http://api_url = api.openweathermap.org/" \
             "data/2.5/weather?q={}&units=imperial&appid={}.format(city_name, api_key)
   r = requests.get(api_url)
   return r.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0')