from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import InventoryItem
import csv

@login_required
def inventory_list(request):
    # Get search and status filter from GET parameters
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    items = InventoryItem.objects.all()
    
    # Filter items based on search query
    if search:
        items = items.filter(name__icontains=search)
        
    # Filter items based on stock status
    if status_filter:
        items = items.filter(status=status_filter)
    
    return render(request, 'inventory/inventory_list.html', {
        'items': items,
        'search': search,
        'status': status_filter
    })

@login_required
def add_item(request):
    if request.method == 'POST':
        # Determine the next number for the new item
        last_item = InventoryItem.objects.order_by('-number').first()
        next_number = last_item.number + 1 if last_item else 1

        quantity = int(request.POST['quantity'])
        threshold = int(request.POST['threshold'])
        
        # Create a new inventory item
        InventoryItem.objects.create(
            number=next_number,
            name=request.POST['name'],
            quantity=quantity,
            unit=request.POST['unit'],
            cost=request.POST['cost'],
            threshold=threshold,
            description=request.POST.get('description', '')
        )
        return redirect('inventory_list')
    return render(request, 'inventory/add_inventory_item.html')

@login_required
def edit_item(request, id):
    item = get_object_or_404(InventoryItem, id=id)
    if request.method == 'POST':
        item.name = request.POST['name']
        item.quantity = int(request.POST['quantity'])
        item.unit = request.POST['unit']
        item.cost = request.POST['cost']
        item.threshold = int(request.POST['threshold'])
        item.description = request.POST.get('description', '')
        item.save()
        return redirect('inventory_list')
    return render(request, 'inventory/edit_inventory_item.html', {'item': item})

@login_required
def delete_item(request, id):
    item = get_object_or_404(InventoryItem, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')
    return render(request, 'inventory/delete_inventory_item.html', {'item': item})

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Number', 'Name', 'Quantity', 'Unit', 'Cost', 'Status'])
    
    # Write each inventory item as a row in the CSV file
    for item in InventoryItem.objects.all():
        writer.writerow([item.number, item.name, item.quantity, item.unit, item.cost, item.status])
    
    return response
