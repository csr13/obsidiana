import logging

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from apis.scanners.scan.models import Scan


logger = logging.getLogger(__name__)


class WafWoof(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    target = models.CharField(max_length=255, null=True)
    scans = models.ManyToManyField(Scan, blank=True)
    date_created = models.DateTimeField(default=now)
    
    class Meta:
        verbose_name = "WafW00f Target"
        verbose_name_plural = "WafW00f Targets"
        ordering = ("-date_created",)
    
    @classmethod
    def create_wafwoof_scan(cls, username, target):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            WafWoof.objects.create(
                user=user,
                target=target,
            )
        except Exception as error:
            logger.exception(str(error))
            return False
        return True
    
    def __str__(self):
        return f'Scan for user: {self.user} - Target: {self.target}'
