from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models.user import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password',
                ),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {
                'fields':
                (
                    'last_login',
                    'date_joined',
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
    list_display = (
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login',
    )
    search_fields = (
        'email',
    )
    ordering = (
        'email',
    )
