# Generated by Django 4.2.7 on 2023-11-28 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_final', '0007_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='instagram',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
