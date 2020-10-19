from v1.third_party.django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
