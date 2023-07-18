from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from .serializers import RequestSerializer, MatchMechanicSerializer
from .models import Request, Mechanic
from rest_framework.views import APIView
from rest_framework.response import Response
import googlemaps
from django.conf import settings


class MatchMechanicView(APIView):
    def post(self, request, format=None):
        # Get the user address from the request body
        user_address = request.data.get('address')
        description = request.data.get('description')

        if not user_address or not description:
            return Response('Invalid address, car brand, or description', status=400)

        # Convert the user address to latitude and longitude
        latitude, longitude = get_coordinates(user_address)

        if latitude is None or longitude is None:
            return Response({'error': 'Invalid address'}, status=400)

        response_data = {
            'latitude': latitude,
            'longitude': longitude
        }

        return Response(response_data, status=200)


def get_coordinates(address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    return None, None
