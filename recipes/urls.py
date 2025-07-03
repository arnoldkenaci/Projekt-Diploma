from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("add/", views.add_recipe, name="add_recipe"),
    path("edit/<int:pk>/", views.edit_recipe, name="edit_recipe"),
    path("detail/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("delete/<int:pk>/", views.delete_recipe, name="delete_recipe"),
    path("status/<int:pk>/<str:status>/", views.update_status, name="update_status"),
    path(
        "change-status/<int:pk>/<str:status>/",
        views.change_recipe_status,
        name="change_recipe_status",
    ),
    # Ingredient management URLs
    path(
        "manage-ingredients/<int:pk>/",
        views.manage_ingredients,
        name="manage_ingredients",
    ),
    path(
        "add-ingredient/<int:pk>/",
        views.add_ingredient_to_recipe,
        name="add_ingredient_to_recipe",
    ),
    path(
        "remove-ingredient/<int:recipe_pk>/<int:ingredient_pk>/",
        views.remove_ingredient_from_recipe,
        name="remove_ingredient_from_recipe",
    ),
]
