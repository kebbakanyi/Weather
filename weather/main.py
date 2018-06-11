from datetime import date, timedelta, datetime
import requests
from darksky import forecast
import credentials

DARKSKY_API_KEY = credentials.DARKSKY_API_KEY
GOOGLE_API_KEY = credentials.GOOGLE_API_KEY


def get_address():
    my_address = input('Input Address: ').replace(' ', '+')
    return my_address


def convert_time(timestamp):
    return datetime.utcfromtimestamp(timestamp)


def time_zone(address, time):

    base_url = f'https://maps.googleapis.com/maps/api/timezone/json?'
    params = f'location={address[0]},{address[1]}&timestamp={time}&key={GOOGLE_API_KEY}'
    url = base_url + params
    r = requests.get(url)
    results = r.json()

    offset_time = results['rawOffset']
    dst_offset = results['dstOffset']
    return offset_time, dst_offset


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
    lat, lng, formatted_address = addr_coordinates(address, GOOGLE_API_KEY)
    weather_location = (lat, lng)

    print(f'\n-----Weather forecast for {formatted_address}-----\n')

    weekday = date.today()

    with forecast(f'{DARKSKY_API_KEY}', *weather_location) as location:
        print(
            f'Current Temperature in {formatted_address} is {int(round(location.temperature))}\xb0F')
        print(location.daily.summary, end='\n---\n')

        right_time, dst_offset = time_zone(weather_location, location.time)

        print(convert_time(location.time + right_time + dst_offset))
        print('--------')

        for day in location.daily:
            day = dict(day=date.strftime(weekday, '%a'),
                       sum=day.summary,
                       tempMin=int(round(day.temperatureMin)),
                       tempMax=int(round(day.temperatureMax)))
            print(
                '{day}: {sum} Temp range: {tempMin}\xb0F - {tempMax}\xb0F'.format(**day))

            weekday += timedelta(days=1)


if __name__ == '__main__':
    weather_forecast()
