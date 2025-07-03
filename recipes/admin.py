from django.contrib import admin
from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ["ingredient", "quantity", "unit", "notes"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "course_type", "status", "portions", "cost", "created_at"]
    list_filter = ["course_type", "status", "created_at"]
    search_fields = ["name", "preparation_sheet"]
    readonly_fields = ["created_at"]
    inlines = [RecipeIngredientInline]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "course_type",
                    "prep_time",
                    "cook_time",
                    "portions",
                    "status",
                )
            },
        ),
        (
            "Nutritional Information",
            {
                "fields": (
                    "calories",
                    "proteins",
                    "fats",
                    "carbohydrates",
                    "sugar",
                    "fiber",
                    "sodium",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Media & Cost", {"fields": ("image", "cost")}),
        ("Preparation", {"fields": ("preparation_sheet",)}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["recipe", "ingredient", "quantity", "unit", "get_cost"]
    list_filter = ["recipe", "ingredient"]
    search_fields = ["recipe__name", "ingredient__name"]

    def get_cost(self, obj):
        return f"${obj.get_cost():.2f}"

    get_cost.short_description = "Cost"
