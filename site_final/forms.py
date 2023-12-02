from django import forms
from .models import Servico,Categoria,SubCategoria
from ajax_select.fields import AutoCompleteSelectField



class ServicoForm(forms.ModelForm):
    subcategoria = AutoCompleteSelectField('subcategoria', required=False)

    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'categoria', 'subcategoria', 'preco']
        labels = {
            'nome': 'Nome do Serviço',
            'descricao': 'Descrição do Serviço',
            'categoria': 'Categoria do Serviço',
            'subcategoria': 'Subcategoria do Serviço',
            'preco': 'Preço do Serviço',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira aqui o nome do serviço'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Insira aqui a descrição do serviço'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'subcategoria': forms.Select(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Insira aqui o preço do serviço'}),
        }

class ServicoUpdateForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'categoria', 'subcategoria', 'preco']
        labels = {
            'nome': 'Nome do Serviço',
            'descricao': 'Descrição do Serviço',
            'categoria': 'Categoria do Serviço',
            'subcategoria': 'Subcategoria do Serviço',
            'preco': 'Preço do Serviço',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira aqui o nome do serviço'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Insira aqui a descrição do serviço'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'subcategoria': forms.Select(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Insira aqui o preço do serviço'}),
        }

