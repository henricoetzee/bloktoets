from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Products, Packaging, Recipe, Store
from .views import update_pricing
import json
import traceback

@csrf_exempt
def extenal_product_price_update(request):
    if request.method != "POST":
        JsonResponse({"error": "Requires POST"}, status=405)
    
    token = request.headers.get("Authorization")
    if token != f"Token {settings.SCRIPT_API_TOKEN}":
        return JsonResponse({"error": "Unauthorized"}, status=401)
    
    try:
        data = json.loads(request.body)
        store_id = data.get("store_id")
        updates = data.get("products")
        
        if not store_id or not isinstance(updates, list):
            return JsonResponse({"error": "Invalid data"}, status=400)
        
        try:
            store = Store.objects.get(id=store_id)
        except:
            return JsonResponse({"error": "Invalid store"}, status=404)
        
        updated = {}
        errors = []

        for entry in updates:
            code = entry.get("product_code")
            name = entry.get("name")
            price = entry.get("price")

            if not code or price is None:
                errors.append({"product_code": code, "error": "Missing data"})
                continue

            # Get the object(s) that needs to be updated. Hopefully only one.
            # Try to get products.
            try:
                products = Products.objects.filter(product_code=code, recipe_book__store=store.id)
                for product in products:
                    # Update price, if it is different
                    if product.cost != price:
                        updated[code] = {
                            "department": product.recipe_book.name,
                            "old_cost": product.cost,
                            "new_cost": price,"price_changes": [],                            
                            }
                        product.cost = price
                        product.unit_price = price / product.packing_qty
                        updated[code]["old_name"] = product.name        # So that we can see the name in the email. Name will not be shown if name is not updated.
                        product.save()
                        updated[code]["price_changes"].extend(update_pricing("product", product.id))

                    # Update name, if it is different
                    if product.name != name:
                        if not code in updated:
                            updated[code] = {}
                        updated[code]["old_name"] = product.name
                        updated[code]["new_name"] = name
                        product.name = name
                        product.save()
                    
            except Exception as e:
                errors.append({"product_code": code, "error in products": str(e)})

            # If there are no products, try to update packaging
            if len(products) == 0:
                try:
                    packs = Packaging.objects.filter(product_code=code, store=store)
                    for pack in packs:
                        # Update price, if it is different
                        if pack.cost != price:
                            updated[code] = {"old_cost": pack.cost, "new_cost": price, "price_changes": []}
                            pack.cost = price
                            pack.save()
                            updated[code]["price_changes"].extend(update_pricing("packaging", pack.id))
                        
                        # Update name if it is different
                        if pack.name != name:
                            if (type(updated[code]) != dict):
                                updated[code] = {}
                            updated[code]["old_name"] = pack.name
                            updated[code]["new_name"] = name
                            pack.name = name
                            pack.save()

                except Exception as e:
                    errors.append({"product_code": code, "error in packaging": str(e)})
        
        return JsonResponse({"updated": updated, "errors": errors})


    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)