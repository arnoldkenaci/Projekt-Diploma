from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Supplier
from .forms import SupplierForm
import csv


@login_required
def supplier_list(request):
    """List all suppliers with search and filtering"""
    suppliers = Supplier.objects.all()

    # Search functionality
    search_query = request.GET.get("search", "")
    if search_query:
        suppliers = (
            suppliers.filter(name__icontains=search_query)
            | suppliers.filter(contact_person__icontains=search_query)
            | suppliers.filter(email__icontains=search_query)
        )

    # Status filter
    status_filter = request.GET.get("status", "")
    if status_filter:
        suppliers = suppliers.filter(status=status_filter)

    # Rating filter
    rating_filter = request.GET.get("rating", "")
    if rating_filter:
        suppliers = suppliers.filter(rating=rating_filter)

    context = {
        "suppliers": suppliers,
        "search_query": search_query,
        "status_filter": status_filter,
        "rating_filter": rating_filter,
    }

    return render(request, "suppliers/supplier_list.html", context)


@login_required
def add_supplier(request):
    """Add a new supplier"""
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier "{supplier.name}" added successfully!')
            return redirect("supplier_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SupplierForm()

    context = {"form": form, "title": "Add New Supplier", "button_text": "Add Supplier"}

    return render(request, "suppliers/supplier_form.html", context)


@login_required
def edit_supplier(request, pk):
    """Edit an existing supplier"""
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(
                request, f'Supplier "{supplier.name}" updated successfully!'
            )
            return redirect("supplier_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SupplierForm(instance=supplier)

    context = {
        "form": form,
        "supplier": supplier,
        "title": f"Edit Supplier: {supplier.name}",
        "button_text": "Update Supplier",
    }

    return render(request, "suppliers/supplier_form.html", context)


@login_required
def supplier_detail(request, pk):
    """Show detailed information about a supplier"""
    supplier = get_object_or_404(Supplier, pk=pk)

    context = {"supplier": supplier}

    return render(request, "suppliers/supplier_detail.html", context)


@login_required
def delete_supplier(request, pk):
    """Delete a supplier"""
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == "POST":
        supplier_name = supplier.name
        supplier.delete()
        messages.success(request, f'Supplier "{supplier_name}" deleted successfully!')
        return redirect("supplier_list")

    context = {"supplier": supplier}

    return render(request, "suppliers/supplier_confirm_delete.html", context)


@login_required
def export_suppliers_csv(request):
    """Export suppliers to CSV file"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="suppliers.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Name",
            "Contact Person",
            "Email",
            "Phone",
            "Address",
            "City",
            "State",
            "Postal Code",
            "Country",
            "Status",
            "Rating",
            "Payment Terms",
            "Credit Limit",
            "Date Created",
        ]
    )

    suppliers = Supplier.objects.all()
    for supplier in suppliers:
        writer.writerow(
            [
                supplier.name,
                supplier.contact_person,
                supplier.email,
                supplier.phone,
                supplier.address,
                supplier.city,
                supplier.state,
                supplier.postal_code,
                supplier.country,
                supplier.get_status_display(),
                supplier.get_rating_display() if supplier.rating else "Not Rated",
                supplier.payment_terms or "",
                supplier.credit_limit or "",
                supplier.date_created.strftime("%Y-%m-%d %H:%M"),
            ]
        )

    return response


@login_required
def toggle_supplier_status(request, pk):
    """Toggle supplier status between active and inactive"""
    supplier = get_object_or_404(Supplier, pk=pk)

    if supplier.status == "active":
        supplier.status = "inactive"
        message = f'Supplier "{supplier.name}" deactivated.'
    else:
        supplier.status = "active"
        message = f'Supplier "{supplier.name}" activated.'

    supplier.save()
    messages.success(request, message)

    return redirect("supplier_list")
