"""
URL configuration for green_endoscopy_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from product_emissions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('product_groups_materials/', views.product_groups_materials_view, name='product_groups_materials'),
    path('product_groups_emissions/', views.product_groups_emissions_view, name='product_groups_emissions'),
    path("reset_center_products/", views.reset_center_products, name="reset_center_products"),
    path("instrument_emissions/", views.instrument_emissions_view, name="instrument_emissions"),
]
