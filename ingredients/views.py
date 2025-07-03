from django.shortcuts import render, redirect, get_object_or_404
from .models import Ingredient
from .forms import IngredientForm
import csv
from django.http import HttpResponse

# List all ingredients
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    
    # Search and filter logic
    search_query = request.GET.get('search', '')
    if search_query:
        ingredients = ingredients.filter(name__icontains=search_query)
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        ingredients = ingredients.filter(status=status_filter)

    return render(request, 'ingredients/ingredient_list.html', {
        'ingredients': ingredients
    })

# Add a new ingredient
def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm()
    return render(request, 'ingredients/add_ingredient.html', {'form': form})

# Edit an existing ingredient
def edit_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'ingredients/edit_ingredient.html', {'form': form, 'ingredient': ingredient})

# Delete an ingredient
def delete_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredient_list')
    return render(request, 'ingredients/confirm_delete.html', {'ingredient': ingredient})

# Export ingredients to CSV
def export_ingredients_csv(request):
    ingredients = Ingredient.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ingredients.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Quantity', 'Price', 'Unit', 'Status', 'Date Created'])
    for ingredient in ingredients:
        writer.writerow([ingredient.name, ingredient.quantity, ingredient.price, ingredient.unit, ingredient.get_status_display(), ingredient.date_created])
    return response
