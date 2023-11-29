# Generated by Django 4.2.6 on 2023-11-25 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Packaging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('scale_code', models.CharField(max_length=32)),
                ('packing_qty', models.FloatField()),
                ('cost', models.FloatField()),
                ('unit_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Packaging_relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloktoets.packaging')),
            ],
        ),
        migrations.CreateModel(
            name='Product_relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('scale_code', models.CharField(max_length=32)),
                ('packing_qty', models.FloatField()),
                ('cost', models.FloatField()),
                ('unit_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('scale_code', models.CharField(max_length=32)),
                ('cost_per_unit', models.FloatField()),
                ('gross_profit', models.FloatField()),
                ('selling_price', models.FloatField()),
                ('ingredients', models.ManyToManyField(blank=True, related_name='used_in', through='bloktoets.Product_relation', to='bloktoets.products')),
                ('packaging', models.ManyToManyField(blank=True, related_name='used_in', through='bloktoets.Packaging_relation', to='bloktoets.packaging')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bloktoets.store')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe_relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_in_recipe', to='bloktoets.recipe')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients_used', to='bloktoets.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bloktoets.recipebook'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_ingredients',
            field=models.ManyToManyField(blank=True, through='bloktoets.Recipe_relation', to='bloktoets.recipe'),
        ),
        migrations.AddField(
            model_name='products',
            name='recipe_book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bloktoets.recipebook'),
        ),
        migrations.AddField(
            model_name='products',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bloktoets.store'),
        ),
        migrations.AddField(
            model_name='product_relation',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloktoets.products'),
        ),
        migrations.AddField(
            model_name='product_relation',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloktoets.recipe'),
        ),
        migrations.AddField(
            model_name='packaging_relation',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloktoets.recipe'),
        ),
        migrations.AddField(
            model_name='packaging',
            name='recipe_book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bloktoets.recipebook'),
        ),
        migrations.AddField(
            model_name='packaging',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bloktoets.store'),
        ),
    ]
