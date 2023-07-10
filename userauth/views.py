# views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from microservices.otp import generate_otp, verify_otp
from .serializers import (
    LoginSerializer, PasswordResetSerializer, SetNewPasswordSerializer,
    SubmitEmailSerializer, UserSerializer, LoginPinSerializer,
    LogoutSerializer, OTPVerificationSerializer, DeleteAccountSerializer,
    Step1Serializer, Step2Serializer, Step3MechanicSerializer,
    Step3OwnerSerializer, SupportingDocumentSerializer, CarBrandSerializer
)
from .models import User, CarBrand, Profile
from microservices.response import create_error_response, create_success_response


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return create_success_response(message="Login successful.",
                                       data=serializer.data, status_code=status.HTTP_200_OK)


class LoginPinView(generics.CreateAPIView):
    serializer_class = LoginPinSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return create_success_response(message="Login successful.",
                                       data=data, status_code=status.HTTP_200_OK)


class SendOTPView(generics.CreateAPIView):
    serializer_class = SubmitEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        subject = "Signup Verification OTP"
        try:
            otp = generate_otp(email, subject)
            return create_success_response(message="Please check your email for OTP", status_code=status.HTTP_200_OK)
        except Exception as e:
            return create_error_response(message="Error occurred. Please try again.", status_code=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(generics.CreateAPIView):
    serializer_class = OTPVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp_code"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return create_error_response(
                message=f"User with email {email} does not exist", status_code=status.HTTP_400_BAD_REQUEST)

        verified = verify_otp(otp_code, email)
        if verified:
            if hasattr(user, 'is_verified') and not user.is_verified:
                user.is_verified = True
                user.save()
            return create_success_response(
                message="OTP Verified Successfully", status_code=status.HTTP_200_OK)
        else:
            return create_error_response(
                message="Invalid OTP", status_code=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email = serializer.validated_data["email"]
        subject = "Registration Verification OTP"
        try:
            otp_code = generate_otp(email, subject)
        except Exception as e:
            # user.delete()  # Delete the user if OTP generation fails
            return create_error_response(message=f"An error occurred while generating the OTP:", data={str(e)},
                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return create_success_response(
            data=serializer.data, message="Registration successful.", status_code=status.HTTP_201_CREATED)


class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        subject = "Password Reset"
        try:
            user = User.objects.get(email=email)
            otp_code = generate_otp(email, subject)
            return create_success_response("OTP sent to your email.", status_code=status.HTTP_200_OK)
        except User.DoesNotExist:
            return create_error_response("Email does not exist.", status_code=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(generics.UpdateAPIView):
    serializer_class = SetNewPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
            "email": request.data.get("email")})
        serializer.is_valid(raise_exception=True)

        otp_code = serializer.validated_data["otp_code"]
        email = serializer.context.get("email")

        try:
            user = serializer.validated_data["user"]
        except User.DoesNotExist:
            return create_error_response(
                f"User with email {email} does not exist", status_code=status.HTTP_400_BAD_REQUEST)

        password = serializer.validated_data["password"]
        user.set_password(password)
        try:
            user.save()
        except Exception as e:
            return create_error_response(f"An error occurred while saving the new password: {str(e)}",
                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return create_success_response(message="Password Reset Successful", status_code=status.HTTP_200_OK)


class LogoutView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return create_success_response("Logout Successful", serializer.data, status_code=serializer.data['status'])


class DeleteAccountView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteAccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return create_success_response("Account Deleted", serializer.data, status_code=serializer.data['status'])


class CarBrandListView(generics.ListAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarBrandCreateView(generics.CreateAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class SupportingDocumentUploadView(generics.CreateAPIView):
    serializer_class = SupportingDocumentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Step1RegistrationView(generics.CreateAPIView):
    serializer_class = Step1Serializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        profile = Profile(user=user)
        profile.save()
        email = serializer.validated_data["email"]
        subject = "Registration Verification OTP"
        try:
            otp_code = generate_otp(email, subject)
        except Exception as e:
            # user.delete()  # Delete the user if OTP generation fails
            return create_error_response(message=f"An error occurred while generating the OTP:", data={str(e)},
                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return create_success_response(
            data=serializer.data, message="Registration successful.", status_code=status.HTTP_201_CREATED)


class Step2RegistrationView(generics.UpdateAPIView):
    serializer_class = Step2Serializer

    def get_object(self):
        return self.request.user.profile


class Step3MechanicRegistrationView(generics.UpdateAPIView):
    serializer_class = Step3MechanicSerializer

    def get_object(self):
        return self.request.user.profile


class Step3OwnerRegistrationView(generics.UpdateAPIView):
    serializer_class = Step3OwnerSerializer

    def get_object(self):
        return self.request.user
