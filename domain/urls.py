from django.urls import path
from domain.views import DashboardView, funct, CreateDomainView

app_name = "domain"
urlpatterns = [
    path("", funct, name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("domain/add/", CreateDomainView.as_view(), name="add"),
]