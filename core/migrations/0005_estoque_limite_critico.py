# Generated by Django 5.1.4 on 2025-01-07 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_estoque_fluxogastos'),
    ]

    operations = [
        migrations.AddField(
            model_name='estoque',
            name='limite_critico',
            field=models.IntegerField(default=50),
        ),
    ]
