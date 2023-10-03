import logging
from django.contrib import admin

from django.shortcuts import reverse
from django.utils.html import mark_safe

from .models import WafWoof
from .admin_forms import WafWoofAdminForm


logger = logging.getLogger(__name__)


@admin.register(WafWoof)
class AdminWafWoof(admin.ModelAdmin):
    form = WafWoofAdminForm
    list_display = [
        "target", 
        "date_created",
    ]
    list_filter = [
        "date_created"
    ]
    fieldsets = [
        (
            "Scanner Information",
            {
                "fields" : ["scanner_information"], 
                "classes" : ["extrapretty"]
            }
        ),
        (
            "Main Info", 
            {
                "fields" :  ["user", "target"],
                "classes" : ["extrapretty"]
            }
        ),
        (
            "Scan Actions",
            {
                "fields" : ["scans_panel"],
                "classes" : ["extrapretty"]
            }
        ),
        (
            "Scans for this target", 
            {
                "fields" :  ["list_of_scans",],
                "classes" : ["extrapretty"]
            }
        ),
    ]
    readonly_fields = [
        "list_of_scans", 
        "scans_panel",
        "scanner_information"
    ]

    @admin.display(description="Information about scanner.")
    def scanner_information(self, obj):
        description = """
        WafWoof Scans are Web Application Firewall Scanners, these are firewalls
        that sit infront of a website, sometimes even before the reverse proxy
        an example of a WAF is Cloudflare. A WAF checks incomming requests, filters
        and allows certain clients to pass the first check, sometimes, a reverse
        proxy sitting behind a waf is the secondary step, sometimes, most often, 
        its not, when doing reconnaisance it's important to do topology of the
        target.
        """
        return mark_safe("<pre>%s</pre>" % description)
 
    @admin.display(description="WafWoof links")
    def list_of_scans(self, obj):
        list_items = [
            """
            <br>
            <li>
              <a href='%s' style='margin-bottom: 20px;'>Target: %s</a>
              <br>
              <span>Status: %s</span>
              <br>
              <span>Start Time: %s</span>
              <br>
              <span>End Time: %s</span>
            </li>
            <br><hr>
            """ % (
                reverse("admin:scan_scan_change", args=(each.pk,)),
                obj.target,
                "<span>%s</span>" % each.normalize_status,
                each.created_at,
                each.end_time
            ) for each in obj.scans.all()
        ]
        return mark_safe(
            "<ol style='margin: 0;'><hr>%s</ol>" % "".join(list_items)
        )

    @admin.display(description="Scans Panel")
    def scans_panel(self, obj):
        if obj.pk is None:
            return (
                "Create the target first and the return to this page to begin"
                " scanning the target."
            )
        a_style = """
        background-color: var(--default-button-bg);
        color: white;
        padding: 10px;
        margin: 5px;
        """
        simple_scan_a = "<a style='%s' href='%s'>Run Simple Scan</a>" % (
            a_style,
            reverse(
                "admin_extend:admin-scan", 
                args=("wafwoof", "simple", obj.pk)
            ),
        )
        full_scan_a = "<a style='%s' href='%s'>Run Heavy Scan</a>" % (
            a_style,
            reverse(
                "admin_extend:admin-scan", 
                args=("wafwoof", "full", obj.pk)
            ),
        )
        return mark_safe(
            "<nav>%s%s</nav>" % (
                simple_scan_a, 
                full_scan_a
            )
        )
