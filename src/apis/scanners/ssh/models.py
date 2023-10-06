from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from apis.scanners.scan.models import Scan


User = get_user_model()


class SshPrank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    meta = models.JSONField(default=dict, null=True)
    date_created = models.DateTimeField(default=now)

    class Meta:
        ordering = ("-date_created",)
        verbose_name = "Ssh Mass Scan"
        verbose_name_plural = "Ssh Mass Scans"

    def __str__(self):
        return self.date_created
