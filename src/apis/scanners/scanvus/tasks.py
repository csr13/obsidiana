"""
register scanvus's task for celery to autodiscover
"""
import logging

from celery import shared_task
from django.db import transaction

from .models import Scanvus


logger = logging.getLogger(__name__)


@shared_task
@transaction.atomic
def scanvus_task(
        ip_address: str, 
        username: str, 
        password: str, 
        key: str,
        api_user_username: str
    ):
    return None 
