from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView
from .forms import RegisterUserForm, CustomAuthenticationForm
from django.urls import reverse_lazy

class UserRegisterView(generic.CreateView):
    form_class = RegisterUserForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"
