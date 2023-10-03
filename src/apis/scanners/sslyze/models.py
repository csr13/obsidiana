from django.db import models
from django.utils.timezone import now

from apis.scanners.scan.models import Scan



class SSLyze(models.Model):
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, null=True
    )
    target = models.CharField(max_length=255, null=True)
    scans = models.ManyToManyField(Scan, blank=True)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)
    
    class Meta:
        ordering = ("-date_created",)
        verbose_name = "SSLyze Target"
        verbose_name_plural = "SSLyze Targets"

    def __str__(self):
        return f'Scan for user: {self.user} - Target: {self.target}'
