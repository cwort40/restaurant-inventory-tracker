from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        fields = ['name', 'quantity', 'unit', 'price_per_unit']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingredient Name',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantity',
                'min': '0.1',
                'step': '0.1',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per Unit ($)',
                'min': '0.1',
                'step': '0.1',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
        }


# Creating a ModelForm class for the Purchase model
class PurchaseForm(forms.ModelForm):
    # Defining a Meta class to specify which model and fields to use
    class Meta:
        model = Purchase
        # Set fields to all fields from the Purchase model
        fields = ['menu_item']
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
        fields = ['title', 'price']
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
                'min': '0.1',
                'step': '0.1',
                'style': 'margin: 0 auto; width: auto; text-align: center;'
            }),
        }


class RecipeRequirementForm(forms.ModelForm):
    UNIT_CHOICES = UNITS_OF_MEASUREMENT
    quantity = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Quantity',
        'min': '0.1',
        'step': '0.1',
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['menu_item'].queryset = MenuItem.objects.filter(user=user).order_by('title')
        self.fields['ingredient'].queryset = Ingredient.objects.filter(user=user).order_by('name')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise forms.ValidationError('Username must be at least 4 characters long')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')
        return password1
