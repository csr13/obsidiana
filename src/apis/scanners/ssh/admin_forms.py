from django import forms

from apis.scanners.ssh.models import SshPrank

class SshPrankForm(forms.ModelForm):
    discover_targets = forms.BooleanField()
    
    class Meta:
        model = SshPrank
        fields = ["user", "discover_targets"] 

