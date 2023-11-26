from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
    
