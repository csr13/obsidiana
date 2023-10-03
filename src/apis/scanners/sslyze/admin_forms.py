from django import forms

from apis.utils.rules import ScannersRules
from .models import SSLyze


class SSLyzeAdminForm(ScannersRules, forms.ModelForm):
    
    def clean_target(self):
        user = self.cleaned_data.get("user")
        if user is None:
            raise forms.ValidationError("User field is required.")
        ok, target = self.sslyze_rules(
            self.cleaned_data["target"]
        )
        if not ok:
            raise forms.ValidationError(target) from None
        if SSLyze.objects.filter(
            target=target, 
            user__pk=self.cleaned_data["user"].pk
        ).exists():
            raise forms.ValidationError("This target already exists.") from None
        return target
