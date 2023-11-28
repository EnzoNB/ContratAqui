from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView
from .forms import RegisterUserForm, CustomAuthenticationForm,PerfilForm
from site_final.models import Perfil
from django.urls import reverse_lazy

class UserRegisterView(generic.CreateView):
    form_class = RegisterUserForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"

class UserEditView(generic.UpdateView):
    form_class = PerfilForm
    template_name = "registration/update_register.html"
    success_url = reverse_lazy('home')

    def get_object(self):
        # Tenta obter o perfil do usuário atual
        perfil = Perfil.objects.filter(user=self.request.user)
        if perfil.exists():
            # Se o perfil existir, retorna o perfil
            return perfil.first()
        else:
            # Se o perfil não existir, cria um novo perfil
            return Perfil(user=self.request.user)
