from django.urls import path
from .views import MatchMechanicView

urlpatterns = [
    path('match-mechanic/', MatchMechanicView.as_view(), name='match-mechanic'),
]
