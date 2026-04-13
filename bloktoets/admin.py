from django.contrib import admin
from bloktoets.models import Store, RecipeBook, Products, Packaging, Recipe

# Register your models here.

admin.site.register(Store)
admin.site.register(Products)
admin.site.register(Packaging)
admin.site.register(Recipe)

@admin.register(RecipeBook)
class RecipeBookAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_store', 'packaging_percent')
    list_editable = ('packaging_percent',)

    @admin.display(description="Store")
    def get_store(self, obj):
        return obj.store.name
    