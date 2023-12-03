from django.db import models

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class RecipeBook(models.Model):
    name = models.CharField(max_length=64, blank=False)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Products(models.Model):
    name = models.CharField(max_length=64, blank=False)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    recipe_book = models.ForeignKey(RecipeBook, on_delete=models.PROTECT, null=True)
    scale_code = models.CharField(max_length=32)
    packing_qty = models.FloatField()
    cost = models.FloatField()
    unit_price = models.FloatField()
    stock_on_hand = models.FloatField(default=00)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "scale_code": self.scale_code,
            "packing_qty": self.packing_qty,
            "cost": self.cost,
            "unit_price": self.unit_price,
            "stock_on_hand": self.stock_on_hand
        }
    

class Packaging(models.Model):
    name = models.CharField(max_length=64, blank=False)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    recipe_book = models.ForeignKey(RecipeBook, on_delete=models.PROTECT, null=True)
    scale_code = models.CharField(max_length=32)
    packing_qty = models.FloatField()
    cost = models.FloatField()
    unit_price = models.FloatField()
    stock_on_hand = models.FloatField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "scale_code": self.scale_code,
            "packing_qty": self.packing_qty,
            "cost": self.cost,
            "unit_price": self.unit_price,
            "stock_on_hand": self.stock_on_hand
        }
    

class Recipe(models.Model):
    name = models.CharField(max_length=64, blank=False)
    recipe_book = models.ForeignKey(RecipeBook, on_delete=models.PROTECT)
    scale_code = models.CharField(max_length=32)
    cost_per_unit = models.FloatField()
    gross_profit = models.FloatField()
    selling_price = models.FloatField()
    recipe_yield = models.FloatField()
    ingredients = models.ManyToManyField(
        Products,
        blank=True,
        through="Product_relation",
        through_fields=("recipe", "ingredient")
    )
    packaging = models.ManyToManyField(
        Packaging,
        blank=True,
        through="Packaging_relation",
        through_fields=("recipe", "ingredient")
    )
    recipe_ingredients = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        through="Recipe_relation",
        through_fields=("recipe", "ingredient")
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "scale_code": self.scale_code,
            "cost_per_unit": self.cost_per_unit,
            "gross_profit": self.gross_profit,
            "unit_price": self.selling_price
        }

class Recipe_relation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="used_recipes")
    ingredient = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="used_in")
    amount = models.FloatField()

    def serialize(self):
        return [self.ingredient.id, self.amount]

class Product_relation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="used_products")
    ingredient = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="used_in")
    amount = models.FloatField()

    def serialize(self):
        return [self.ingredient.id, self.amount]

class Packaging_relation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="used_packaging")
    ingredient = models.ForeignKey(Packaging, on_delete=models.CASCADE, related_name="used_in")
    amount = models.FloatField()

    def serialize(self):
        return [self.ingredient.id, self.amount]