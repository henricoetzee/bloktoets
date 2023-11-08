from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from bloktoets.models import Store, RecipeBook, Products, Packaging, Recipe



def index(request):
    return render(request, "bloktoets/bloktoets.html")

@login_required
def api(request):
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
            return JsonResponse({"status": "failed", "error": e})
    # Get recipebooks
    if (request.GET['get'] == 'recipebook'):
        try:
            recipebooks = RecipeBook.objects.filter(store__pk=request.GET['store_id'])
            return JsonResponse({
                "status": "success",
                "headers": ["Recipebooks"],
                "data": [r.serialize() for r in recipebooks]
            })
        except Exception as e:
            return JsonResponse({"status": "failed", "error": e})
    # Get recipes
    if (request.GET['get'] == 'recipes'):
        try:
            recipes = Recipe.objects.filter(recipe_book__pk=request.GET['recipebook'])
            return JsonResponse({
                "status": "success",
                "headers": ["Recipe", "Scale code", "Cost per unit", "Gross profit", "Selling price"],
                "data": [r.serialize() for r in recipes]
            })
        except Exception as e:
            return JsonResponse({"status": "failed", "error": e})
    return JsonResponse({"status": "Unknown request"})