import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SparApps.settings')
django.setup()

from django.db import transaction
from bloktoets.models import Store, RecipeBook, Recipe, Products, Packaging, Product_relation, Packaging_relation, Recipe_relation
import traceback

from django.db import transaction

def duplicate_store(store_id, new_store_id):
    try:
        original_store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return None  # Handle the case where the store does not exist

    with transaction.atomic():  # Ensures atomicity (all or nothing)
        # Step 1: Duplicate Store
        new_store = Store.objects.get(id=new_store_id)

        print(f"Old store: {original_store.name}")
        print(f"New store: {new_store.name}")

        # Step 2: Duplicate RecipeBooks
        original_recipe_books = RecipeBook.objects.filter(store=original_store)
        old_to_new_recipe_books = {}

        for rb in original_recipe_books:
            new_rb = RecipeBook.objects.create(name=rb.name, store=new_store)
            print(f"Created recipebook: {new_rb.name}")
            old_to_new_recipe_books[rb.id] = new_rb  # Map old IDs to new objects



        # Step 3: Duplicate Products
        original_products = Products.objects.filter(recipe_book__store=original_store)
        print(f"Found {original_products.count()} products to duplicate.")
        old_to_new_products = {}

        for product in original_products:
            #print(f"Duplicating product: {product.name} (ID: {product.id})")
            new_product = Products.objects.create(
                name=product.name,
                store=new_store,
                recipe_book=old_to_new_recipe_books.get(product.recipe_book.id, None),
                product_code=product.product_code,
                scale_code=product.scale_code,
                packing_qty=product.packing_qty,
                cost=product.cost,
                unit_price=product.unit_price,
                stock_on_hand=product.stock_on_hand,
                sub_dept=product.sub_dept,
            )
            #print(f"Created product: {new_product.name} in {new_product.recipe_book.name}")
            old_to_new_products[product.id] = new_product

        # Step 4: Duplicate Packaging
        original_packaging = Packaging.objects.filter(recipe_book__store=original_store)
        old_to_new_packaging = {}

        for pack in original_packaging:
            new_pack = Packaging.objects.create(
                name=pack.name,
                store=new_store,
                recipe_book=old_to_new_recipe_books.get(pack.recipe_book.id, None),
                product_code=pack.product_code,
                scale_code=pack.scale_code,
                packing_qty=pack.packing_qty,
                cost=pack.cost,
                unit_price=pack.unit_price,
                stock_on_hand=pack.stock_on_hand,
                sub_dept=pack.sub_dept,
            )
            #print(f"Created packaging: {new_pack.name} in {new_pack.recipe_book.name}")
            old_to_new_packaging[pack.id] = new_pack

        # Step 5: Duplicate Recipes
        original_recipes = Recipe.objects.filter(recipe_book__store=original_store)
        old_to_new_recipes = {}

        for recipe in original_recipes:
            new_recipe = Recipe.objects.create(
                name=recipe.name,
                recipe_book=old_to_new_recipe_books[recipe.recipe_book.id],
                scale_code=recipe.scale_code,
                product_code=recipe.product_code,
                cost_per_unit=recipe.cost_per_unit,
                gross_profit=recipe.gross_profit,
                selling_price=recipe.selling_price,
                recipe_yield=recipe.recipe_yield,
                stock_on_hand=recipe.stock_on_hand,
                sub_dept=recipe.sub_dept,
            )
            #print(f"Created Recipe: {new_recipe.name} in {new_recipe.recipe_book.name}")
            old_to_new_recipes[recipe.id] = new_recipe

        # Step 6: Duplicate Relationships (Ingredients, Packaging, and Nested Recipes)
        for recipe in original_recipes:
            new_recipe = old_to_new_recipes[recipe.id]

            # Product Relationships
            for relation in Product_relation.objects.filter(recipe=recipe):
                
                Product_relation.objects.create(
                    recipe=new_recipe,
                    ingredient=old_to_new_products.get(relation.ingredient.id),
                    amount=relation.amount,
                )

            # Packaging Relationships
            for relation in Packaging_relation.objects.filter(recipe=recipe):
                Packaging_relation.objects.create(
                    recipe=new_recipe,
                    ingredient=old_to_new_packaging.get(relation.ingredient.id),
                    amount=relation.amount,
                )

            # Recipe Relationships
            for relation in Recipe_relation.objects.filter(recipe=recipe):
                Recipe_relation.objects.create(
                    recipe=new_recipe,
                    ingredient=old_to_new_recipes.get(relation.ingredient.id),
                    amount=relation.amount,
                )

    return new_store