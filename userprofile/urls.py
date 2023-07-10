# from django.urls import path
# from userprofile import views
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('work/', views.WorkExperienceViewset.as_view(
#         {'get': 'list', 'post': 'create'}), name='work-experience-list'),
#     path('work/<int:pk>/', views.WorkExperienceViewset.as_view(
#         {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='work-experience-detail'),
#     path('education/', views.EducationViewset.as_view(
#         {'get': 'list', 'post': 'create'}), name='education-list'),
#     path('education/<int:pk>/', views.EducationViewset.as_view(
#         {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='education-detail'),
#     path('certification/', views.LicenseAndCertificationViewset.as_view(
#         {'get': 'list', 'post': 'create'}), name='certification-list'),
#     path('certification/<int:pk>/', views.LicenseAndCertificationViewset.as_view(
#         {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='certification-detail'),
#     path('volunteer/', views.VolunteerExperienceViewset.as_view(
#         {'get': 'list', 'post': 'create'}), name='volunteer-experience-list'),
#     path('volunteer/<int:pk>/', views.VolunteerExperienceViewset.as_view(
#         {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='volunteer-experience-detail'),
#     path('strength/', views.ProfileStrengthView.as_view(), name='profile-strength'),
#     path('get_work/<int:profile_id>/',
#          views.GetWorkView.as_view(), name='get-work'),
#     path('get_academic/<int:profile_id>/',
#          views.GetAcademicView.as_view(), name='get-academic'),
#     path('view/social_profile/', views.SocialProfileView.as_view(),
#          name='social-profile-view'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
