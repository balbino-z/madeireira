# Generated by Django 5.1.4 on 2025-02-16 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_estoque_limite_critico'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedido',
            options={'ordering': ['-id']},
        ),
    ]
