from django import forms
from .models import Recipe, RecipeIngredient
from ingredients.models import Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "name",
            "course_type",
            "prep_time",
            "cook_time",
            "portions",
            "status",
            "image",
            "cost",
            "calories",
            "proteins",
            "fats",
            "carbohydrates",
            "sugar",
            "fiber",
            "sodium",
            "preparation_sheet",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "course_type": forms.Select(attrs={"class": "form-control"}),
            "prep_time": forms.TextInput(attrs={"class": "form-control"}),
            "cook_time": forms.TextInput(attrs={"class": "form-control"}),
            "portions": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "cost": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "calories": forms.NumberInput(attrs={"class": "form-control"}),
            "proteins": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "fats": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "carbohydrates": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "sugar": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "fiber": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "sodium": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "preparation_sheet": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
        }


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "quantity", "unit", "notes"]
        widgets = {
            "ingredient": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "unit": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show ingredients that are in stock
        self.fields["ingredient"].queryset = Ingredient.objects.filter(
            status="in_stock"
        )
        self.fields["ingredient"].empty_label = "Select an ingredient..."


class RecipeIngredientFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = RecipeIngredient.objects.none()

    def clean(self):
        super().clean()
        ingredients = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE"):
                ingredient = form.cleaned_data.get("ingredient")
                if ingredient in ingredients:
                    raise forms.ValidationError(
                        "Each ingredient can only be added once to a recipe."
                    )
                ingredients.append(ingredient)
