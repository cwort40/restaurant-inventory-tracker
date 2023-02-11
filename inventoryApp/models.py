from django.db import models


# Create your models here.
class MenuItem(models.Model):
    # Item on the restaurant's menu
    title = models.CharField(max_length=200, unique=True)
    price = models.FloatField(default=0.00)

    def get_absolute_url(self):
        return "/menu"

    def available(self):
        return all(X.enough() for X in self.reciperequirement_set.all())

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    # Ingredient within the restaurant's inventory
    name = models.CharField(max_length=200, unique=True)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=200)
    price_per_unit = models.FloatField(default=0)

    def get_absolute_url(self):
        return "/ingredients"

    def __str__(self):
        return f"{self.name} per {self.unit}"


class RecipeRequirement(models.Model):
    # An ingredient and corresponding quantity needed for the recipe of a MenuItem.
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    def __str__(self):
        return f"{self.menu_item.__str__()}: {self.ingredient.name} qty of {self.quantity}"

    def get_absolute_url(self):
        return "/menu"

    def enough(self):
        return self.quantity <= self.ingredient.quantity


class Purchase(models.Model):
    # Purchase of a MenuItem
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item.__str__()} @ {self.timestamp}"

    def get_absolute_url(self):
        return "/purchases"
