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

class Perfil(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    bio = models.TextField()
    foto_de_perfil = models.ImageField(null=True, blank=True,upload_to="imagens/perfil/")
    telefone = models.CharField(null=True, blank=True,max_length=11)
    whatsapp = models.CharField(null=True, blank=True,max_length=11)
    instagram = models.CharField(null=True, blank=True,max_length=25)

    
class SalaDeMensagens(models.Model):
    servico = models.ForeignKey('Servico', on_delete=models.CASCADE)
    clientes = models.ManyToManyField(User, related_name='salas_de_mensagens')
    identificador_sala = models.CharField(max_length=100, default='seila')

    def __str__(self):
        return f"Sala de Mensagens para {self.servico.nome}"

class Mensagem(models.Model):
    sala_de_mensagens = models.ForeignKey(SalaDeMensagens, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.autor.username} para {self.sala_de_mensagens.servico.nome}"

class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sala_de_mensagens = models.ForeignKey(SalaDeMensagens, on_delete=models.CASCADE)
    visualizada = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.usuario.username}"
    
class PropostaServico(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, related_name='propostas_feitas', on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, related_name='propostas_recebidas', on_delete=models.CASCADE)
    valor_proposta = models.DecimalField(max_digits=10, decimal_places=2)
    aceita = models.BooleanField(null=True, blank=True)
    recusada = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Proposta de {self.autor.username} para {self.servico.nome}"