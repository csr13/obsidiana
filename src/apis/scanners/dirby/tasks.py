import logging

from celery import shared_task
from django.db import transaction

from apis.scanners.scan.models import Scan
from docker.docker_exec import DockerExec
from .models import DirBy


logger = logging.getLogger(__name__)


@shared_task
def dirby_task(pk):
    try:
        obj = DirBy.objects.get(pk=pk)
        scan = Scan.objects.create()
        obj.scans.add(scan)
        obj.save()
        data = {
            'obj' : obj,
            'scan_type' : scan_type, 
            'scan_obj': scan
        }
        DockerExec.dirby_task(data)
    except Exception as error:
        logger.info(str(error))
        return False
    return True
