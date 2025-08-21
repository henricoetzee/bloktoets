from django.contrib import admin
from bloktoets.models import Store, RecipeBook, Products, Packaging, Recipe

# Register your models here.

admin.site.register(Store)
admin.site.register(RecipeBook)
admin.site.register(Products)
admin.site.register(Packaging)
admin.site.register(Recipe)