from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save
from django.dispatch import receiver
from microservices.id_generator import KUIDGenerator
import cloudinary
import cloudinary.models


class CarBrand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SupportingDocument(models.Model):
    id = models.CharField(primary_key=True, max_length=255,
                          default=KUIDGenerator.generate_kuid)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to='supporting_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email'}


class User(AbstractUser):
    AUCCOUNT_TYPES = (
        ('owner', 'owner'),
        ('mechanic', 'mechanic'),
    )

    id = models.CharField(primary_key=True, max_length=255,
                          default=KUIDGenerator.generate_kuid)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    account_type = models.CharField(
        choices=AUCCOUNT_TYPES, max_length=100, default='owner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pin = models.CharField(max_length=128, null=True)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
    completed_registration = models.BooleanField(default=False)
    car_brand = models.ManyToManyField(CarBrand)
    car_model = models.CharField(max_length=255, blank=True, null=True)

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0]
        return super().save(*args, **kwargs)

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Profile(models.Model):
    GENDER = (
        ("select", "Select"),
        ('male', 'Male'),
        ('female', 'Female')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_pic = cloudinary.models.CloudinaryField('image', blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default="select")
    date_of_birth = models.DateField(blank=True, null=True)
    car_speciality = models.CharField(max_length=255, blank=True, null=True)
    education_level = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.save()
        return super().save(*args, **kwargs)


class PushToken(models.Model):
    id = models.CharField(
        primary_key=True, max_length=255, default=KUIDGenerator.generate_kuid)
    token = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.token


# @ receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
    # if created and not instance.is_staff:  # Only create details for non-admin users
        # Security.objects.create(user=instance)
        # NextofKin.objects.create(user=instance)
        # Profile.objects.create(user=instance)
