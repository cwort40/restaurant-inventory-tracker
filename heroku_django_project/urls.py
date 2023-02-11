"""heroku_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path

from inventoryApp import views
from inventoryApp.views import IngredientListView, MenuListView, PurchaseListView, IngredientUpdateView, \
    IngredientCreateView, IngredientDeleteView, PurchaseAddView, PurchaseDeleteView, MenuItemCreateView, \
    MenuItemUpdateView, NewRecipeRequirementView, MenuItemDeleteView, RestaurantSummaryView

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path('admin/', admin.site.urls),
    path('', views.about, name='about'),
    path('insights/', RestaurantSummaryView.as_view(), name='insights'),
    path('ingredients/', IngredientListView.as_view(), name='ingredient-detail'),
    path('ingredients/<slug:pk>/update', IngredientUpdateView.as_view(), name="update-ingredient"),
    path('ingredients/add', IngredientCreateView.as_view(), name="add-ingredient"),
    path('ingredients/<slug:pk>/delete', IngredientDeleteView.as_view(), name="delete-ingredient"),
    path('menu/', MenuListView.as_view(), name='menu-detail'),
    path('menu/add', MenuItemCreateView.as_view(), name="add-menu-item"),
    path('menu/<slug:pk>/update', MenuItemUpdateView.as_view(), name="update-menu-item"),
    path('menu/add-recipe-requirement', NewRecipeRequirementView.as_view(), name="add-recipe-requirement"),
    path('menu/<slug:pk>/delete', MenuItemDeleteView.as_view(), name="delete-menu-item"),
    path('purchases/', PurchaseListView.as_view(), name='purchase-detail'),
    path('purchase/add', PurchaseAddView.as_view(), name="add-purchase"),
    path('purchase/<slug:pk>/delete', PurchaseDeleteView.as_view(), name="delete-purchase"),
]
