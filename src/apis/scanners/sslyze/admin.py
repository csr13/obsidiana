from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import mark_safe

from apis.scanners.sslyze.models import SSLyze
from .admin_forms import SSLyzeAdminForm

from admin_extend.admin import my_admin


class AdminSSLyze(admin.ModelAdmin):
    form = SSLyzeAdminForm
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
        SSLyze can analyze the SSL/TLS configuration of a server by connecting to it,
        in order to ensure that it uses strong encryption settings (certificate, cipher suites,
        elliptic curves, etc.), and that it is not vulnerable to known TLS attacks 
        (Heartbleed, ROBOT, OpenSSL CCS injection, etc.).
        """
        return mark_safe("<pre>%s</pre>" % description)
 
    @admin.display(description="SSLyze scans for this target")
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
            "<ol style='margin: 0;'><hr>%s</ol>" % "".join(
                list_items
            )
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
                args=("sslyze", "simple", obj.pk)
            ),
        )
        full_scan_a = "<a style='%s' href='%s'>Run Heavy Scan</a>" % (
            a_style,
            reverse(
                "admin_extend:admin-scan", 
                args=("sslyze", "full", obj.pk)
            ),
        )
        return mark_safe(
            "<nav>%s%s</nav>" % (
                simple_scan_a, 
                full_scan_a
            )
        )


my_admin.register(SSLyze)
