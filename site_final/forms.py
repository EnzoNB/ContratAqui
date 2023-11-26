from django import forms
from .models import Post, Comment,Category

choices_all=Category.objects.all().values_list('type','type')
choices_dynamic = []
for choice in choices_all:
    choices_dynamic.append(choice)



class PostForm(forms.ModelForm):
    Category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),widget=forms.CheckboxSelectMultiple, label = "Categorias")
    class Meta:
        model = Post 
        fields = ('título','tag_aba','autor','Category','corpo')

        widgets = {
            'título': forms.TextInput(attrs={'class': 'form-control',"placeholder":"Insira aqui o título de sua postagem"}),
            'tag_aba': forms.TextInput(attrs={'class': 'form-control',"placeholder":"Insira aqui a tag de sua postagem"}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'Category': forms.Select(choices=choices_dynamic, attrs={'class': 'form-control'}),
            'corpo': forms.Textarea(attrs={'class': 'form-control',"placeholder":"Insira aqui de sua postagem"}),
        }

class EditForm(forms.ModelForm):
    Category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),widget=forms.CheckboxSelectMultiple, label = "Categorias")
    class Meta:
        model = Post 
        fields = ('título','tag_aba','Category','corpo')

        widgets = {
            'título': forms.TextInput(attrs={'class': 'form-control',"placeholder":"Insira aqui o título de sua postagem"}),
            'tag_aba': forms.TextInput(attrs={'class': 'form-control',"placeholder":"Insira aqui a tag de sua postagem"}),
            'Category': forms.Select(choices=choices_dynamic, attrs={'class': 'form-control'}),
            'corpo': forms.Textarea(attrs={'class': 'form-control',"placeholder":"Insira aqui de sua postagem"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('nome','corpo')

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control',"placeholder":"Insira aqui o título de sua postagem"}),
            'corpo': forms.Textarea(attrs={'class': 'form-control',"placeholder":"Insira aqui de sua postagem"}),
        }