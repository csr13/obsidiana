import logging

from django.contrib import admin
from django.utils.html import mark_safe

from .models import Scan

from admin_extend.admin import my_admin


logger = logging.getLogger(__name__)


class ScanAdminModel(admin.ModelAdmin):
    list_display = [
        "target_display",
        "scanner",
        "status",
        "created_at",
        "uid",
    ]
    list_filter = ["created_at"]
    fieldsets = [
        (
            "Scan Information",
            {
                "fields" : ["uid", "target", "status"],
                "classes" : ["extrapretty", "wide"]
            }
        ),
        (
            "Dates",
            {
                "fields" : ["created_at"],
                "classes" : ["extrapretty", "wide"]
            }
        ),
        (
            "Meta Data",
            {
                "fields" : ["metadata"],
                "description" : "Meta data 4 the this scan instance"
            }
        ),
        (
            "Human Readable Report Summary",
            {
                "fields" : ["descriptive_text_report"],
            }
        ),
        (
            "Raw JSON Data",
            {
                "fields" : ["meta", "data"],
                "classes" : ["extrapretty", "collapse"],
                "description" : "Raw JSON display."
            }
        )
    ]
    readonly_fields = [
        "scanner", 
        "target",
        "metadata",
        "status",
        "descriptive_text_report",
        "created_at"
    ]
    
    @admin.display(description="Target")
    def target_display(self, obj):
        return "ID: %s | %s" % (obj.pk, self.target(obj))
    
    @admin.display(description="Scanner")
    def scanner(self, obj):
        return obj.meta.get('scanner')
    
    def target(self, obj):
        scanner = obj.meta.get('scanner')
        scanner_pk = obj.meta.get('parent_scan_pk')
        scanner_model = Scan.map_scan_to_scanner_model(scanner)
        if scanner_model is None:
            return "Faulty scanner model query"
        try:
            parent_scan = scanner_model.objects.get(pk=scanner_pk)
            target = parent_scan.target
        except scanner_model.DoesNotExist:
            return "faulty target"
        return target

    @admin.display(description="Normalized Metadata")
    def metadata(self, obj):
        blob =  """
        <div style='margin: 0;'>
            <br>
            <p>
                Scanner: %s<br>
                <hr>
                Target: %s<br>
            </p>
        </div>
        """ % (
            self.scanner(obj), 
            self.target(obj),
        )
        return mark_safe(blob)

    def descriptive_text_report(self, obj):
        scanner = self.scanner(obj)
        if scanner == "wafw00f":
            report = obj.wafw00f_text_report()
        elif scanner == "sslyze":
            report = obj.sslyze_text_report()
        else:
            report = "Scanner report not ready yet."
        return mark_safe("<pre style='margin: 0;'>%s</pre>" % report)


my_admin.register(Scan)
