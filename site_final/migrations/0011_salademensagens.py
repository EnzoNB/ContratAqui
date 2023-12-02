# Generated by Django 4.2.7 on 2023-11-30 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_final', '0010_mensagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaDeMensagens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientes', models.ManyToManyField(related_name='salas_de_mensagens', to=settings.AUTH_USER_MODEL)),
                ('servico', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sala_de_mensagens', to='site_final.servico')),
            ],
        ),
    ]
