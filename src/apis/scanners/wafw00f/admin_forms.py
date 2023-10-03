from django import forms

from apis.utils.rules import ScannersRules
from .models import WafWoof


class WafWoofAdminForm(forms.ModelForm, ScannersRules):

    def clean_target(self):
        user = self.cleaned_data.get("user")
        if user is None:
            raise forms.ValidationError("User field is required.")
        ok, target = self.wafwoof_rules(
            self.cleaned_data["target"]
        )
        if not ok:
            raise forms.ValidationError(target) from None
        if WafWoof.objects.filter(
            target=target, 
            user__pk=self.cleaned_data["user"].pk
        ).exists():
            raise forms.ValidationError("This target already exists.") from None
        return target
