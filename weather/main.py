from datetime import date, timedelta
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
    formatted_address = results[0]['formatted_address']
    location = results[0]['geometry']['location']

    return location['lat'], location['lng'], formatted_address


def weather_forecast():

    address = get_address()
    lat, long, formatted_address = addr_coordinates(address, GOOGLE_API_KEY)
    weather_location = (lat, long)

    print(f'\n-----Weather forecast for {formatted_address}-----\n')

    weekday = date.today()

    with forecast(f'{DARKSKY_API_KEY}', *weather_location) as location:
        print(
            f'Current Temperature in {formatted_address} is {int(round(location.temperature))}\xb0F')
        print(location.daily.summary, end='\n---\n')

        for day in location.daily:
            day = dict(day=date.strftime(weekday, '%a'),
                       sum=day.summary,
                       tempMin=int(round(day.temperatureMin)),
                       tempMax=int(round(day.temperatureMax)))
            print(
                '{day}: {sum} Temp range: {tempMin}\xb0F - {tempMax}\xb0F'.format(**day))

            weekday += timedelta(days=1)


weather_forecast()
