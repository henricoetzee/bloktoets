import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SparApps.settings')
django.setup()

from bloktoets.models import Products
from bloktoets.views import update_recipe_pricing_all

products = Products.objects.all()
print("Store\t\t\tRecipebook\t\tProduct\t\t\t\tNet Cost\tVolume\t\tCurrent cost\tNew cost")

count = 0
for product in products:

    correct_price = product.cost / product.volume
  
    if not (-0.3 < correct_price - product.unit_price < 0.3):
        count += 1
        """ volume_tabs = '\t'
        if product.cost < 1000.0:
            volume_tabs += '\t'
        price_tabs = '\t'
        if product.unit_price < 1000.0:
            price_tabs += '\t'
        recipebook = product.recipe_book.name + ' ' * (20-len(product.recipe_book.name)) if product.recipe_book is not None else "NONE" + " " * 15
        store = product.recipe_book.store.name if product.recipe_book is not None else product.store.name if product.store is not None else "NONE" + " " * 15
        if len(product.name) > 31:
            print(f'{store}\t{recipebook}\t{product.name[:14]}...{product.name[-14:]}\t{product.cost:,.2f}{volume_tabs}{product.volume:,.2f}\t\t{product.unit_price:,.2f}{price_tabs}{correct_price:,.2f}')
        else:
            space = ' ' * (31 - len(product.name))
            print(f'{store}\t{recipebook}\t{product.name}{space}\t{product.cost:,.2f}{volume_tabs}{product.volume:,.2f}\t\t{product.unit_price:,.2f}{price_tabs}{correct_price:,.2f}')
 """
        product.unit_price = correct_price
        product.save(update_fields=["unit_price"])

print(f"Updated {count} products. Calculating new recipe prices...")

changes = update_recipe_pricing_all()

print(f"Updated {len(changes)} recipe prices.")