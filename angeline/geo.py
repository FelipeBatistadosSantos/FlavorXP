import requests

API_KEY = 'AIzaSyCwZdw6qgPukD4g4FwTshRuxgEeKrJz7C4'

endereco = '1 hack drive, menlo park, CA'

params = {
    'key': API_KEY,
    'endereco': endereco
}

base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
response = requests.get(base_url, params=params).json()
response.keys()

if response['status'] == 'OK':
    geometry = response['results'][0]['geometry']
    lat = geometry['location']['lat']
    lon = geometry['location']['lng']

print(lat, lon)    