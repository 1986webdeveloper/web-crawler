"""
    import needed things
"""
from user.forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect


class RegistrationView(FormView):
    """
        RegistrationView
    """
    form_class = NewUserForm
    template_name = 'user/register.html'

    def dispatch(self, request, *args, **kwargs):
        """
                dispatch
        """
        if request.user.is_authenticated:
            return redirect(reverse("user:login"))
        return super(RegistrationView, self).dispatch(request)

    def form_valid(self, form):
        """
            form_valid
        """
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return redirect(reverse("domain:dashboard"))


class LoginView(View):
    """
         LoginView
    """
    def dispatch(self, request, *args, **kwargs):
        """
                dispatch
        """
        if request.user.is_authenticated:
            return redirect(reverse("domain:dashboard"))
        return super(LoginView, self).dispatch(request)

    def get(self, request):
        """
          Get User
        """
        return render(request, 'user/login.html', {'form': AuthenticationForm})

    def post(self, request):
        """
           post data of user
        """
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                return render(
                    request,
                    'user/login.html',
                    {'form': form, 'invalid_creds': True}
                )

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'user/login.html',
                    {'form': form, 'invalid_creds': True}
                )
            login(request, user)
            return redirect(reverse("domain:dashboard"))
        return render(request, 'user/login.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    """
        LogoutView
    """
    def get(self, request):
        """
            get user for log out
        """
        logout(request)
        return redirect(reverse('user:login'))
