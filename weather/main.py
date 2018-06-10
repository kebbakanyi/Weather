import requests
from datetime import datetime as dt
import time
from darksky import forecast
import credentials

darksky_api_key = credentials.DARKSKY_API_KEY
GOOGLE_API_KEY = credentials.GOOGLE_API_KEY


def format_time(my_time):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(my_time)))


def get_address():
    my_address = input('Input Address: ').replace(' ', '+')
    return my_address


def addr_coordinates(address, key):

    the_address = f'address={address}'
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {'&key': f'{key}',
              'address': the_address}

    r = requests.get(base_url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']

    return location['lat'], location['lng']


def weather_forecast():

    address = get_address()
    lat, long = addr_coordinates(address, GOOGLE_API_KEY)
    weather_location = (darksky_api_key, lat, long)
    location_forecast = forecast(*weather_location)
    location_temp = location_forecast['currently']['temperature']

    return location_temp


print(weather_forecast())
