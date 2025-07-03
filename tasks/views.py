from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User  # To access users for assigning tasks
from .models import Task
from .forms import TaskForm
import csv

# List all tasks with optional filtering
def task_list(request):
    tasks = Task.objects.all()

    # Filter by status if requested
    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks
    })

# Add a new task
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/add_task.html', {
        'form': form
    })

# Edit an existing task
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    users = User.objects.all()  # Get all users for the 'Assign To' field

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'task': task,
        'users': users
    })

# Delete a task
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/delete_task.html', {
        'task': task
    })

# Export tasks to CSV
def export_tasks_csv(request):
    tasks = Task.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Status', 'Priority', 'Assigned To', 'Date Created'])

    for task in tasks:
        writer.writerow([
            task.name,
            task.description,
            task.get_status_display(),
            task.get_priority_display(),
            task.assigned_to.username if task.assigned_to else 'Unassigned',
            task.date_created.strftime('%Y-%m-%d %H:%M'),
        ])

    return response
