import logging

import requests
from django.contrib import admin
from django.utils.html import mark_safe

from proxies.models import ProxyConfig


logger = logging.getLogger(__name__)


@admin.register(ProxyConfig)
class AdminProxyConfig(admin.ModelAdmin):
    list_display = [
        "host",
        "schema_normalized",
        "port",
        "as_url",
        "is_active",
    ]
    fieldsets = (
        (
            "Model Information",
            {
                "fields" : [
                    "host", 
                    "port", 
                    "schema",
                    "protocol",
                    "schema_normalized", 
                    "is_active", 
                    "as_url",
                ],
                "classes" : ["extrapretty"],
                "description" : "Proxy information, mostly read only, some options"
            }
        ),
        (
            "Authentication (if applicable)",
            {
                "fields" : [
                    "auth", 
                    "username", 
                    "password"
                ],
                "classes" : ["extrapretty"],
                "description" : "Configure username and password for basic auth proxy"
            }
        ),
        (
            "Meta data",
            {
                "fields" : ["meta"], 
                "classes" : ["collapse"]
            }
        ),
    )
    readonly_fields = [
        "host",
        "schema_normalized",
        "as_url",
    ]

    @admin.display(description="Proxy schema")
    def schema_normalized(self, obj):
        return obj.schema
    
    @admin.display(description="Ip used for proxy")
    def tor_proxy_ip(self, obj):
        proxy_ip = ProxyConfig.true_proxy_ip(obj)
        return proxy_ip
