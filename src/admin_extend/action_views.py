import logging
import threading

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from admin_extend.mixins import AdminExtendedActionView
from apis.scanners.dirby.tasks import dirby_task
from apis.scanners.sslyze.tasks import sslyze_task
from apis.scanners.wafw00f.tasks import wafwoof_task
from docker.docker_exec import DockerExec


logger = logging.getLogger(__name__)


class ScannerAdminAction(AdminExtendedActionView):

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        scan_type = kwargs["type"]
        scanner = kwargs["scanner"]
        username = request.user.username
        if scanner not in settings.SCANNERS_AVAILABLE_LIST:
            messages.info(request, "Invalid option")
            return HttpResponseRedirect(reverse("admin:index"))
        if scanner == "dirby":
            dirby_task(username, pk, scan_type)
            redirect_url = reverse("admin:dirby_dirby_change", args=(pk,))
        elif scanner == "sslyze":
            sslyze_task(username, pk, scan_type)
            redirect_url = reverse("admin:sslyze_sslyze_change", args=(pk,))
        elif scanner == "wafwoof" or scanner == "wafw00f":
            wafwoof_task(username, pk, scan_type)
            redirect_url = reverse("admin:wafw00f_wafwoof_change", args=(pk,))
        messages.info(request, "Scan has been sent to worker")
        return HttpResponseRedirect(redirect_url)
