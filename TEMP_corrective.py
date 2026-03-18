import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SparApps.settings')
django.setup()

from bloktoets.models import Products, Store, RecipeBook

try:
    products = Products.objects.all()

    with open("product_changes.csv", "w") as file:
        file.write("Store,Department,Product,Old cost,New cost\n")
        updates = 0

        for product in products:
            old_unit_price = product.unit_price
            if product.volume != 0:
                product.unit_price = float(product.cost) / float(product.volume)
            else:
                product.unit_price = product.cost
            if product.unit_price != old_unit_price:
                updates += 1
                file.write(product.recipe_book.store.name + "," +
                        product.recipe_book.name + "," +
                        product.name + "," +
                        f"{old_unit_price:.2f}" + "," +
                        f"{product.unit_price:.2f}" + "\n"
                        )
                product.save()

    print(f"Updated {updates} products.")
except Exception as e:
    print("Exception: " + str(e))