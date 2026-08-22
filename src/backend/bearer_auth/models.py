from datetime import timedelta, timezone
import uuid

from django.db import models

from bearer_auth import settings
from device.models import UserDevice
from shared.utils import now

# Create your models here.


class Token(models.Model):

    id = models.UUIDField(verbose_name="jti", primary_key=True, default=uuid.uuid4, max_length=36)
    userdevice = models.ForeignKey(verbose_name="Владелец", to=UserDevice, on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name="Статус вывода из строя", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now=True)

    
    @property
    def expired(self):
        return self.created_at + timedelta(seconds=settings.EXPIRES_IN) < now(tzinfo=timezone.utc)
    
    @property
    def expired_refresh(self):
        return self.created_at + timedelta(seconds=settings.EXPIRES_REFRESH_IN) < now(tzinfo=timezone.utc)
