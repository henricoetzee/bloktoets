# Generated by Django 4.2.6 on 2023-12-02 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloktoets', '0004_packaging_stock_on_hand_products_stock_on_hand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packaging',
            name='stock_on_hand',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='products',
            name='stock_on_hand',
            field=models.FloatField(default=0),
        ),
    ]
