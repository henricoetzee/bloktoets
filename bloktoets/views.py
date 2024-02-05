import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from bloktoets.models import Store, RecipeBook, Products, Packaging, Recipe, Recipe_relation, Product_relation, Packaging_relation
import time


def index(request):
    return render(request, "bloktoets/bloktoets.html")

@login_required
def api(request):
    #-------------------GET REQUESTS-------------------
    if (request.method == 'GET'):
        # Get stores
        if (request.GET['get'] == 'stores'):
            try:
                stores = Store.objects.all()
                return JsonResponse({
                    "status": "success",
                    "headers": ["Stores"],
                    "data": [s.serialize() for s in stores]
                    })
            except Exception as e:
                print(e)
                return JsonResponse({"status": "failed", "error": "Server error while getting stores"})
        # Get recipebooks
        if (request.GET['get'] == 'recipebook'):
            try:
                recipebooks = RecipeBook.objects.filter(store__pk=request.GET['id'])
                return JsonResponse({
                    "status": "success",
                    "headers": ["Recipebooks"],
                    "data": [r.serialize() for r in recipebooks]
                })
            except Exception as e:
                print(e)
                return JsonResponse({"status": "failed", "error": "Server error while getting recipebooks"})
        # Get recipes
        if (request.GET['get'] == 'recipes'):
            try:
                recipes = Recipe.objects.filter(recipe_book__pk=request.GET['recipebook'])
                return JsonResponse({
                    "status": "success",
                    "headers": ["Recipe", "Scale code", "Sub dept","Cost per unit", "Gross profit", "Selling price"],
                    "data": [r.serialize() for r in recipes]
                })
            except Exception as e:
                print(e)
                return JsonResponse({"status": "failed", "error": "Server error while getting recipes"})
        # Get products
        if (request.GET['get'] == 'products'):
            try:
                products = Products.objects.filter(Q(recipe_book__pk=request.GET['recipebook']) | Q(store__pk=request.GET['id']))
                return JsonResponse({
                    "status": "success",
                    "headers": ["Product", "Scale code", "Sub dept", "Packing qty", "Cost", "Unit cost"],
                    "data": [p.serialize() for p in products]
                })
            except Exception as e:
                print(e)
                return JsonResponse({"status": "failed", "error": "Server error while getting products"})
        # Get packaging
        if (request.GET['get'] == 'packaging'):
            try:
                packaging = Packaging.objects.filter(Q(recipe_book__pk=request.GET['recipebook']) | Q(store__pk=request.GET['id']))
                return JsonResponse({
                    "status": "success",
                    "headers": ["Packaging", "Scale code", "Sub dept", "Packing qty", "Cost", "Unit cost"],
                    "data": [p.serialize() for p in packaging]
                })
            except Exception as e:
                print(e)
                return JsonResponse({"status": "failed", "error": "Server error while getting packaging"})
        
        # Get single product
        if (request.GET['get'] == 'product'):
            try:
                product = Products.objects.get(id=request.GET['id'])
                used_in = Product_relation.objects.filter(ingredient=product)
                return JsonResponse({
                    "status": "success",
                    "item": product.serialize(),
                    "store_visible": True if product.store is not None else False,
                    "used_in": [r.recipe.name for r in used_in]
                })
            except Exception as e:
                print(e)
                return JsonResponse({"status": "failed", "error": "Server error while getting product"})
        # Get single packaging
        if (request.GET['get'] == 'package'):
            try:
                package = Packaging.objects.get(id=request.GET['id'])
                used_in = Packaging_relation.objects.filter(ingredient=package)
                return JsonResponse({
                    "status": "success",
                    "item": package.serialize(),
                    "store_visible": True if package.store is not None else False,
                    "used_in": [r.recipe.name for r in used_in]
                })
            except Exception as e:
                print(e)
                return JsonResponse({"status": "failed", "error": "Server error while getting package"})
        # Get single recipe
        if (request.GET['get'] == 'recipe'):
            try:
                recipe = Recipe.objects.get(id=request.GET['id'])
                recipe_ingredients = Recipe_relation.objects.filter(recipe=recipe)
                product_ingredients = Product_relation.objects.filter(recipe=recipe)
                packaging_ingredients = Packaging_relation.objects.filter(recipe=recipe)
                used_in = Recipe_relation.objects.filter(ingredient=recipe)
                return JsonResponse({
                    "status": "success",
                    "id": recipe.id,
                    "name": recipe.name,
                    "scale_code": recipe.scale_code,
                    "sub_dept": recipe.sub_dept,
                    "recipe_ingredients": [i.serialize() for i in recipe_ingredients],
                    "product_ingredients": [i.serialize() for i in product_ingredients],
                    "packaging_ingredients": [i.serialize() for i in packaging_ingredients],
                    "cost_per_unit": recipe.cost_per_unit,
                    "unit_price": recipe.cost_per_unit,  # Extra name for cost, blame bad planning
                    "gross_profit": recipe.gross_profit,
                    "selling_price": recipe.selling_price,
                    "recipe_yield": recipe.recipe_yield,
                    "used_in": [r.recipe.name for r in used_in],
                    "stock_on_hand": recipe.stock_on_hand
                })
            except Exception as e:
                print(e)
                JsonResponse({"status": "failed", "error": "Server error while getting recipe"})
        return JsonResponse({"status": "failed", "error": "Unknown request"})

    
    #------------------------PUT REQUESTS------------------------
    if (request.method == 'PUT'):
        data = json.loads(request.body)

        #-------------------PRODUCTS-------------------#
        if (data['what'] == 'product'):

            if (data['todo'] == 'create'):  #-----------CREATE PRODUCT
                try:
                    newP = Products(
                        name = data["name"],
                        scale_code = data["scale_code"],
                        sub_dept = data["sub_dept"],
                        packing_qty = float(data["packing_qty"]),
                        cost = float(data["cost"]),
                        stock_on_hand = float(data["stock_on_hand"])
                    )
                    if (newP.packing_qty != 0):
                        newP.unit_price = newP.cost / newP.packing_qty
                    if (data["store_visible"]):
                        newP.store = Store.objects.get(id=data["store"])
                    else:
                        newP.recipe_book = RecipeBook.objects.get(id=data["recipe_book"])
                    newP.save()
                    return JsonResponse({"status": "success", "message": "Product created"})
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "error": "Failed to create product."})
            
            if (data['todo'] == 'modify'):  #-----------CHANGE PRODUCT
                try:
                    p = Products.objects.get(id=data["id"])
                    p.name = data["name"]
                    p.scale_code = data["scale_code"]
                    p.sub_dept = data["sub_dept"]
                    p.packing_qty = float(data["packing_qty"])
                    p.cost = float(data["cost"])
                    p.stock_on_hand = float(data["stock_on_hand"])
                    if (p.packing_qty != 0):
                        p.unit_price = float(p.cost) / float(p.packing_qty)
                    p.save()

                    # Update recipe pricing:
                    update_pricing("product", p.id)

                    return JsonResponse({"status": "success", "message": "Product updated"})
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "error": "Failed to update product"})
            
            if (data['todo'] == 'delete'): #-------------DELETE PRODUCT
                try:
                    p = Products.objects.get(id=data["id"])
                    p.delete()
                    # Recalculate recipe costing
                    update_recipe_pricing_all()
                    return JsonResponse({"status": "success"})
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "error": "Failed to delete product"})

                
        # -------------PACKAGING---------------#
        if (data['what'] == 'packaging'):  

            if (data['todo'] == 'create'): #-----CREATE PACKAGING
                try:
                    newP = Packaging(
                        name = data["name"],
                        scale_code = data["scale_code"],
                        packing_qty = float(data["packing_qty"]),
                        sub_dept = data["sub_dept"],
                        cost = float(data["cost"]),
                        stock_on_hand = float(data["stock_on_hand"])
                    )
                    if (newP.packing_qty != 0):
                        newP.unit_price = newP.cost / newP.packing_qty
                    if (data["store_visible"]):
                        newP.store = Store.objects.get(id=data["store"])
                    else:
                        newP.recipe_book = RecipeBook.objects.get(id=data["recipe_book"])
                    newP.save()
                    return JsonResponse({"status": "success"})
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "error": "Failed to create packaging"})

            if (data['todo'] == 'modify'): #-----------CHANGE PACKAGING
                try:
                    p = Packaging.objects.get(id=data["id"])
                    p.name = data["name"]
                    p.scale_code = data["scale_code"]
                    p.sub_dept = data["sub_dept"]
                    p.packing_qty = float(data["packing_qty"])
                    p.cost = float(data["cost"])
                    p.stock_on_hand = float(data["stock_on_hand"])
                    if (p.packing_qty != 0):
                        p.unit_price = float(p.cost) / float(p.packing_qty)
                    p.save()

                    # Update recipe pricing:
                    update_pricing("packaging", p.id)

                    return JsonResponse({"status": "success", "message": "Packing updated"})
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "error": "Failed to update product"})
        
            if (data['todo'] == 'delete'): #-------------DELETE PACKAGING
                try:
                    p = Packaging.objects.get(id=data["id"])
                    p.delete()
                    # Recalculate recipe costing
                    update_recipe_pricing_all()
                    return JsonResponse({"status": "success"})
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "error": "Failed to delete packaging"})
                
        # -----------------RECIPE-----------------------#
        if (data['what'] == "recipe"):

            if (data['todo'] == "create"): #------------CREATE RECIPE
                try:
                    recipe_book = RecipeBook.objects.get(id=data["recipe_book"])
                    recipe = Recipe(
                        name = data["name"],
                        recipe_book = recipe_book,
                        scale_code = data["scale_code"],
                        sub_dept = data["sub_dept"],
                        cost_per_unit = data["cost_per_unit"],
                        selling_price = data["selling_price"],
                        recipe_yield = data["recipe_yield"],
                        stock_on_hand = data["stock_on_hand"]
                    )
                    if recipe.selling_price != 0:
                        recipe.gross_profit = ((recipe.selling_price / 1.15) - recipe.cost_per_unit) / (recipe.selling_price / 1.15) * 100
                    else:
                        recipe.gross_profit = 0
                    recipe.save()

                    for item in data["recipe_ingredients"]:
                        relation = Recipe_relation(
                            recipe = recipe,
                            ingredient = Recipe.objects.get(id=item[0]),
                            amount = item[1]
                        )
                        relation.save()
                        
                    for item in data["ingredients"]:
                        relation = Product_relation(
                            recipe = recipe,
                            ingredient = Products.objects.get(id=item[0]),
                            amount = item[1]
                        )
                        relation.save()

                    for item in data["packaging"]:
                        relation = Packaging_relation(
                            recipe = recipe,
                            ingredient = Packaging.objects.get(id=item[0]),
                            amount = item[1]
                        )
                        relation.save()
                    
                    return JsonResponse({"status": "success", "message": "Recipe successfully created"})

                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "error": "Failed to create recipe"})
            
            if (data["todo"] == "modify"): #-------------CHANGE RECIPE
                try:
                    recipe = Recipe.objects.get(id=data["id"])
                    recipe.name = data["name"]
                    recipe.scale_code = data["scale_code"]
                    recipe.sub_dept = data["sub_dept"]
                    recipe.cost_per_unit = data["cost_per_unit"]
                    recipe.selling_price = data["selling_price"]
                    recipe.recipe_yield = data["recipe_yield"]
                    recipe.stock_on_hand = data["stock_on_hand"]
                    if recipe.selling_price != 0:
                        recipe.gross_profit = ((recipe.selling_price / 1.15) - recipe.cost_per_unit) / (recipe.selling_price / 1.15) * 100
                    else:
                        recipe.gross_profit = 0
                    recipe.save()

                    # Remove all relations
                    recipe_ingredients = Recipe_relation.objects.filter(recipe=recipe)
                    recipe_ingredients.delete()
                    product_ingredients = Product_relation.objects.filter(recipe=recipe)
                    product_ingredients.delete()
                    packaging_ingredients = Packaging_relation.objects.filter(recipe=recipe)
                    packaging_ingredients.delete()

                    # Recreate relations
                    for item in data["recipe_ingredients"]:
                        relation = Recipe_relation(
                            recipe = recipe,
                            ingredient = Recipe.objects.get(id=item[0]),
                            amount = item[1]
                        )
                        relation.save()
                        
                    for item in data["ingredients"]:
                        relation = Product_relation(
                            recipe = recipe,
                            ingredient = Products.objects.get(id=item[0]),
                            amount = item[1]
                        )
                        relation.save()

                    for item in data["packaging"]:
                        relation = Packaging_relation(
                            recipe = recipe,
                            ingredient = Packaging.objects.get(id=item[0]),
                            amount = item[1]
                        )
                        relation.save()

                    # Check for loops
                    if find_loop_all():
                        return JsonResponse({"status": "failed", "error": "Recipe saved, but there is a loop in the recipe ingredients, recipe pricing cannot be updated. Please fix!"})

                    # Update recipe pricing:
                    update_pricing("recipe", recipe.id)

                    return JsonResponse({"status": "success", "message": "Recipe changed"})

                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "error": "Could not change recipe"})
            
            if (data['todo'] == 'delete'): #-------------DELETE RECIPE
                try:
                    r = Recipe.objects.get(id=data["id"])
                    r.delete()
                    # Recalculate recipe costing
                    update_recipe_pricing_all()
                    return JsonResponse({"status": "success"})
                except Exception as e:
                    print(e)
                    return JsonResponse({"status": "failed", "error": "Failed to delete recipe"})

        if (data["what"] == "pricing"):
            try:
                update_recipe_pricing_all()
                return JsonResponse({"status": "success"})
            except Exception as e:
                return JsonResponse({"status": "failed"})
        return JsonResponse({"status": "failed", "error": "Unknown request"})
    return JsonResponse({"status": "failed", "error": "Unknown request"})

# Old update pricing function
# def update_recipe_pricing():
#     recipes = Recipe.objects.all()
#     for i in range(0,10):    # Run 10 times so that changes in recipes can be reflected in other recipes that was already changed.
#         for recipe in recipes:
#             recipe.cost_per_unit = 0
#             for used_recipes in Recipe_relation.objects.filter(recipe = recipe):
#                 recipe.cost_per_unit += used_recipes.ingredient.cost_per_unit * used_recipes.amount
#             for used_products in Product_relation.objects.filter(recipe = recipe):
#                 recipe.cost_per_unit += used_products.ingredient.cost / used_products.ingredient.packing_qty * used_products.amount
#             for used_packaging in Packaging_relation.objects.filter(recipe = recipe):
#                 recipe.cost_per_unit += used_packaging.ingredient.cost / used_packaging.ingredient.packing_qty * used_packaging.amount
#             recipe.cost_per_unit /= recipe.recipe_yield
#             if recipe.selling_price != 0:
#                 recipe.gross_profit = ((recipe.selling_price / 1.15) - recipe.cost_per_unit) / (recipe.selling_price / 1.15) * 100
#             else:
#                 recipe.gross_profit = 0
#             recipe.save()

def update_pricing(what_changed, id):
    relations = False
    if what_changed == "product":
        relations = Product_relation.objects.filter(ingredient__id=id)
    if what_changed == "packaging":
        relations = Packaging_relation.objects.filter(ingredient__id=id)
    if what_changed == "recipe":
        relations = Recipe_relation.objects.filter(ingredient__id=id)
    if relations != False:
        for r in relations:
            update_recipe_pricing(r.recipe.id)

def update_recipe_pricing_all():
    recipes = Recipe.objects.all()
    if recipes.count() > 0:
        for r in recipes:
            update_pricing("recipe", r.id)

def update_recipe_pricing(id = False, depth=0):

    if depth > 50:
        return
    recipe = Recipe.objects.get(id=id)
    recipe.cost_per_unit = 0
    for used_recipes in Recipe_relation.objects.filter(recipe = recipe):
        recipe.cost_per_unit += used_recipes.ingredient.cost_per_unit * used_recipes.amount
    for used_products in Product_relation.objects.filter(recipe = recipe):
        recipe.cost_per_unit += used_products.ingredient.cost / used_products.ingredient.packing_qty * used_products.amount
    recipe.cost_per_unit /= recipe.recipe_yield
    for used_packaging in Packaging_relation.objects.filter(recipe = recipe):
        recipe.cost_per_unit += used_packaging.ingredient.cost / used_packaging.ingredient.packing_qty * used_packaging.amount
    if recipe.selling_price != 0:
        recipe.gross_profit = ((recipe.selling_price / 1.15) - recipe.cost_per_unit) / (recipe.selling_price / 1.15) * 100
    else:
        recipe.gross_profit = 0
    recipe.save()

    new_recipes = Recipe_relation.objects.filter(ingredient=recipe)
    if new_recipes.count() > 0:
        for r in new_recipes:
            update_recipe_pricing(r.recipe.id, depth + 1)
    return
    
def find_loop(id, console_out=False, depth=0, next_id=False):
    # End if traversal goes to deep. (possible loop prevention)
    if depth > 50:
        return False
    # next_id will be false on the first iteration
    if not next_id:
        next_id = id
    relations = Recipe_relation.objects.filter(recipe__id=next_id)
    for r in relations:
        if console_out:
            print(str(next_id) + " -> " + str(r.ingredient.id))
        if r.ingredient.id == id:
            return True
        if find_loop(id, console_out, depth + 1, r.ingredient.id):
            return True
    return False

def find_loop_all(console_out=False):
    recipes = Recipe.objects.all()
    for r in recipes:
        if console_out:
            print(str(r.id) + ": " + r.name)
        if (find_loop(r.id, console_out)):
            return True
    return False