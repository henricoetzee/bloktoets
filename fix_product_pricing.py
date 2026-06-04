import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SparApps.settings')
django.setup()

from bloktoets.models import Products

products = Products.objects.all()

for product in products:
    correct_price = product.cost / product.volume
    if not (-0.3 < correct_price - product.unit_price < 0.3):
        print(product.name + ": " + product.unit_price + " → " + correct_price)

