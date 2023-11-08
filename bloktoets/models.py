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
    scale_code = models.CharField(max_length=32)
    packing_qty = models.FloatField()
    cost = models.FloatField()
    unit_price = models.FloatField()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "scale_code": self.scale_code,
            "packing_qty": self.packing_qty,
            "cost": self.cost,
            "unit_price": self.unit_price
        }

class Packaging(models.Model):
    name = models.CharField(max_length=64, blank=False)
    scale_code = models.CharField(max_length=32)
    packing_qty = models.FloatField()
    cost = models.FloatField()
    unit_price = models.FloatField()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "scale_code": self.scale_code,
            "packing_qty": self.packing_qty,
            "cost": self.cost,
            "unit_price": self.unit_price
        }

class Recipe(models.Model):
    name = models.CharField(max_length=64, blank=False)
    recipe_book = models.ForeignKey(RecipeBook, on_delete=models.PROTECT)
    scale_code = models.CharField(max_length=32)
    cost_per_unit = models.FloatField()
    gross_profit = models.FloatField()
    selling_price = models.FloatField()
    ingredients = models.ManyToManyField(Products, related_name="used_in")
    packaging = models.ManyToManyField(Packaging, related_name="used_in")
    recipe_ingredients = models.ManyToManyField('self', symmetrical=False, related_name="used_in")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "scale_code": self.scale_code,
            "cost_per_unit": self.cost_per_unit,
            "gross_profit": self.gross_profit,
            "selling_price": self.selling_price,
        }



