from django.contrib.gis.db import models
from userauth.models import User, CarBrand


class MechanicManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(account_type='mechanic')


class Mechanic(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    location = models.PointField()

    objects = MechanicManager()


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
