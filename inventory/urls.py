from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.add_item, name='add_item'),
    path('<int:id>/edit/', views.edit_item, name='edit_item'),
    path('<int:id>/delete/', views.delete_item, name='delete_item'),
    path('export/', views.export_csv, name='export_csv'),
]