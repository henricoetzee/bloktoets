import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SparApps.settings')
django.setup()

from bloktoets.models import Products

products = Products.objects.all()
print("Product\t\t\tNet Cost\tVolume\t\tCurrent cost\tNew cost")
for product in products:
    correct_price = product.cost / product.volume
    if not (-0.3 < correct_price - product.unit_price < 0.3):
        volume_tabs = '\t'
        if product.cost < 1000.0:
            volume_tabs += '\t'
        price_tabs = '\t'
        if product.unit_price < 1000.0:
            price_tabs += '\t'
        if len(product.name) > 20:
            print(f'{product.name[:8]}...{product.name[-8:]}\t{product.cost:,.2f}{volume_tabs}{product.volume:,.2f}\t\t{product.unit_price:,.2f}{price_tabs}{correct_price:,.2f}')
        else:
            space = ' ' * (20 - len(product.name))
            print(f'{product.name}{space}\t{product.cost:,.2f}{volume_tabs}{product.volume:,.2f}\t\t{product.unit_price:,.2f}{price_tabs}{correct_price:,.2f}')
    
    