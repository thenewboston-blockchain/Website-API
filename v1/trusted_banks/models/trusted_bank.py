from uuid import uuid4

from django.core.cache import cache
from django.core.validators import MaxValueValidator
from django.db import models
from thenewboston.constants.network import PROTOCOL_CHOICES
from thenewboston.models.created_modified import CreatedModified


class TrustedBank(CreatedModified):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(65535)])
    protocol = models.CharField(choices=PROTOCOL_CHOICES, max_length=5)

    class Meta:
        verbose_name_plural = 'trusted banks'
        constraints = [
            models.UniqueConstraint(
                fields=['ip_address', 'port', 'protocol'],
                name='%(app_label)s_%(class)s_unique_ip_port_proto')
        ]

    def __str__(self):
        return f'#{self.pk}: {self.protocol}://{self.ip_address}:{self.port}'

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(TrustedBank, self).save(*args, **kwargs)
