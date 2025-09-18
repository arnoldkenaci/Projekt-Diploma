# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from recipes.models import Recipe
from ingredients.models import Ingredient
from inventory.models import InventoryItem
from tasks.models import Task
from suppliers.models import Supplier


@login_required
def dashboard(request):
    # Summary counts
    recipe_count = Recipe.objects.count()
    ingredient_count = Ingredient.objects.count()
    inventory_count = InventoryItem.objects.count()
    task_count = Task.objects.count()
    supplier_count = Supplier.objects.count()
    user_count = User.objects.count()

    # Recent activity (last 5 of each)
    recent_recipes = Recipe.objects.order_by("-created_at")[:5]
    recent_ingredients = Ingredient.objects.order_by("-date_created")[:5]
    recent_tasks = Task.objects.order_by("-date_created")[:5]
    recent_suppliers = Supplier.objects.order_by("-date_created")[:5]

    # Stock alerts
    low_stock_ingredients = Ingredient.objects.filter(
        status="out_of_stock"
    ) | Ingredient.objects.filter(quantity__lte=5)
    low_stock_inventory = [
        item for item in InventoryItem.objects.all() if item.status != "in_stock"
    ]

    # Task overview
    open_tasks = Task.objects.filter(status="open").count()
    in_progress_tasks = Task.objects.filter(status="in_progress").count()
    completed_tasks = Task.objects.filter(status="completed").count()

    context = {
        "recipe_count": recipe_count,
        "ingredient_count": ingredient_count,
        "inventory_count": inventory_count,
        "task_count": task_count,
        "supplier_count": supplier_count,
        "user_count": user_count,
        "recent_recipes": recent_recipes,
        "recent_ingredients": recent_ingredients,
        "recent_tasks": recent_tasks,
        "recent_suppliers": recent_suppliers,
        "low_stock_ingredients": low_stock_ingredients,
        "low_stock_inventory": low_stock_inventory,
        "open_tasks": open_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": completed_tasks,
    }
    return render(request, "dashboard/dashboard.html", context)
