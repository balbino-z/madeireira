# Generated by Django 5.1.4 on 2024-12-30 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Madeira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('qualidade', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=50)),
                ('tamanho', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('metragens', models.FloatField()),
                ('madeira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.madeira')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pedido', models.DateField()),
                ('data_inicio', models.DateField()),
                ('data_entrega', models.DateField()),
                ('quantidade', models.IntegerField()),
                ('madeira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.madeira')),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_venda', models.DateField()),
                ('quantidade_vendida', models.IntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pedido')),
            ],
        ),
    ]
