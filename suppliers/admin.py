from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "contact_person",
        "email",
        "phone",
        "status",
        "rating",
        "date_created",
    ]
    list_filter = ["status", "rating", "date_created"]
    search_fields = ["name", "contact_person", "email", "phone"]
    readonly_fields = ["date_created", "date_updated"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "contact_person", "email", "phone")}),
        (
            "Address Information",
            {"fields": ("address", "city", "state", "postal_code", "country")},
        ),
        ("Business Information", {"fields": ("tax_id", "website", "status", "rating")}),
        ("Financial Information", {"fields": ("payment_terms", "credit_limit")}),
        ("Additional Information", {"fields": ("notes",)}),
        (
            "Timestamps",
            {"fields": ("date_created", "date_updated"), "classes": ("collapse",)},
        ),
    )

    ordering = ["name"]
    list_per_page = 25
