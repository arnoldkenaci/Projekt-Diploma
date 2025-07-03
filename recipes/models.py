from django.db import models
from ingredients.models import Ingredient


class Recipe(models.Model):
    COURSE_CHOICES = [
        ("starter", "Starter"),
        ("main", "Main Course"),
        ("dessert", "Dessert"),
        ("drink", "Drink"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    name = models.CharField(max_length=200)
    course_type = models.CharField(max_length=20, choices=COURSE_CHOICES)
    prep_time = models.CharField(max_length=50)
    cook_time = models.CharField(max_length=50)
    portions = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Nutritional facts (per portion)
    calories = models.PositiveIntegerField(
        blank=True, null=True, help_text="Total calories (kcal)"
    )
    proteins = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Grams of protein",
    )
    fats = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, help_text="Grams of fat"
    )
    carbohydrates = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Grams of carbs",
    )
    sugar = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Grams of sugar",
    )
    fiber = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Grams of fiber",
    )
    sodium = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Milligrams of sodium",
    )

    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    preparation_sheet = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def calculate_total_cost(self):
        """Calculate total cost of recipe based on ingredients"""
        total_cost = 0
        for recipe_ingredient in self.recipeingredient_set.all():
            ingredient_cost = (
                recipe_ingredient.ingredient.price * recipe_ingredient.quantity
            )
            total_cost += ingredient_cost
        return total_cost

    def calculate_cost_per_portion(self):
        """Calculate cost per portion"""
        total_cost = self.calculate_total_cost()
        if self.portions > 0:
            return total_cost / self.portions
        return 0

    def get_ingredients_list(self):
        """Get list of ingredients with quantities"""
        return self.recipeingredient_set.select_related("ingredient").all()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Quantity needed for this recipe"
    )
    unit = models.CharField(max_length=50, help_text="Unit of measurement")
    notes = models.TextField(
        blank=True, null=True, help_text="Additional notes for this ingredient"
    )

    class Meta:
        unique_together = ["recipe", "ingredient"]
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe Ingredients"

    def __str__(self):
        return (
            f"{self.recipe.name} - {self.ingredient.name} "
            f"({self.quantity} {self.unit})"
        )

    def get_cost(self):
        """Calculate cost for this ingredient in the recipe"""
        return self.ingredient.price * self.quantity
