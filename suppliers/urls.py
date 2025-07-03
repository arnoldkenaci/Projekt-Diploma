from django.urls import path
from . import views

urlpatterns = [
    path("", views.supplier_list, name="supplier_list"),
    path("add/", views.add_supplier, name="add_supplier"),
    path("edit/<int:pk>/", views.edit_supplier, name="edit_supplier"),
    path("detail/<int:pk>/", views.supplier_detail, name="supplier_detail"),
    path("delete/<int:pk>/", views.delete_supplier, name="delete_supplier"),
    path("export/", views.export_suppliers_csv, name="export_suppliers_csv"),
    path(
        "toggle-status/<int:pk>/",
        views.toggle_supplier_status,
        name="toggle_supplier_status",
    ),
]
