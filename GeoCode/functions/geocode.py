import ast
import json
import googlemaps
from django.conf import settings



gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

def get_geocode(address):
    # Get the GeoCode of the address
    geocode_result = gmaps.geocode(address)
    # Convert the resultset into dictionary
    data = ast.literal_eval(json.dumps(
        geocode_result[0]['geometry']['location']))
    lat = data['lat']
    lang = data['lng']
    return lat, lang
