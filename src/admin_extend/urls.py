from django.urls import re_path

from admin_extend import action_views

app_name = "admin_extend"

urlpatterns = [
    re_path(
        r'^/admin-scan/(?P<scanner>\w+)/(?P<type>\w+)/(?P<pk>\d+)$', 
        view=action_views.ScannerAdminAction.as_view(),
        name='admin-scan'
    ),
]
