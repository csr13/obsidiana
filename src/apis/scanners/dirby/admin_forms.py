from django import forms

from apis.utils.rules import ScannersRules

from .models import DirBy


class DirbpyAdminForm(forms.ModelForm, ScannersRules):

    def clean_target(self):
        user = self.cleaned_data.get("user")
        if user is None:
            raise forms.ValidationError("User Field is required")
        ok, target = self.dirby_rules(self.cleaned_data.get("target"))
        if not ok:
            raise forms.ValidationError(target) from None
        if DirBy.objects.filter(
            target=target,
            user__pk=self.cleaned_data["user"].pk
        ).exists():
            raise forms.ValidationError("This target already exists") from None
        return target
