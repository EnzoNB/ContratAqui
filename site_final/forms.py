from django import forms
from .models import Servico,Categoria,SubCategoria
from ajax_select.fields import AutoCompleteSelectField



class ServicoForm(forms.ModelForm):
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
    subcategoria = AutoCompleteSelectField('subcategoria', required=False)

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
