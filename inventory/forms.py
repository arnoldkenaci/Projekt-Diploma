from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'unit', 'cost', 'threshold', 'description']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

    def clean_threshold(self):
        threshold = self.cleaned_data.get('threshold')
        if threshold < 0:
            raise forms.ValidationError("Threshold cannot be negative.")
        return threshold
