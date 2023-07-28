from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    PasswordResetView,
    SendOTPView,
    SetNewPasswordView,
    UserRegisterView,
    VerifyOTPView,
    LoginPinView,
    LogoutView,
    DeleteAccountView,
    CarBrandCreateView,
    CarBrandListView,
    SupportingDocumentUploadView,
    Step1RegistrationView,
    Step2RegistrationView,
    Step3OwnerRegistrationView,
    Step3MechanicRegistrationView,
    UserRetrieveView
)

urlpatterns = [
    path("send-otp/", SendOTPView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    # path("register/", UserRegisterView.as_view()),
    path("login/", LoginView.as_view()),
    # path("login/pin/", LoginPinView.as_view()),
    path("password-reset/", PasswordResetView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<str:pk>/', UserRetrieveView.as_view(), name='user-detail'),

    # path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path("set-new-password/", SetNewPasswordView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path('car-brands/', CarBrandListView.as_view(), name='car-brand-list'),
    path('car-brands/create/', CarBrandCreateView.as_view(),
         name='car-brand-create'),
    path('supporting-documents/', SupportingDocumentUploadView.as_view(),
         name='supporting-document-upload'),
    path('registration/step1/', Step1RegistrationView.as_view(),
         name='registration-step1'),
    path('registration/step2/', Step2RegistrationView.as_view(),
         name='registration-step2'),
    path('registration/step3/mechanic/', Step3MechanicRegistrationView.as_view(),
         name='registration-step3-mechanic'),
    path('registration/step3/owner/', Step3OwnerRegistrationView.as_view(),
         name='registration-step3-owner'),
]
