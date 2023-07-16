import googlemaps
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Request, Mechanic
from .serializers import RequestSerializer, MatchMechanicSerializer
from django.conf import settings
from pyresponse.response import create_error_response, create_success_response


class MatchMechanicView(APIView):
    def post(self, request, format=None):
        user_address = request.data.get('address')
        car_brand_id = request.data.get('car_brand_id')
        description = request.data.get('description')

        if not user_address or not car_brand_id or not description:
            return create_error_response(message='Invalid address, car brand, or description', status_code=400, )

        # Convert address to latitude and longitude
        latitude, longitude = get_coordinates(user_address)

        if latitude is None or longitude is None:
            return Response({'error': 'Invalid address'}, status=400)

        user_point = GEOSGeometry(f'POINT({longitude} {latitude})', srid=4326)

        mechanics = Mechanic.objects.filter(
            account_type='mechanic', user__car_brand_id=car_brand_id, is_available=True, rating__gte=3.0
        ).annotate(distance=Distance('location', user_point)).order_by('distance')

            
        nearest_mechanic = mechanics.objects.all()[0:2]

        if nearest_mechanic is None:
            return create_error_response(message='No mechanics found', status_code=404)

        serializer = MatchMechanicSerializer(nearest_mechanic)

        # Create a request
        request_obj = Request.objects.create(
            user=request.user,
            car_brand_id=car_brand_id,
            description=description
        )

        return create_success_response(data=serializer.data, message='Success', status_code=200)


def get_coordinates(address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    return None, None
