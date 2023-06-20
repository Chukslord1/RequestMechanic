from django.contrib import admin

from profile import models

admin.site.register(models.WorkExperience)
admin.site.register(models.Education)
admin.site.register(models.LicenseAndCertification)
admin.site.register(models.VolunteerExperience)
admin.site.register(models.SocialProfile)
admin.site.register(models.ProfileView)
