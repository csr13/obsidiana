from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import re_path, path, include

from django.conf import settings as base

from admin_extend.admin import my_admin as admin


urlpatterns = [
    re_path('^admin-actions', include('admin_extend.urls', namespace='admin_actions')),
    re_path('^admin/', admin.urls),
    re_path('^fuck-off\/', view=lambda request: HttpResponse(
            "Fuck off", content_type="text/html"
        )
    )
]


##########################################
# Api urls
# Comment to disable a specific scanner.
##########################################

api_urls = [
    path('scanners/', include(([
        path('scanvus/', include('apis.scanners.scanvus.urls', namespace='scanvus')),
        path('sslyze/', include('apis.scanners.sslyze.urls', namespace='sslyze')),
        path('wafwoof/', include('apis.scanners.wafw00f.urls', namespace='wafwoof')),
    ]))),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

