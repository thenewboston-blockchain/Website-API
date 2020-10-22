# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


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
                    'created_date',
                    'modified_date',
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
