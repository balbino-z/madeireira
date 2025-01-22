# Generated by Django 5.1.4 on 2025-01-04 21:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_pedido_data_inicio_remove_pedido_madeira_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='pedido',
        ),
        migrations.AddField(
            model_name='pedido',
            name='quantidade',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='comprimento',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='data_entrega',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='data_pedido',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='endereco',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='espessura',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='largura',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='nome_cliente',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='telefone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='tipo',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='valor_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='valor_unitario',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Estoque',
        ),
        migrations.DeleteModel(
            name='Madeira',
        ),
        migrations.DeleteModel(
            name='Venda',
        ),
    ]
