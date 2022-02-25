"""
    import needed things
"""
from django.urls import path

from . import views

app_name = "user"
urlpatterns = [path("register/", views.RegistrationView.as_view(), name="register"),
               path('login/', views.LoginView.as_view(), name='login'),
               path('logout/', views.LogoutView.as_view(), name='logout'),
               ]
