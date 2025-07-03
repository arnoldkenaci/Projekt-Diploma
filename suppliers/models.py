from django.db import models


class Supplier(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("pending", "Pending"),
    ]

    RATING_CHOICES = [
        (1, "1 - Poor"),
        (2, "2 - Fair"),
        (3, "3 - Good"),
        (4, "4 - Very Good"),
        (5, "5 - Excellent"),
    ]

    name = models.CharField(max_length=200, help_text="Supplier company name")
    contact_person = models.CharField(
        max_length=100, help_text="Primary contact person"
    )
    email = models.EmailField(help_text="Primary email address")
    phone = models.CharField(max_length=20, help_text="Primary phone number")
    address = models.TextField(help_text="Full address")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    postal_code = models.CharField(max_length=20, default="")
    country = models.CharField(max_length=100, default="")

    # Business Information
    tax_id = models.CharField(
        max_length=50, blank=True, null=True, help_text="Tax identification number"
    )
    website = models.URLField(blank=True, null=True, help_text="Company website")

    # Status and Rating
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        blank=True,
        null=True,
        help_text="Supplier performance rating",
    )

    # Financial Information
    payment_terms = models.CharField(
        max_length=100, blank=True, null=True, help_text="Payment terms (e.g., Net 30)"
    )
    credit_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Credit limit amount",
    )

    # Additional Information
    notes = models.TextField(
        blank=True, null=True, help_text="Additional notes about the supplier"
    )

    # Timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        """Returns the complete address as a string"""
        address_parts = [self.address]
        if self.city:
            address_parts.append(self.city)
        if self.state:
            address_parts.append(self.state)
        if self.postal_code:
            address_parts.append(self.postal_code)
        if self.country:
            address_parts.append(self.country)
        return ", ".join(address_parts)

    @property
    def is_active(self):
        """Returns True if supplier is active"""
        return self.status == "active"
