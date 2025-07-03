from django.db import models


class InventoryItem(models.Model):
    UNIT_CHOICES = [
        ("kg", "Kilogram"),
        ("pcs", "Pieces"),
        ("box", "Box"),
        ("g", "Gram"),
        ("l", "Liter"),
        ("ml", "Milliliter"),
        # Add more unit options as needed
    ]

    number = models.PositiveIntegerField(unique=True, editable=False)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    threshold = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    @property
    def status(self):
        if self.quantity == 0:
            return "out_of_stock"
        elif self.quantity < self.threshold:
            return "low_stock"
        else:
            return "in_stock"

    def __str__(self):
        return self.name
