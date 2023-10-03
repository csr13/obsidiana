import datetime
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_aware

from apis import scanners
from apis.scanners.scan.mixins import ScanParser
from helpers.random import random_uid

logger = logging.getLogger(__name__)


class Scan(models.Model, ScanParser):
    class StatusChoices(models.TextChoices):
        STARTED = "ST", _("Started")
        RUNNING = "RU", _("Running")
        DONE = "DO", _("Done")
        FAILED = "FL", _("Failed")
    uid = models.CharField(max_length=255, default=random_uid, null=True)
    meta = models.JSONField(default=dict, null=True)
    status = models.CharField(
        max_length=2,
        default=StatusChoices.STARTED,
        choices=StatusChoices.choices
    )
    data = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Scan"
        verbose_name_plural = "Scans"
    
    @property
    def normalize_status(self):
        if self.status == "DO":
            return "Complete"
        elif self.status == "RU":
            return "Running"
        elif self.status == "FL":
            return "Failed"
        elif self.status == "ST":
            return "Started"
        return "Unknown"

    @classmethod
    def map_scan_to_scanner_model(cls, scanner):
        if scanner == "wafw00f":
            return scanners.wafw00f.models.WafWoof
        elif scanner == "sslyze":
            return scanners.sslyze.models.SSLyze
        elif scanner == "dirpy" or scanner == "dirbpy":
            return scanners.dirby.models.DirBy
        return None

    @classmethod
    def save_scan_result(cls, meta, data, scan_obj):
        try:
            scan_obj.meta = meta
            scan_obj.data = data
            scan_obj.end_time = make_aware(datetime.datetime.now())
            scan_obj.save()
        except Exception as error:
            logger.info(str(error))
            return False
        return True

    def parent_scan(self):
        """
        деталі сканування батьківської цілі містяться в метаданих
        """
        parent_scan_pk = self.meta.get('parent_scan_pk')
        scanner = self.meta.get('scanner')
        if parent_scan_pk is None or scanner is None:
            return None, "No sufficient metadata to provide info"
        scanner_model = Scan.map_scan_to_scanner_model(scanner)
        if scanner_model is None:
            return None, "No mapping from scan to scanner."
        try: 
            parent_scan = scanner_model.objects.get(pk=parent_scan_pk)
        except (scanner_model.DoesNotExist, Exception) as error:
            return None, str(error)
        return parent_scan, scanner

    def __str__(self):
        parent_scan, msg = self.parent_scan()
        if not parent_scan:
            return msg
        scanner = msg
        return "Scan %s for Scanner %s | target %s" % (self.pk, scanner, parent_scan.target)
        
