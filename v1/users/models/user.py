import uuid

from django.core.cache import cache
from django.db.models import BooleanField, CharField, URLField, UUIDField
from thenewboston.constants.network import VERIFY_KEY_LENGTH
from thenewboston.models.created_modified import CreatedModified

from v1.third_party.django.contrib.auth.models import AbstractUser


class User(CreatedModified, AbstractUser):
    uuid = UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    account_number = CharField(blank=True, max_length=VERIFY_KEY_LENGTH)
    display_name = CharField(max_length=250)
    github_username = CharField(blank=True, max_length=250)
    profile_image = URLField(blank=True, max_length=500)
    discord_username = CharField(blank=True, max_length=250)

    # Auth
    is_email_verified = BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f'#{self.pk}: {self.username}, {self.display_name}'

    @property
    def username(self):
        return self.email

    @property
    def first_name(self):
        return self.display_name

    @first_name.setter
    def first_name(self, val):
        self.display_name = val

    @property
    def last_name(self):
        return None

    @last_name.setter
    def last_name(self, val):
        pass

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(User, self).save(*args, **kwargs)
