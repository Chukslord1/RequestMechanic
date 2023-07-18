from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Request, Mechanic
from userauth.models import User
from .serializers import MatchMechanicSerializer
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.conf import settings
import googlemaps


class MatchMechanicView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Verify permission based on UserID
        user_id = '6ec9c5c69aea612fbb3cf0ed638784d09774822b8c1d9a2163550803b03e5742970f9dcd3163adc7db615754103406014a9777a9a4f43acf447e56daee28ddbc'
        # if user_id != request.data.get('user_id'):
        #     return Response({'error': 'Permission denied'}, status=403)

        # Get user information from the database
        user = get_object_or_404(User, id=user_id)

        # Get the user address from the request body
        user_address = request.data.get('address')
        car_brand_id = request.data.get('car_brand_id')
        description = request.data.get('description')

        if not user_address or not car_brand_id or not description:
            return Response('Invalid address, car brand, or description', status=400)

        # Convert the user address to latitude and longitude
        latitude, longitude = get_coordinates(
            user_address, settings.GOOGLE_MAPS_API_KEY)

        if latitude is None or longitude is None:
            return Response({'error': 'Invalid address'}, status=400)

        user_point = GEOSGeometry(f'POINT({longitude} {latitude})', srid=4326)

        mechanics = Mechanic.objects.filter(
            user=user,
            user__car_brand_id=car_brand_id,
            user__car_model="Ranger Rover",
            is_available=True,
            rating__gte=3.0
        ).annotate(distance=Distance('user__address', user_point)).order_by('distance')

        nearest_mechanics = mechanics[:2]

        if not nearest_mechanics:
            return Response({'error': 'No mechanics found'}, status=404)

        serializer = MatchMechanicSerializer(nearest_mechanics, many=True)

        # Create a request
        request_obj = Request.objects.create(
            user=user,
            car_brand_id=car_brand_id,
            description=description
        )

        return Response({'success': 'Request created successfully'}, status=200)


def get_coordinates(address, api_key):
    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    return None, None
