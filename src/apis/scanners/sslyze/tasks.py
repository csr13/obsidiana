import json
import logging

from celery import shared_task
from django.db import transaction

from apis.scanners.scan.models import Scan
from docker.docker_exec import DockerExec
from .models import SSLyze

logger = logging.getLogger(__name__)


@shared_task
def sslyze_task(username, pk, scan_type):
    try:
        logger.info("SSlyze task started")
        obj = SSLyze.objects.get(user__username=username, pk=pk)
        scan = Scan.objects.create()
        obj.scans.add(scan)
        obj.save()
        data = {
            'obj' : obj,
            'scan_type' : scan_type, 
            'scan_obj': scan
        }
        logger.info("Running sslyze action")
        DockerExec.sslyze_task(data)
    except Exception as error:
        logger.error(str(error))
        return False
    return True
