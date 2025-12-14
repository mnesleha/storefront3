from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from core.models import User


class HomeView(TemplateView):
    template_name = 'core/home.html'


class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:profile')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, 'Successfully logged in!')
        next_url = self.request.GET.get('next', 'core:profile')
        return redirect(next_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


class RegisterView(TemplateView):
    template_name = 'core/register.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'core/profile.html'
    login_url = '/login/'


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully logged out!')
        return redirect('core:home')
