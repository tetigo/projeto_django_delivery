# Generated by Django 4.0 on 2023-12-14 17:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CupomDesconto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=8, unique=True)),
                ('desconto', models.FloatField()),
                ('usos', models.IntegerField(default=0)),
                ('ativo', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='pedido',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 14, 43, 16, 927492)),
        ),
        migrations.AddField(
            model_name='pedido',
            name='cupom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedido.cupomdesconto'),
        ),
    ]
