# Generated by Django 4.2.7 on 2023-11-28 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_final', '0004_servico'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='preco',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
