from . import views
from django.urls import path

urlpatterns = [
    path('', views.ingredient_list, name='ingredient_list'),
    path('add/', views.add_ingredient, name='add_ingredient'),
    path('edit/<int:pk>/', views.edit_ingredient, name='edit_ingredient'),
    path('delete/<int:pk>/', views.delete_ingredient, name='delete_ingredient'),
    path('export/csv/', views.export_ingredients_csv, name='export_ingredients_csv'),
]
