import datetime
import logging
import sys

from django.core.management.base import BaseCommand

from proxies.models import ProxyConfig


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Configure the main proxy (tor) from the docker services"
    
    main_config = {
        "schema" : "https",
        "protocol" : "http",
        "host" : "10.10.10.8",
        "port" : 8888,
        "auth" : "NOAUTH",
        "is_active" : True,
        "meta" : {
            "country_code" : "N/A",
            "region" : "N/A",
            "anonymity" : "moderate",
            "last_checked" : datetime.datetime.now().timestamp(),
            "is_main" : True
        }
    }

    def add_arguments(self, parser):
        return None

    def handle(self, *args, **kwargs):
        if ProxyConfig.objects.filter(
            host=self.main_config.get("host")
        ).exists():
            self.stdout.write(self.style.SUCCESS("Main ProxyConfig already exists"))
            sys.exit(0)
        ProxyConfig.objects.create(**self.main_config)
        self.stdout.write(self.style.SUCCESS("Main ProxyConfig Created"))
        sys.exit(0)

