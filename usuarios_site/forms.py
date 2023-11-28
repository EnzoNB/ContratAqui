from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    primeiro_nome = forms.CharField(max_length=50, label='Primeiro nome')
    ultimo_nome = forms.CharField(max_length=50, label='Último nome')
    cpf = forms.CharField(max_length=14, label='CPF')
    cidade = forms.CharField(max_length=100, label='Cidade')
    username = forms.CharField(max_length=100, label='Nome de Login')
    password1 = forms.CharField(max_length=100, label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label='Confirme sua senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'primeiro_nome', 'ultimo_nome', 'email', 'cpf', 'cidade', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nome de Login')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)