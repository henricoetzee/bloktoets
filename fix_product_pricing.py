import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SparApps.settings')
django.setup()

from bloktoets.models import Products

products = Products.objects.all()
print("Store\t\t\tRecipebook\t\tProduct\t\t\t\tNet Cost\tVolume\t\tCurrent cost\tNew cost")
count = 0
for product in products:
    count += 1
    correct_price = product.cost / product.volume
    if (-0.3 < correct_price - product.unit_price < 0.3):
        volume_tabs = '\t'
        if product.cost < 1000.0:
            volume_tabs += '\t'
        price_tabs = '\t'
        if product.unit_price < 1000.0:
            price_tabs += '\t'
        recipebook = product.recipe_book.name + ' ' * (20-len(product.recipe_book.name)) if product.recipe_book is not None else "NONE" + " " * 15
        store = product.recipe_book.store.name if product.recipe_book is not None else product.store.name if product.store is not None else "NONE" + " " * 15
        if len(product.name) > 23:
            print(f'{store}\t{recipebook}\t{product.name[:10]}...{product.name[-10:]}\t{product.cost:,.2f}{volume_tabs}{product.volume:,.2f}\t\t{product.unit_price:,.2f}{price_tabs}{correct_price:,.2f}')
        else:
            space = ' ' * (20 - len(product.name))
            print(f'{store}\t{recipebook}\t{product.name}{space}\t{product.cost:,.2f}{volume_tabs}{product.volume:,.2f}\t\t{product.unit_price:,.2f}{price_tabs}{correct_price:,.2f}')
    #if count > 100:
    #    break
    