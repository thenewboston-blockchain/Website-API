# -*- coding: utf-8 -*-
import uuid

from django.db.models import CharField, URLField, UUIDField
from thenewboston.constants.network import VERIFY_KEY_LENGTH
from thenewboston.models.created_modified import CreatedModified

from v1.third_party.django.contrib.auth.models import AbstractUser


class User(CreatedModified, AbstractUser):
    uuid = UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    account_number = CharField(max_length=VERIFY_KEY_LENGTH)
    display_name = CharField(max_length=250)
    github_username = CharField(blank=True, max_length=250)
    profile_image = URLField(blank=True, max_length=500)
    slack_username = CharField(blank=True, max_length=250)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f'#{self.pk}: {self.display_name}'
