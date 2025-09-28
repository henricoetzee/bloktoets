import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SparApps.settings')
django.setup()

from bloktoets.views import update_recipe_pricing_all

# Update prices
print("Updating pricing...")
changes = update_recipe_pricing_all()
print("Updated " + str(len(changes)) + " recipes.")

# Save changes to file:
try:
    with open("changes.csv", "w") as file:
        file.write("Store" + "," + 
                "Department" + "," + 
                "Recipe name" + "," + 
                "Old cost" + "," + 
                "New cost" + "," + 
                "% Change" + "," +
                "Selling" + "," + 
                "New GP" + "\n")
        for c in changes:
            file.write(c["store"] + "," + 
                    c["department"] + "," + 
                    "\"" + c["recipe_name"] + "\"" + "," + 
                    str(c["old_cost"]) + "," + 
                    str(c["new_cost"]) + "," + 
                    str((c["new_cost"] - c["old_cost"]) / c["new_cost"] * 100) + "," + 
                    str(c["selling"]) + "," + 
                    str(c["new_gp"]) + "\n")
    print("Changes saved to changes.csv")
except Exception as e:
    print("Could not save file. Error: " + e.__str__())