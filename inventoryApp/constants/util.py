from inventoryApp.constants.densities import INGREDIENT_DENSITIES
from inventoryApp.constants.measurements import UNIT_CONVERSIONS


class UnitConversionUtil:
    @staticmethod
    def convert_to_common_unit(quantity, unit, ingredient_name):
        density = INGREDIENT_DENSITIES.get(ingredient_name)
        for key in UNIT_CONVERSIONS:
            if key.find(unit) != -1:
                quantity *= UNIT_CONVERSIONS.get(key)
                break
        return quantity / density  # Convert to grams or milliliters

    @staticmethod
    def convert_to_original_unit(quantity, unit, ingredient_name):
        density = INGREDIENT_DENSITIES.get(ingredient_name)
        for key in UNIT_CONVERSIONS:
            if key.find(unit) != -1:
                quantity /= UNIT_CONVERSIONS.get(key)
                break
        return quantity * density  # Convert to original unit
