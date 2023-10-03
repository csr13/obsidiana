import logging
import random

import requests
from django.db import models
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class ProxyConfig(models.Model):
    """
    Зареєструйте безкоштовні, платні чи інші проксі-сервери для використання під час
    певних сканувань на додаток до використання цього сканера на VPC, бажано в
    слов’янській країні, неподалік.
    """

    class SchemaChoices(models.TextChoices):
        HTTPS = _("https")
        HTTP = _("http")
        SOCKS5 = _("socks5")

    class ProxyAuthChoices(models.TextChoices):
        BASIC = "BASIC", _("basic")
        TOKEN = "TOKEN", _("token")
        NO_AUTH = "NOAUTH", _("no-auth")

    username = models.CharField(max_length=255, default="no-username", null=True)
    password = models.CharField(max_length=255, default="no-password", null=True)
    auth = models.CharField(
        max_length=255, 
        default=ProxyAuthChoices.NO_AUTH,
        choices=ProxyAuthChoices.choices
    )
    schema = models.CharField(
        max_length=255, 
        default=SchemaChoices.HTTP,
        choices=SchemaChoices.choices, 
    )
    protocol = models.CharField(
        max_length=255,
        default=SchemaChoices.HTTP,
        choices=SchemaChoices.choices
    )
    host = models.GenericIPAddressField(protocol="both", unique=True)
    port = models.IntegerField(default=9201)
    is_active = models.BooleanField(default=False)
    #######################################
    # Мета містить
    # {
    #     country_code: <код країни>,
    #     region : <регіон країни, якщо є>
    #     anonymity : <рівень анонімності>
    #     last_checked : <останній перевірений статус онлайн>
    # }
    #######################################
    meta = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Proxy"
        verbose_name_plural = "Proxies"

    @property
    def as_url(self):
        url = None
        if self.auth == "BASIC":
            url = "%s://%s:%s@%s:%s" % (
                self.protocol, 
                self.username, 
                self.password, 
                self.host, 
                self.port
            )
        elif self.auth == "NOAUTH":
            url = "%s://%s:%s" % (
                self.protocol, 
                self.host, 
                self.port
            )
        else:
            url = "not-implemented"
        return url

    @classmethod
    def available_proxies_as_url(cls):
        proxies = cls.objects.filter(
            is_active=True,  
            auth__in=["BASIC", "NOAUTH"]
        )
        return [x.as_url for x in proxies]
    
    @classmethod
    def get_random_proxy(cls):
        return random.choice(cls.available_proxies)
    
    @classmethod
    def true_proxy_ip(cls, obj):
        try:
            proxies = {}
            schema = obj.schema.lower()
            if schema == "https":
                proxies["https"] = obj.as_url
            elif schema == "http":
                proxies["http"] = obj.as_url
            else:
                proxies["http"] = obj.as_url
            ip = requests.get("https://api.ipify.org?format=json", proxies=proxies)
            if ip.status_code != 200:
                return "Unable to get proxy ip"
        except Exception as error:
            logger.error(str(error))
            return str(error)
        return ip.json().get("ip", "No IP returned from ipify.")

    def __str__(self):
        return self.as_url

