# Generated by Django 4.2.6 on 2023-12-02 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloktoets', '0003_recipe_recipe_yield'),
    ]

    operations = [
        migrations.AddField(
            model_name='packaging',
            name='stock_on_hand',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='stock_on_hand',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
