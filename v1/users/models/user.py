import uuid

from django.db.models import UUIDField
from thenewboston.models.created_modified import CreatedModified

from v1.third_party.django.contrib.auth.models import AbstractUser


class User(CreatedModified, AbstractUser):
    uuid = UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
