import logging

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from apis.scanners.scan.models import Scan

logger = logging.getLogger(__name__)


class DirBy(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    target = models.CharField(max_length=255, null=True)
    scans = models.ManyToManyField(Scan, blank=True)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)
    
    class Meta:
        ordering = ("-date_created",)
        verbose_name = "Dirbpy Target"
        verbose_name_plural = "Dirbpy Targets"

    @classmethod
    def create_dirby_scan(cls, **data):
        """create a dirby scan result"""
        try:
            User = get_user_model()
            data["user"] = User.objects.get(data["user"])
            cls.objects.create(**data)
        except Exception as create_error:
            logger.info(str(create_error))
            return False
        return True

    def __str__(self):
        return f'Scan for user: {self.user} - Target: {self.target}'
