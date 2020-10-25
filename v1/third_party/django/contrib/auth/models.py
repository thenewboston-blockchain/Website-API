from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db.models import BooleanField, EmailField
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    email = EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required.'),
        error_messages={
            'unique': _('A user with that email address already exists.'),
        },
    )
    is_staff = BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        abstract = True
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
