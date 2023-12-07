# Generated by Django 4.2.7 on 2023-12-02 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_final', '0023_perfil_nota_media_perfil_numero_avaliacoes_avaliacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropostaAceita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concluida', models.BooleanField(default=False)),
                ('proposta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='proposta_aceita', to='site_final.propostaservico')),
            ],
        ),
    ]
