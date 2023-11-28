from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify



class Category(models.Model):
    type = models.CharField(max_length=255)
    descrição = models.TextField()

    def __str__(self):
        return self.type
    
    def get_absolute_url(self):
        return reverse('home')

class Post(models.Model):
    título = models.CharField(max_length=255)
    tag_aba = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    corpo = models.TextField()
    data_postagem = models.DateTimeField(auto_now_add=True)
    Category = models.ManyToManyField(Category)

    def __str__(self):
        return self.título + " | " + str(self.autor)
    
    def get_absolute_url(self):
        return reverse('article-detail',args=(str(self.id)))

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    corpo = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.título + " | " + str(self.nome)
###########################################################################################  
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome).title()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('categoria_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.nome


class SubCategoria(models.Model):
    categoria_pai = models.ForeignKey(Categoria, related_name='subcategorias', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('subcategoria_detail', kwargs={'categoria_slug': self.categoria_pai.slug, 'subcategoria_slug': self.slug})

    def __str__(self):
        return self.nome

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
