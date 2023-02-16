from django import forms

from inventoryApp.constants.measurements import UNITS_OF_MEASUREMENT
from inventoryApp.models import Ingredient, RecipeRequirement, Purchase, MenuItem


# Creating a ModelForm class for the Ingredient model
class IngredientForm(forms.ModelForm):
    UNIT_CHOICES = UNITS_OF_MEASUREMENT
    unit = forms.ChoiceField(choices=UNIT_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'style': 'margin: 0 auto; width: auto; text-align: center;'
    }))

    class Meta:
        model = Ingredient
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingredient Name',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantity',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per Unit ($)',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
        }


# Creating a ModelForm class for the Purchase model
class PurchaseForm(forms.ModelForm):
    # Defining a Meta class to specify which model and fields to use
    class Meta:
        model = Purchase
        # Set fields to all fields from the Purchase model
        fields = "__all__"
        # Set widgets for each of the fields
        widgets = {
            'menu_item': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Menu Item',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
        }


# Creating a ModelForm class for the MenuItem model
class MenuItemForm(forms.ModelForm):
    # Defining a Meta class to specify which model and fields to use
    class Meta:
        model = MenuItem
        # Set fields to all fields from the MenuItem model
        fields = "__all__"
        # Set widgets for each of the fields
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
        }


class RecipeRequirementForm(forms.ModelForm):
    UNIT_CHOICES = UNITS_OF_MEASUREMENT
    quantity = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Quantity',
        'style': 'margin: 0 auto; width: auto; text-align: center;'
    }))
    unit = forms.ChoiceField(choices=UNIT_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'style': 'margin: 0 auto; width: auto; text-align: center;'
    }))

    class Meta:
        model = RecipeRequirement
        fields = ['menu_item', 'ingredient', 'quantity', 'unit']
        widgets = {
            'menu_item': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Menu Item',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
            'ingredient': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Ingredient',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
        }

