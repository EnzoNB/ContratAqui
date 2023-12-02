from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from site_final.models import Perfil
from site_final.models import DiaDaSemana


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(max_length=50, label='Primeiro nome')  
    last_name = forms.CharField(max_length=50, label='Último nome')  
    cpf = forms.CharField(max_length=14, label='CPF')
    cidade = forms.CharField(max_length=100, label='Cidade')
    username = forms.CharField(max_length=100, label='Nome de Login')
    password1 = forms.CharField(max_length=100, label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label='Confirme sua senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'cpf', 'cidade', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nome de Login')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)



choices_all=DiaDaSemana.objects.all().values_list('dia','dia')
choices_dynamic = []
for choice in choices_all:
    choices_dynamic.append(choice)
  

class PerfilForm(forms.ModelForm):
    dias_de_trabalho = forms.ModelMultipleChoiceField(queryset=DiaDaSemana.objects.all(), widget=forms.CheckboxSelectMultiple, label='Dias de trabalho')

    class Meta:
        model = Perfil
        fields = ['bio', 'foto_de_perfil', 'telefone', 'whatsapp', 'instagram', 'dias_de_trabalho', 'horario_entrada', 'horario_saida']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Insira aqui a sua biografia'}),
            'foto_de_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira aqui o seu telefone'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira aqui o seu whatsapp'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira aqui o seu instagram'}),
            'dias_de_trabalho': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'horario_entrada': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Insira aqui o horário de entrada'}),
            'horario_saida': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Insira aqui o horário de saída'}),
        }
