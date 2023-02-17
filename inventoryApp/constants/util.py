from inventoryApp.constants.densities import INGREDIENT_DENSITIES
from inventoryApp.constants.measurements import UNIT_CONVERSIONS
import difflib


class UnitConversionUtil:
    @staticmethod
    def convert_to_common_unit(quantity, unit, ingredient_name):
        density = INGREDIENT_DENSITIES.get(ingredient_name)
        if density is None:
            # If the density is None, try to find the closest matching ingredient name
            best_match = difflib.get_close_matches(ingredient_name, INGREDIENT_DENSITIES.keys(), n=1)
            if best_match:
                density = INGREDIENT_DENSITIES[best_match[0]]
            else:
                density = 1  # Density of water as default
        for key in UNIT_CONVERSIONS:
            if key.find(unit) != -1:
                quantity *= UNIT_CONVERSIONS.get(key)
                break
        return quantity / density  # Convert to grams or milliliters

    @staticmethod
    def convert_to_original_unit(quantity, unit, ingredient_name):
        density = INGREDIENT_DENSITIES.get(ingredient_name)
        if density is None:
            # If the density is None, try to find the closest matching ingredient name
            best_match = difflib.get_close_matches(ingredient_name, INGREDIENT_DENSITIES.keys(), n=1)
            if best_match:
                density = INGREDIENT_DENSITIES[best_match[0]]
            else:
                density = 1  # Density of water as default
        for key in UNIT_CONVERSIONS:
            if key.find(unit) != -1:
                quantity /= UNIT_CONVERSIONS.get(key)
                break
        return quantity * density  # Convert to original unit
