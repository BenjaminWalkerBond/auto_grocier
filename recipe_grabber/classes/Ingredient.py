from .IngredientList import IngredientList

class Ingredient(IngredientList):
    def __init__(self, name, amount=1, unit="none"):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.tag = Ingredient.setTag(self, self.name)
        print(self.tag)
    def __str__(self):
        return f"{self.name} : {self.tag}"
    def setTag(self, ingredientName):
        # print("getTag Ingredient")
        return super().getTag(ingredientName)
    def get_name(self):
        return self.name
    def get_tag(self):
        return self.tag
