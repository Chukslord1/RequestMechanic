from .models import WorkExperience, Education, LicenseAndCertification, VolunteerExperience, SocialProfile
from .serializers import WorkExperienceSerializer, EducationSerializer, LicenseAndCertificationSerializer, VolunteerExperienceSerializer, SocialProfileSerializer
from rest_framework import views, viewsets
from .permissions import IsAuthenticatedAndOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from userauth.models import UserProfile
from django.shortcuts import get_object_or_404


class SocialProfileView(views.APIView):

    def get(self, request):

        queryset = SocialProfile.objects.all()
        serialzer = SocialProfileSerializer(
            queryset, many=True, context={'request': request})
        return Response(serialzer.data, status=status.HTTP_200_OK)


class WorkExperienceViewset(viewsets.ViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

    def create(self, request):

        profile_id = request.data.get('user')
        update_tagline = request.data.get('update_tagline')
        social_profile = get_object_or_404(
            UserProfile, id=profile_id).social_profile

        if update_tagline:
            serializer = WorkExperienceSerializer(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                social_profile.tagline = f"{serializer.data['position']} at {serializer.data['organization_name']}"
                social_profile.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = WorkExperienceSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):

        instance = WorkExperience.objects.get('pk')
        social_profile = request.data.user.social_profile
        update_tagline = request.data.get('update_tagline')

        if update_tagline:
            serializer = WorkExperienceSerializer(
                instance, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                social_profile.tagline = f"{serializer.data['position']} at {serializer.data['organization_name']}"
                social_profile.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = WorkExperienceSerializer(
            instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = []
            # permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = []
        return [permission() for permission in permission_classes]


class EducationViewset(viewsets.ModelViewSet):

    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            # permission_classes = [IsAuthenticatedAndOwner]
            permission_classes = []
        elif self.action == 'list':
            permission_classes = []
        return [permission() for permission in permission_classes]


class LicenseAndCertificationViewset(viewsets.ModelViewSet):

    queryset = LicenseAndCertification.objects.all()
    serializer_class = LicenseAndCertificationSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class VolunteerExperienceViewset(viewsets.ModelViewSet):

    queryset = VolunteerExperience.objects.all()
    serializer_class = VolunteerExperienceSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticatedAndOwner]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class GetWorkView(views.APIView):

    def get(self, request, profile_id=None):

        user = get_object_or_404(UserProfile, id=profile_id)

        try:
            work_experience = user.work_experience.all()
            serializer = WorkExperienceSerializer(
                work_experience, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'No work experience yet'}, status=status.HTTP_400_BAD_REQUEST)


class GetAcademicView(views.APIView):

    def get(self, request, profile_id=None):
        user = get_object_or_404(UserProfile, id=profile_id)

        try:
            academic_experience = user.education.all()
            serializer = EducationSerializer(
                academic_experience, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'No academic experience yet'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileStrengthView(views.APIView):

    def get(self, request):
        user = get_object_or_404(UserProfile, id=request.user.profile.id)

        message = dict()
        profile_strength = 0

        avatar = user.avatar
        article = user.articles.count()
        connections = user.request_received.filter(has_been_accepted=True).count() + \
            user.request_sent.filter(has_been_accepted=True).count()
        try:
            skills = len(user.skills.skills_list)
        except:
            skills = 0

        work_experiences = user.work_experience.count()
        academics = user.education.count()
        bio = user.social_profile.bio

        if avatar:
            profile_strength += 1
            message['Profile Picture'] = True
        else:
            message['Profile Picture'] = False

        if connections > 20:
            profile_strength += 1
            message['Connections(20+)'] = True
        else:
            message['Connections(20+)'] = False

        if work_experiences:
            profile_strength += 1
            message['Work Experience'] = True
        else:
            message['Work Experience'] = False

        if academics:
            profile_strength += 1
            message['Academics'] = True
        else:
            message['Academics'] = False

        if bio:
            profile_strength += 1
            message['About'] = True
        else:
            message['About'] = False

        # if len(message) == 0:
        #     return Response({'detail': 'User has completed his profile.'}, status = status.HTTP_204_NO_CONTENT)
        return Response({'profile_strength': profile_strength, 'message': message}, status=status.HTTP_200_OK)
