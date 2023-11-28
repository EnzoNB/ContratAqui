from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


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
    
    def __str__(self):
        return self.nome + " | Categoria: " + str(self.categoria_pai)

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return self.nome + " | SubCategoria: " + str(self.subcategoria)
