from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


class AdminExtendedActionView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.info(request, "Fuck off")
            return HttpResponseRedirect(
                reverse("fuck-off")
            )
        return super().dispatch(request, *args, **kwargs)


