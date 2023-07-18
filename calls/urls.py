from django.urls import path
from .views import InitiateCallView, EndCallView

urlpatterns = [
    path('call/initiate/', InitiateCallView.as_view(), name='initiate-call'),
    path('call/end/', EndCallView.as_view(), name='end-call'),
]
