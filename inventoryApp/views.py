from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView

from inventoryApp.forms import IngredientForm, MenuItemForm, RecipeRequirementForm
from inventoryApp.models import Ingredient, MenuItem, Purchase, RecipeRequirement


# Define 2 functions to render HTML pages
def base(request):
    # Render the base.html page
    return render(request, 'inventoryApp/base.html')


def about(request):
    # Render the about.html page
    return render(request, 'inventoryApp/about.html')


# Define ListView to display a list of ingredients
class IngredientListView(LoginRequiredMixin, ListView):
    # Displays a list of ingredients
    template_name = 'inventoryApp/ingredients.html'
    model = Ingredient
    ordering = ['name']
    paginate_by = 15

    def get_queryset(self):
        # Filter the queryset based on a search term
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search', None)
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        return queryset


# Define UpdateView, CreateView, and DeleteView for ingredients
class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    # Update an ingredient
    template_name = 'inventoryApp/update-ingredient.html'
    model = Ingredient
    form_class = IngredientForm
    success_url = '/ingredients'


class IngredientCreateView(LoginRequiredMixin, CreateView):
    # Create an ingredient
    template_name = "inventoryApp/add-ingredient.html"
    model = Ingredient
    form_class = IngredientForm
    success_url = '/ingredients'


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    # Delete an ingredient
    template_name = "inventoryApp/delete-ingredient.html"
    model = Ingredient
    success_url = '/ingredients'


# Define ListView to display a list of purchases
class PurchaseListView(LoginRequiredMixin, ListView):
    # Displays a list of purchases
    template_name = 'inventoryApp/purchases.html'
    model = Purchase
    ordering = ['timestamp']
    paginate_by = 15

    def get_queryset(self):
        # Filter the queryset based on a search term
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search', None)
        if search_term:
            queryset = queryset.filter(menu_item__title__icontains=search_term)
        return queryset


# Define PurchaseAddView to add a purchase
class PurchaseAddView(LoginRequiredMixin, TemplateView):
    # Add a purchase
    template_name = "inventoryApp/add-purchase.html"

    # Checks if menu item is available
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [X for X in MenuItem.objects.all() if X.available()]
        return context

    # Removes the ingredients from the inventory that were used to make the menu item
    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity
            required_ingredient.save()

        purchase.save()
        return redirect("/purchases")


# Define purchase delete view
class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    # Delete a purchase
    template_name = "inventoryApp/delete-purchase.html"
    model = Purchase
    success_url = '/purchases'


# Define ListView to display a list of menu items
class MenuListView(LoginRequiredMixin, ListView):
    # Displays a list of menu items
    template_name = 'inventoryApp/menu.html'
    model = MenuItem
    ordering = ['title']
    paginate_by = 5

    def get_queryset(self):
        # Filter the queryset based on a search term
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search', None)
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)
        return queryset


# Define UpdateView, CreateView, and DeleteView for menu items
class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    # Update a menu item
    template_name = 'inventoryApp/update-menu-item.html'
    model = MenuItem
    form_class = MenuItemForm
    success_url = '/menu'


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    # Create a menu item
    template_name = "inventoryApp/add-menu-item.html"
    model = MenuItem
    form_class = MenuItemForm
    success_url = '/menu'


class NewRecipeRequirementView(LoginRequiredMixin, CreateView):
    # Create a recipe requirement
    template_name = "inventoryApp/add-recipe-requirement.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm


class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    # Delete a menu item
    template_name = "inventoryApp/delete-menu-item.html"
    model = MenuItem
    success_url = '/menu'


# Define RestaurantSummaryView to display restaurant metrics
class RestaurantSummaryView(View):
    # Displays a restaurant summary
    def get(self, request, *args, **kwargs):
        ingredients = Ingredient.objects.all()
        purchases = Purchase.objects.all()

        # Calculate the total cost of inventory, total revenue, and total profit
        total_cost_of_inventory, total_revenue, total_profit = 0, 0, 0
        if ingredients and purchases:
            total_cost_of_inventory = sum([ingredient.quantity * ingredient.price_per_unit for ingredient in ingredients])
            total_revenue = sum([purchase.menu_item.price for purchase in purchases])
            total_profit = total_revenue - total_cost_of_inventory

        context = {
            "total_cost_of_inventory": total_cost_of_inventory,
            "total_revenue": total_revenue,
            "total_profit": total_profit,
        }

        return render(request, "inventoryApp/insights.html", context)


# handles logout request and redirects user to login page
def log_out(request):
    logout(request)
    return redirect("/accounts/login")
