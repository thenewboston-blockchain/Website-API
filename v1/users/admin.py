# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models.user import User
from .models.user_earnings import UserEarnings

admin.site.register(UserEarnings)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password',
                    'account_number',
                    'display_name',
                    'github_username',
                    'profile_image',
                    'slack_username',
                    'is_email_verified',
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
        'created_date',
        'last_login',
    )
    search_fields = (
        'email',
    )
    ordering = (
        'email',
    )
