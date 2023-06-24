from django.db import models
from userauth.models import UserProfile
import datetime
from django.db.models import F


class WorkExperience(models.Model):

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='work_experience')
    organization_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    start_date = models.DateField(default=datetime.date.today)  # yyyy-mm-dd
    end_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'

    class Meta:
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'
        ordering = ('end_date', 'start_date', '-id')  # 2019 < 2020
        app_label = 'userprofile'


class Education(models.Model):

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='education')
    organization_name = models.CharField(max_length=50)
    start_date = models.DateField(default=datetime.date.today)  # yyyy-mm-dd
    end_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'

    class Meta:
        verbose_name = 'Academic '
        verbose_name_plural = 'Academics'
        ordering = ('-start_date',)
        app_label = 'userprofile'


class LicenseAndCertification(models.Model):

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=50)
    organization_name = models.CharField(max_length=50)
    issue_date = models.DateField(default=datetime.date.today)  # yyyy-mm-dd
    expiration_date = models.DateField(blank=True, null=True, default=None)
    credential_id = models.TextField(max_length=30, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.certification_name}'

    class Meta:
        verbose_name = 'License And Certification'
        verbose_name_plural = 'License And Certifications'
        ordering = ('-issue_date',)
        app_label = 'userprofile'


class VolunteerExperience(models.Model):
    ROLE = (
        ('Animal Welfare', 'Animal Welfare'),
        ('Arts and Culture', 'Arts and Culture'),
        ('Children', 'Children'),
        ('Civil Rights and Social Action',
         'Civil Rights and Social Action'),
        ('Economic Empowerment', 'Economic Empowerment'),
        ('Education', 'Education'),
        ('Environment', 'Environment'),
        ('Health', 'Health'),
        ('Human Rights', 'Human Rights'),
        ('Politics', 'Politics'),
        ('Poverty Alleviation', 'Poverty Alleviation'),
        ('Veteran Support', 'Veteran Support'),
        ('Social Services', 'Social Services'),
        ('Science and Technology', 'Science and Technology'),
    )

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='volunteer_experience')
    organization_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    cause = models.CharField(choices=ROLE, default=None, max_length=50)
    start_date = models.DateField(default=datetime.date.today)  # yyyy-mm-dd
    end_date = models.DateField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.organization_name}'

    class Meta:
        verbose_name = 'Volunteer Experience'
        verbose_name_plural = 'Volunteer Experiences'
        ordering = ('-start_date',)
        app_label = 'userprofile'


# Social Profile

class SocialProfile(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='social_profile')

    bio = models.TextField(blank=True, null=True)
    tagline = models.CharField(max_length=60, blank=True, null=True)
    background_photo = models.ImageField(
        upload_to='background/', blank=True, null=True, max_length=1048576)
    dob = models.DateField(blank=True, null=True, default=None)
    profile_url = models.TextField(blank=True, null=True)

    current_industry = models.OneToOneField(
        WorkExperience, blank=True, null=True, on_delete=models.SET_NULL, default=None, related_name='current_work')
    current_academia = models.OneToOneField(
        Education, blank=True, null=True, on_delete=models.SET_NULL, default=None, related_name='current_academic')

    viewer_list = models.ManyToManyField(UserProfile, through='ProfileView')

    is_private = models.BooleanField(default=False)
    completely_private = models.BooleanField(default=False)
    semi_private = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} > {self.tagline}'

    class Meta:
        verbose_name = 'Social Profile'
        verbose_name_plural = 'Social Profiles'
        app_label = 'userprofile'


class ProfileView(models.Model):
    viewer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='viewed')
    profile = models.ForeignKey(
        SocialProfile, on_delete=models.CASCADE, related_name='views')
    viewed_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.viewer.first_name} {self.viewer.last_name} > {self.profile.user.first_name} {self.profile.user.last_name}'

    class Meta:
        verbose_name = 'Profile View'
        verbose_name_plural = 'Profile Views'
        # ordering = ('-date_viewed','user')
        app_label = 'userprofile'
