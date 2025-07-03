"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),  # This will include the dashboard URL patterns
    path("recipes/", include("recipes.urls")),  # Recipes app
    path("ingredients/", include("ingredients.urls")),  # Include the ingredients URLs
    path("tasks/", include("tasks.urls")),  # Include the ingredients URLs
    path("inventory/", include("inventory.urls")),  # Include the inventory URLs
    path("suppliers/", include("suppliers.urls")),  # Include the suppliers URLs
    path("accounts/", include("accounts.urls")),  # Include the accounts URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
