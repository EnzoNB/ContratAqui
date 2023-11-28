# Generated by Django 4.2.7 on 2023-11-26 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_final', '0002_category_post_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('categoria_pai', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias', to='site_final.categoria')),
            ],
        ),
    ]
