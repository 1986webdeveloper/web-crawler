"""
    import needed things
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from domain.forms import DomainForm
from domain.models import Domain
from domain.tasks import scrapp_url_in_domain


class DashboardView(LoginRequiredMixin, ListView):
    """
        DashboardView
    """
    template_name = 'domain/dashboard.html'
    paginate_by = 10

    def get_queryset(self):
        """
            For getting get_context_data
        """
        return Domain.objects.filter(user=self.request.user).order_by('-created_at')


def funct(request):
    """
        funct for redirecting to dashboard
    """
    return redirect(reverse("domain:dashboard"))


class CreateDomainView(LoginRequiredMixin, CreateView):
    """
        CreateDomainView for creating Domain
    """
    template_name = "domain/create.html"
    form_class = DomainForm
    success_url = reverse_lazy("domain:dashboard")

    def form_valid(self, form):
        """
             Form validation
        """
        name = form.cleaned_data["name"]
        if self.request.user.domains.filter(name=name, status__in=[0,1]).exists():
            form.add_error("name", "Report generate is in progress.")
            return self.form_invalid(form)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        scrapp_url_in_domain.delay(obj.id)
        return HttpResponseRedirect(self.success_url)
