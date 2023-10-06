from django.contrib import admin

from apis.scanners.ssh.admin_forms import SshPrankForm
from apis.scanners.ssh.models import SshPrank


@admin.register(SshPrank)
class AdminSshPrank(admin.ModelAdmin):
    form = SshPrankForm 
