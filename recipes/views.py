from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormSet


# View for listing all recipes
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})


def change_recipe_status(request, pk, status):
    recipe = get_object_or_404(Recipe, pk=pk)
    if status in ["pending", "in_progress", "completed"]:
        recipe.status = status
        recipe.save()
    return redirect("recipe_list")


# View for adding a new recipe
def add_recipe(request):
    form = RecipeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        recipe = form.save()
        messages.success(request, f'Recipe "{recipe.name}" created successfully!')
        return redirect("recipe_detail", pk=recipe.pk)
    return render(request, "recipes/add_recipe.html", {"form": form})


# View for editing an existing recipe
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        messages.success(request, f'Recipe "{recipe.name}" updated successfully!')
        return redirect("recipe_detail", pk=recipe.pk)
    return render(request, "recipes/edit_recipe.html", {"form": form, "recipe": recipe})


# View for showing the details of a recipe
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = recipe.get_ingredients_list()
    total_cost = recipe.calculate_total_cost()
    cost_per_portion = recipe.calculate_cost_per_portion()

    context = {
        "recipe": recipe,
        "ingredients": ingredients,
        "total_cost": total_cost,
        "cost_per_portion": cost_per_portion,
    }
    return render(request, "recipes/recipe_detail.html", context)


# View for deleting a recipe
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe_name = recipe.name
    recipe.delete()
    messages.success(request, f'Recipe "{recipe_name}" deleted successfully!')
    return redirect("recipe_list")


# View for updating the status of a recipe (Quick Actions)
def update_status(request, pk, status):
    recipe = get_object_or_404(Recipe, pk=pk)
    if status in ["pending", "in_progress", "completed"]:
        recipe.status = status
        recipe.save()
        messages.success(request, f"Recipe status updated to {status.title()}")
    return redirect("recipe_list")


# View for managing recipe ingredients
def manage_ingredients(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        formset = RecipeIngredientFormSet(
            request.POST,
            instance=recipe,
            queryset=RecipeIngredient.objects.filter(recipe=recipe),
        )
        if formset.is_valid():
            formset.save()
            messages.success(request, "Recipe ingredients updated successfully!")
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        formset = RecipeIngredientFormSet(
            instance=recipe, queryset=RecipeIngredient.objects.filter(recipe=recipe)
        )

    context = {
        "recipe": recipe,
        "formset": formset,
    }
    return render(request, "recipes/manage_ingredients.html", context)


# View for adding a single ingredient to a recipe
def add_ingredient_to_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        form = RecipeIngredientForm(request.POST)
        if form.is_valid():
            recipe_ingredient = form.save(commit=False)
            recipe_ingredient.recipe = recipe
            recipe_ingredient.save()
            messages.success(request, "Ingredient added to recipe successfully!")
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeIngredientForm()

    context = {
        "recipe": recipe,
        "form": form,
    }
    return render(request, "recipes/add_ingredient.html", context)


# View for removing an ingredient from a recipe
def remove_ingredient_from_recipe(request, recipe_pk, ingredient_pk):
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    recipe_ingredient = get_object_or_404(
        RecipeIngredient, pk=ingredient_pk, recipe=recipe
    )
    ingredient_name = recipe_ingredient.ingredient.name
    recipe_ingredient.delete()
    messages.success(request, f'Ingredient "{ingredient_name}" removed from recipe!')
    return redirect("recipe_detail", pk=recipe.pk)
