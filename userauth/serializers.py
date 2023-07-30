from io import BytesIO
from PIL import Image

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from phonenumber_field.serializerfields import PhoneNumberField

from cloudinary.templatetags import cloudinary
import cloudinary
import cloudinary.uploader

from .models import User, Profile, SupportingDocument, CarBrand
from microservices.otp import verify_otp
from microservices.messages import *

from rest_framework.exceptions import ValidationError, AuthenticationFailed


class SubmitEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = "__all__"

    def validate(self, attrs):
        email = attrs.get("email", "")
        user = User.objects.get(email=email)
        _check_email = User.objects.filter(email=email)
        if _check_email.exists() and user.email_verified == True:
            raise serializers.ValidationError("User already verified.")
        return super().validate(attrs)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(
        max_length=255,
        min_length=5,
        error_messages={
            'required': EMAIL_REQUIRED,
            'invalid': EMAIL_INVALID
        }
    )
    password = serializers.CharField(
        max_length=68,
        min_length=5,
        write_only=True,
        error_messages={
            'required': PASSWORD_REQUIRED
        }
    )
    has_pin = serializers.SerializerMethodField()
    tokens = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    car_speciality = serializers.SerializerMethodField()
    education_level = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email",
                  "phone_number", "password", "has_pin", "profile_pic", "account_type", "car_brand", "car_speciality","education_level", "tokens"]

    def get_has_pin(self, user):
        if isinstance(user, dict):
            return user.get('pin') is not None
        return user.pin is not None

    def get_tokens(self, user):
        return {
            'access': user.tokens['access'],
            'refresh': user.tokens['refresh'],
        }

    def get_profile_pic(self, user):
        try:
            profile = Profile.objects.get(user=user)
            return profile.profile_pic.url
        except Profile.DoesNotExist:
            return None
    
    def get_car_speciality(self, user):
        try:
            profile = Profile.objects.get(user=user)
            return profile.car_speciality
        except Profile.DoesNotExist:
            return None
    
    def get_education_level(self, user):
        try:
            profile = Profile.objects.get(user=user)
            return profile.education_level
        except Profile.DoesNotExist:
            return None

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', None)

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError(
                INVALID_CREDENTIALS
            )

        if not user.is_verified:
            raise serializers.ValidationError(
                EMAIL_NOT_VERIFIED
            )

        if not user.is_active:
            raise serializers.ValidationError(
                ACCOUNT_DEACTIVATED
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                INVALID_CREDENTIALS
            )

        return user
        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.profile.first_name,
            "last_name": user.profile.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "profile_pic": user.profile.profile_pic.url,
            "has_pin": user.pin
        }


class LoginPinSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    pin = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['email', 'pin']

    def validate(self, attrs):
        email = attrs.get('email', '')
        pin = attrs.get('pin', None)

        if not email:
            raise serializers.ValidationError("Email field is required")

        user = authenticate(email=email, pin=pin)

        if not user:
            raise AuthenticationFailed("Incorrect pin.")

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        if not user.is_active:
            raise AuthenticationFailed(
                "Your account has been deactivated. Please contact customer support.")

        refresh = RefreshToken.for_user(user)
        response = {
            'refresh': str(refresh),
        }

        return response


class OTPSerializer(serializers.Serializer):
    otp_code = serializers.IntegerField()
    email = serializers.EmailField(max_length=255, min_length=5)

    class Meta:
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()
    username = serializers.CharField(read_only=True)
    profile_pic = serializers.SerializerMethodField(
        source='profile.profile_pic', read_only=True)
    car_speciality = serializers.SerializerMethodField(
        source='profile.car_speciality', read_only=True)
    education_level = serializers.SerializerMethodField(
        source='profile.education_level', read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name",
                  "email", "password", "username", "phone_number", "profile_pic", "car_brand","car_speciality", "education_level", "tokens",]

    def create(self, validated_data):
        email = validated_data.get("email")
        phone_number = validated_data.get("phone_number")
        password = validated_data.get("password")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        profile_pic = validated_data.get("profile_pic")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "User with this email already exists. Please sign in or verify your account.")

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                "User with this phone number already exists.")

        user = User.objects.create(
            email=email,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user)
        profile.first_name = first_name
        profile.last_name = last_name

        if profile_pic:
            # If profile_pic is provided, upload the image to Cloudinary
            uploaded_image = cloudinary.uploader.upload(profile_pic)
            profile.profile_pic = uploaded_image['secure_url']
        else:
            # If profile_pic is not provided, set a default image
            profile.profile_pic = cloudinary.utils.cloudinary_url(
                'image/upload/v1674506279/pdokhuhpuwvhmtgxjc2s.jpg')[0]

        profile.save()

        return user
    
    def get_profile_pic(self, obj):
        if obj.profile.profile_pic:
            return obj.profile.profile_pic
        return cloudinary.utils.cloudinary_url(
            'image/upload/v1674506279/pdokhuhpuwvhmtgxjc2s.jpg')[0]

    def get_car_speciality(self, user):
        try:
            profile = Profile.objects.get(user=user)
            return profile.car_speciality
        except Profile.DoesNotExist:
            return None

    def get_education_level(self, user):
        try:
            profile = Profile.objects.get(user=user)
            return profile.education_level
        except Profile.DoesNotExist:
            return None
    # @receiver(post_save, sender=User)
    # def create_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return {
            'access': access_token,
            'refresh': refresh_token
        }

    def validate(self, attrs):
        email = attrs.get("email", "")
        phone_number = attrs.get("phone_number", "")

        if not email:
            raise ValidationError("Email field is required")

        if not phone_number:
            raise ValidationError("Phone number field is required")

        return attrs


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ['id', 'name']


class SupportingDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportingDocument
        fields = ['document']


class UserSerializer(serializers.ModelSerializer):
    car_brand = CarBrandSerializer(many=True, read_only=True)
    supporting_documents = SupportingDocumentSerializer(
        many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'car_brand',
                  'car_model', 'completed_registration', 'supporting_documents']


class Step1Serializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    account_type = serializers.ChoiceField(choices=User.ACCOUNT_TYPES)

    # profile_pic = serializers.SerializerMethodField(
    #     source='profile.profile_pic', read_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists. Please sign in or verify your account.")
        return value

    def validate_password(self, value):
        return value

    class Meta:
        model = User
        fields = ['email', 'password', 'account_type']


class Step2Serializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name',
                  'date_of_birth', 'phone_number']


class Step3MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'car_speciality', 'education_level']


class Step3OwnerSerializer(serializers.ModelSerializer):
    car_brand = serializers.PrimaryKeyRelatedField(
        queryset=CarBrand.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['id', 'car_brand', 'car_model']


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    redirect_url = serializers.CharField(required=False)

    class Meta:
        fields = "__all__"

    def validate(self, attrs):
        email = attrs.get('email', '')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("User does not exist.")
        return super().validate(attrs)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    redirect_url = serializers.CharField(required=False)

    class Meta:
        fields = "__all__"

    def validate(self, attrs):
        email = attrs.get('email', '')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("User does not exist.")
        return super().validate(attrs)


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        otp_code = attrs.get("otp_code")
        if not verify_otp(otp_code, email):
            raise serializers.ValidationError("Invalid OTP")
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(min_length=6, max_length=6)
    password = serializers.CharField(
        min_length=6, max_length=80, write_only=True)

    def get_user(self, validated_data):
        email = validated_data.get("email")
        user = User.objects.get(email=email)
        return user

    def validate(self, attrs):
        email = attrs.get("email")
        user = self.get_user(attrs)
        if not user:
            raise serializers.ValidationError("User does not exist.")
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


class ImageValidator:
    def __call__(self, value):
        if not value:
            return value
        if not value.content_type.startswith('image'):
            raise ValidationError(
                ('File type not supported. Please upload an image file.'))


class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(
        validators=[ImageValidator()], required=False)

    class Meta:
        model = Profile
        fields = ('profile_pic',)

    def update(self, instance, validated_data):
        picture = validated_data.get('profile_pic')
        if picture:
            # Open the image, convert to RGB mode, compress, and convert to JPEG
            img = Image.open(picture)
            img = img.convert('RGB')
            img.thumbnail((500, 500))
            output = BytesIO()
            img.save(output, format='JPEG', quality=60)
            output.seek(0)

            # Upload compressed image to Cloudinary
            result = cloudinary.uploader.upload(output)

            # Construct Cloudinary URL with domain and resource type
            cloudinary_url = cloudinary.CloudinaryImage(result['public_id']).build_url(
                format=result['format'],
                secure=True,
            )

            # Update profile picture URL and save
            instance.profile_pic = result['secure_url']
            instance.save()

            # Construct response with Cloudinary URL
            response_data = {
                "success": "Profile picture updated.",
                "profile_pic": cloudinary_url,
            }
            # print(response_data)

            return response_data
        else:
            return super().update(instance, validated_data)

    def delete(self, instance):
        if not instance.profile_pic:
            raise serializers.ValidationError("Profile picture not found.")

        try:
            # Remove picture from Cloudinary and save changes
            cloudinary.uploader.destroy(instance.profile_pic.public_id)
            instance.profile_pic = None
            instance.save()

            # Return success message
            return {"success": "Profile picture removed."}

        except Exception as e:
            raise serializers.ValidationError("Error removing picture.")


class PinSerializer(serializers.Serializer):
    old_pin = serializers.IntegerField(required=False)
    new_pin = serializers.IntegerField()

    def validate_new_pin(self, value):
        if value == self.initial_data.get('old_pin'):
            raise serializers.ValidationError(
                'New pin cannot be the same as old pin')
        return make_password(str(value))


class ChangeUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
            return {
                'status': STATUS_OK,
                'message': LOGOUT_SUCCESS
            }
        except TokenError:
            return {
                'status': STATUS_UNAUTHORIZED,
                'message': INVALID_TOKEN
            }


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Invalid password.')
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.delete()
        return {
            'status': STATUS_OK,
            'message': DELETE_ACCOUNT_SUCCESS
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}
