import requests
from darksky import forecast
import credentials

DARKSKY_API_KEY = credentials.DARKSKY_API_KEY
GOOGLE_API_KEY = credentials.GOOGLE_API_KEY


def get_address():
    my_address = input('Input Address: ').replace(' ', '+')
    return my_address


def addr_coordinates(address, api_key):

    the_address = f'address={address}'
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {'&key': f'{api_key}',
              'address': the_address}

    r = requests.get(base_url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']

    return location['lat'], location['lng']


def weather_forecast():

    address = get_address()
    lat, long = addr_coordinates(address, GOOGLE_API_KEY)
    weather_location = (DARKSKY_API_KEY, lat, long)
    location_forecast = forecast(*weather_location)
    location_temp = str(
        location_forecast['currently']['temperature']) + '\xB0F'

    return location_temp


print(weather_forecast())
