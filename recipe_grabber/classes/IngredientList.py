import os

class IngredientList:
    
    tags_dict = {}
    tags= ["spice","fish","vegetable","fruit","cheese", "oil","meat","tree_nut","wine"]
    tags_constant = {"eggs","milk","none"}

    def init_dicts(self):
        # load all txt files in the word_dictionaries folder into tags_dict
        # get the parent directory of the current file
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
        x = 0
        for path in os.scandir("word_dictionaries/"):
            if path.is_file():
                with open(parent_dir + "\word_dictionaries\\" + self.tags[x] + ".txt") as f:
                    for line in f:
                        self.tags_dict[line.strip()] = self.tags[x]
            x += 1
       
        #  initialize each dictionary with their respective word files
        print("initialized tag dictionary")
        
        self.tags_dict["eggs"] = "eggs"
        self.tags_dict["milk"] = "milk"
    def __init__(self):
        self.init_dicts();
        self.ingredients = []
    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
    def remove_last_ingredient(self):
        return self.ingredients.pop()

    # need to alter algorithim to search for compound words like "green beans"
    def getTag(self,ingredientName):
        ingredientName = ingredientName.lower()
        tag=self.tags_dict.get(ingredientName)
        # check if self.tags.get(ingredientName) is not in the dictionary
        if tag is None:
            ingredientName = ingredientName.split(" ")
            # check each word in the ingredient name for a tag match
            for word in ingredientName:
                check = self.tags_dict.get(word)
                if(word == "salt"):
                    print("check is: ", check, "when word is salt")
                if check is not None:
                    tag = self.tags_dict.get(word)
                    break
        else:
            print()
        print("getTag IngredientList")
        print("ingredientName: ", ingredientName)
        return tag
    def get_ingredients(self):
        return self.ingredients
    def showList(self):
        print("INGREDIENT LIST: \n")
        for ingredient in self.ingredients:
            print(ingredient)

