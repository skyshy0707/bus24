from django.db import models

from api.models import User
# Create your models here.

class Device(models.Model):

    fingerprint = models.CharField(verbose_name="Отпечаток устройства", max_length=64)
    ip = models.CharField(verbose_name="ip адрес", max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["fingerprint", "ip"],
                name="device"
            )
        ]

class UserDevice(models.Model):

    user = models.ForeignKey(verbose_name="Кто пользуется", to=User, on_delete=models.CASCADE)
    device = models.ForeignKey(verbose_name="Из какого устройства", to=Device, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "device_id"],
                name="whose"
            )
        ]