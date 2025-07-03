from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "name",
            "contact_person",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
            "tax_id",
            "website",
            "status",
            "rating",
            "payment_terms",
            "credit_limit",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter supplier company name",
                }
            ),
            "contact_person": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter primary contact person",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter email address"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter phone number"}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter full address",
                }
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter city"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter state/province"}
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter postal code"}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter country"}
            ),
            "tax_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter tax identification number",
                }
            ),
            "website": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "Enter website URL"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "rating": forms.Select(attrs={"class": "form-control"}),
            "payment_terms": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Net 30, Cash on Delivery",
                }
            ),
            "credit_limit": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Enter credit limit amount",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter additional notes about the supplier",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            # Check if email already exists for another supplier
            supplier_id = self.instance.id if self.instance else None
            if Supplier.objects.filter(email=email).exclude(id=supplier_id).exists():
                raise forms.ValidationError(
                    "A supplier with this email address already exists."
                )
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            # Basic phone number validation
            import re

            phone_pattern = re.compile(r"^[\+]?[1-9][\d]{0,15}$")
            if not phone_pattern.match(
                phone.replace(" ", "")
                .replace("-", "")
                .replace("(", "")
                .replace(")", "")
            ):
                raise forms.ValidationError("Please enter a valid phone number.")
        return phone
