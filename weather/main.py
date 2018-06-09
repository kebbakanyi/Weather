import requests
from datetime import datetime as dt
from darksky import forecast
import credentials

# api_key = credentials.DARKSKY_API_KEY

google_api_key = credentials.GOOGLE_API_KEY


# t = dt(2018, 6, 6).isoformat()
# HOME_ADDRESS = '15631 Ash way Lynnwood WA 98087'.replace(' ', '+')
# HOME_ADDRESS_CORDINATES= (api_key, 47.856449, - 122.254531)
# home = forecast(*HOME_ADDRESS)


def get_address():
    my_address = input('Input Address: ').replace(' ', '+')
    return my_address


def get_geo_location(my_address, my_google_api):

    api = f'&key={my_google_api}'

    my_address = f'address={my_address}'
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    full_url = base_url + address + api

    params = {'sensor': 'false', 'address': my_address.replace('+', ' ')}

    r = requests.get(full_url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']

    return location['lat'], location['lng']


address = get_address()
print(get_geo_location(address, google_api_key))


# def format_time(time):
#     return dt.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')

# print(home['currently'])
# home_time = home['currently']['time']
# print(format_time(home_time))
