from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView
from domain.forms import DomainForm
from domain.models import Domain


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'domain/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data()
        context["domains"] = Domain.objects.filter(user=self.request.user)
        return context


def funct(request):
    return redirect(reverse("domain:dashboard"))


class CreateDomainView(LoginRequiredMixin, CreateView):
    template_name = "domain/create.html"
    form_class = DomainForm
    success_url = reverse_lazy("domain:dashboard")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        if self.request.user.domains.filter(name=name).exists():
            form.add_error("name", "This domain exist.")
            return self.form_invalid(form)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)

