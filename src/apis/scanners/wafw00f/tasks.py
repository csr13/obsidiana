import json
import logging

from celery import shared_task
from django.db import transaction

from apis.scanners.scan.models import Scan
from docker.docker_exec import DockerExec
from .models import WafWoof

logger = logging.getLogger(__name__)


@shared_task
def wafwoof_task(username, pk, scan_type):
    try:
        obj = WafWoof.objects.get(user__username=username, pk=pk)
        scan = Scan.objects.create()
        obj.scans.add(scan)
        obj.save()
        data = {
            'obj' : obj,
            'scan_type' : scan_type, 
            'scan_obj': scan
        }
        DockerExec.wafwoof_task(data)
    except Exception as eror:
        logger.error(str(error))
        return False
    return True
