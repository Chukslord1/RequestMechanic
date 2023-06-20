from rest_framework import serializers, exceptions, fields

from .models import WorkExperience, Education, LicenseAndCertification, VolunteerExperience, ProfileView, SocialProfile
from userauth.models import User, UserProfile

from userauth.serializers import UserProfileSerializer

from rest_framework import status

import json


class WorkExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkExperience
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(
            instance.user, context={'request': self.context.get('request')}).data['id']
        return response


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(
            instance.user, context={'request': self.context.get('request')}).data['id']
        return response


class LicenseAndCertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LicenseAndCertification
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(
            instance.user, context={'request': self.context.get('request')}).data
        return response


class VolunteerExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = VolunteerExperience
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserProfileSerializer(
            instance.user, context={'request': self.context.get('request')}).data
        return response


class SocialProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialProfile
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # response['user'] = UserProfileSerializer(instance.user, context = {'request': self.context.get('request')}).data
        response['current_industry'] = WorkExperienceSerializer(instance.current_industry, context={
                                                                'request': self.context.get('request')}).data['organization_name']
        response['current_academia'] = EducationSerializer(instance.current_academia, context={
                                                           'request': self.context.get('request')}).data['organization_name']
        return response


class ProfileViewSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileView
        fields = '__all__'
