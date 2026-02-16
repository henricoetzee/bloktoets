from collections import deque

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from bloktoets.models import (
    RecipeBook,
    Products,
    Recipe,
    Product_relation,
    Recipe_relation,
)

class Command(BaseCommand):
    help = "Copy all products and recipes (filtered by sub_dept) from one RecipeBook to another, including recursive sub-recipes."

    def add_arguments(self, parser):
        parser.add_argument("--src", type=int, required=True, help="Source RecipeBook ID")
        parser.add_argument("--dst", type=int, required=True, help="Destination RecipeBook ID")
        parser.add_argument("--sub-dept", type=str, required=True, help="Recipe.sub_dept value to copy")
        parser.add_argument(
            "--iexact",
            action="store_true",
            help="Case-insensitive sub_dept match (sub_dept__iexact).",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="If set, skip creating Products/Recipes that already exist in destination (by name + codes).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        src_id = options["src"]
        dst_id = options["dst"]
        sub_dept = options["sub_dept"]
        iexact = options["iexact"]
        skip_existing = options["skip_existing"]

        try:
            src_book = RecipeBook.objects.get(id=src_id)
            dst_book = RecipeBook.objects.get(id=dst_id)
        except RecipeBook.DoesNotExist as e:
            raise CommandError(str(e))

        if src_book.id == dst_book.id:
            raise CommandError("Source and destination RecipeBook cannot be the same.")

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"Copying from '{src_book}' (id={src_book.id}) → '{dst_book}' (id={dst_book.id})"
        ))
        self.stdout.write(f"Recipe filter: sub_dept {'(iexact)' if iexact else '(exact)'} == '{sub_dept}'")

        # 1) Copy ALL products from src to dst, build mapping old_product_id -> new_product
        product_map = {}
        src_products = Products.objects.filter(recipe_book=src_book).order_by("id")

        created_products = 0
        skipped_products = 0

        for p in src_products:
            if skip_existing:
                existing = Products.objects.filter(
                    recipe_book=dst_book,
                    name=p.name,
                    product_code=p.product_code,
                    scale_code=p.scale_code,
                ).first()
                if existing:
                    product_map[p.id] = existing
                    skipped_products += 1
                    continue

            new_p = Products.objects.create(
                name=p.name,
                recipe_book=dst_book,
                store=None,  # store ignored
                product_code=p.product_code,
                scale_code=p.scale_code,
                packing_qty=p.packing_qty,
                cost=p.cost,
                unit_price=p.unit_price,
                stock_on_hand=p.stock_on_hand,
                sub_dept=p.sub_dept,
                volume=p.volume,
                unit_of_measure=p.unit_of_measure,
                supplier_product_code=p.supplier_product_code,
            )
            product_map[p.id] = new_p
            created_products += 1

        self.stdout.write(
            f"Products: created={created_products}, skipped(existing)={skipped_products}, total_mapped={len(product_map)}"
        )

        # 2) Root recipes by sub_dept (source book only)
        recipe_filter = {"recipe_book": src_book, "sub_dept__iexact" if iexact else "sub_dept": sub_dept}
        root_recipes = list(Recipe.objects.filter(**recipe_filter).order_by("id"))

        if not root_recipes:
            raise CommandError(
                f"No recipes found in source RecipeBook {src_book.id} with sub_dept='{sub_dept}'."
            )

        self.stdout.write(f"Root recipes selected: {len(root_recipes)}")

        # 3) Discover ALL dependent recipes via Recipe_relation recursively
        # We do a BFS over recipe->ingredient edges.
        all_recipe_ids = set(r.id for r in root_recipes)
        q = deque(all_recipe_ids)

        while q:
            current_id = q.popleft()
            # Find sub-recipes used by current
            sub_ids = (
                Recipe_relation.objects
                .filter(recipe_id=current_id)
                .values_list("ingredient_id", flat=True)
            )
            for sid in sub_ids:
                if sid not in all_recipe_ids:
                    all_recipe_ids.add(sid)
                    q.append(sid)

        all_recipes = list(
            Recipe.objects.filter(recipe_book=src_book, id__in=all_recipe_ids).order_by("id")
        )

        # Sanity: ensure none of the discovered IDs are from another book (shouldn't happen, but just in case)
        if len(all_recipes) != len(all_recipe_ids):
            found = {r.id for r in all_recipes}
            missing = sorted(all_recipe_ids - found)
            raise CommandError(
                "Some dependent recipe IDs were referenced but not found in the source book. "
                f"Missing IDs: {missing}"
            )

        self.stdout.write(f"Total recipes to copy (roots + sub-recipes): {len(all_recipes)}")

        # Map old_recipe_id -> new_recipe
        recipe_map = {}

        def get_or_copy_recipe(old_recipe: Recipe) -> Recipe:
            if old_recipe.id in recipe_map:
                return recipe_map[old_recipe.id]

            if old_recipe.recipe_book_id != src_book.id:
                raise CommandError(f"Recipe id={old_recipe.id} is not in the source RecipeBook; can't copy.")

            if skip_existing:
                existing = Recipe.objects.filter(
                    recipe_book=dst_book,
                    name=old_recipe.name,
                    product_code=old_recipe.product_code,
                    scale_code=old_recipe.scale_code,
                ).first()
                if existing:
                    recipe_map[old_recipe.id] = existing
                    return existing

            new_r = Recipe.objects.create(
                name=old_recipe.name,
                recipe_book=dst_book,
                scale_code=old_recipe.scale_code,
                product_code=old_recipe.product_code,
                cost_per_unit=old_recipe.cost_per_unit,
                gross_profit=old_recipe.gross_profit,
                selling_price=old_recipe.selling_price,
                recipe_yield=old_recipe.recipe_yield,
                stock_on_hand=old_recipe.stock_on_hand,
                sub_dept=old_recipe.sub_dept,
                unit_of_measure=old_recipe.unit_of_measure,
            )
            recipe_map[old_recipe.id] = new_r
            return new_r

        # 4) Copy all recipe base rows first (so relations can point to them)
        created_recipe_rows = 0
        skipped_recipe_rows = 0

        for old_r in all_recipes:
            before = len(recipe_map)
            new_r = get_or_copy_recipe(old_r)
            after = len(recipe_map)
            if after > before:
                created_recipe_rows += 1
            else:
                # might have been mapped to existing
                if skip_existing:
                    skipped_recipe_rows += 1

        self.stdout.write(f"Recipes: created={created_recipe_rows}, skipped(existing)={skipped_recipe_rows}, total_mapped={len(recipe_map)}")

        # 5) Copy Product_relation for EVERY copied recipe
        created_product_lines = 0
        for old_r in all_recipes:
            new_r = recipe_map[old_r.id]
            lines = Product_relation.objects.filter(recipe=old_r).select_related("ingredient")
            for line in lines:
                old_ing = line.ingredient
                if old_ing.id not in product_map:
                    raise CommandError(
                        f"Recipe id={old_r.id} uses Product id={old_ing.id}, but that product wasn't copied/mapped. "
                        f"Is that product in the source recipe book?"
                    )
                new_ing = product_map[old_ing.id]

                if skip_existing and Product_relation.objects.filter(
                    recipe=new_r, ingredient=new_ing, amount=line.amount
                ).exists():
                    continue

                Product_relation.objects.create(
                    recipe=new_r,
                    ingredient=new_ing,
                    amount=line.amount,
                )
                created_product_lines += 1

        self.stdout.write(f"Product_relation lines created: {created_product_lines}")

        # 6) Copy Recipe_relation for EVERY copied recipe (now that all recipes exist in dst)
        created_recipe_links = 0
        for old_r in all_recipes:
            new_r = recipe_map[old_r.id]
            links = Recipe_relation.objects.filter(recipe=old_r).select_related("ingredient")
            for link in links:
                old_sub = link.ingredient
                if old_sub.id not in recipe_map:
                    # Should not happen because we discovered dependencies, but keep it safe.
                    new_sub = get_or_copy_recipe(old_sub)
                else:
                    new_sub = recipe_map[old_sub.id]

                if skip_existing and Recipe_relation.objects.filter(
                    recipe=new_r, ingredient=new_sub, amount=link.amount
                ).exists():
                    continue

                Recipe_relation.objects.create(
                    recipe=new_r,
                    ingredient=new_sub,
                    amount=link.amount,
                )
                created_recipe_links += 1

        self.stdout.write(f"Recipe_relation links created: {created_recipe_links}")
        self.stdout.write(self.style.SUCCESS("Done."))
