from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
from django.utils.translation import gettext_lazy as _
from microservices.expo_push_service import send_push_message
from .models import PushToken

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('username', 'phone_number',
         'email', 'password', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff', 'username')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Profile)


@admin.register(PushToken)
class PushTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'active')
    actions = ['send_push_notification']

    def send_push_notification(self, request, queryset):
        for push_token in queryset:
            if push_token.active:
                # Customize your push notification message here
                message = "Hello, this is a push notification!"
                try:
                    send_push_message(push_token.token, message)
                    self.message_user(
                        request, "Push notification sent successfully.")
                except Exception as e:
                    self.message_user(
                        request, f"Failed to send push notification: {str(e)}")
            else:
                self.message_user(
                    request, "Inactive push token. Skipping notification.")
    send_push_notification.short_description = "Send push notification"
