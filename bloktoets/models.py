from django.db import models

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    def __str__(self):
        return self.name

class RecipeBook(models.Model):
    name = models.CharField(max_length=64, blank=False)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    def __str__(self):
        return self.store.name + " - " + self.name

class Products(models.Model):
    name = models.CharField(max_length=64, blank=False)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    recipe_book = models.ForeignKey(RecipeBook, on_delete=models.PROTECT, null=True)
    product_code = models.CharField(max_length=64, blank=True)
    scale_code = models.CharField(max_length=32)
    packing_qty = models.FloatField()
    cost = models.FloatField()
    unit_price = models.FloatField()
    stock_on_hand = models.FloatField(default=00)
    sub_dept = models.CharField(max_length=32)

    def serialize(self):
        used_in_recipes = True if Product_relation.objects.filter(ingredient=self).count() else False
        return {
            "id": self.id,
            "name": self.name,
            "product_code": self.product_code,
            "scale_code": self.scale_code,
            "sub_dept": self.sub_dept,
            "packing_qty": self.packing_qty,
            "cost": self.cost,
            "unit_price": self.unit_price,
            "stock_on_hand": self.stock_on_hand,
            "used_in_recipes": used_in_recipes
        }
    
    def __str__(self):
        return self.recipe_book.store.name + " - " + self.recipe_book.name + " - " + self.name
    

class Packaging(models.Model):
    name = models.CharField(max_length=64, blank=False)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    recipe_book = models.ForeignKey(RecipeBook, on_delete=models.PROTECT, null=True)
    product_code = models.CharField(max_length=64, blank=True)
    scale_code = models.CharField(max_length=32)
    packing_qty = models.FloatField()
    cost = models.FloatField()
    unit_price = models.FloatField()
    stock_on_hand = models.FloatField(default=0)
    sub_dept = models.CharField(max_length=32)

    def serialize(self):
        used_in_recipes = True if Packaging_relation.objects.filter(ingredient=self).count() else False
        return {
            "id": self.id,
            "name": self.name,
            "product_code": self.product_code,
            "scale_code": self.scale_code,
            "sub_dept": self.sub_dept,
            "packing_qty": self.packing_qty,
            "cost": self.cost,
            "unit_price": self.unit_price,
            "stock_on_hand": self.stock_on_hand,
            "used_in_recipes": used_in_recipes
        }
    
    def __str__(self):
        return self.recipe_book.store.name + " - " + self.recipe_book.name + " - " + self.name

class Recipe(models.Model):
    name = models.CharField(max_length=64, blank=False)
    recipe_book = models.ForeignKey(RecipeBook, on_delete=models.PROTECT)
    scale_code = models.CharField(max_length=32)
    product_code = models.CharField(max_length=64, blank=True)
    cost_per_unit = models.FloatField()
    gross_profit = models.FloatField()
    selling_price = models.FloatField()
    recipe_yield = models.FloatField()
    stock_on_hand = models.FloatField(default=0)
    sub_dept = models.CharField(max_length=32)
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
            "sub_dept": self.sub_dept,
            "cost_per_unit": self.cost_per_unit,
            "gross_profit": self.gross_profit,
            "unit_price": self.selling_price,
            "stock_on_hand": self.stock_on_hand,
        }
    
    def __str__(self):
        return self.recipe_book.__str__() + self.name
    

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