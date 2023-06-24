import pytesseract
import cv2
import re

import numpy as np
import matplotlib.pyplot as plt         # displaying output images

import pyautogui
pyautogui.FAILSAFE = True
import time


# import classes.IngredientList as IngredientList
from classes.IngredientList import IngredientList
# import classes.Ingredient as Ingredient
from classes.Ingredient import Ingredient

from chatgpt3 import get_ingredients_gpt

import undetected_chromedriver as uc
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from update_notion import add_grocery_item

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'


def clean_ingredient(ingr):

    return ingr
def screenshot_url(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920x1080")
    driver = uc.Chrome(options=options)

    driver.get(url)

    # set the driver width to a fourth of the screen height
    
    pyautogui.press('f11')
    time.sleep(7)

    # get the height of the page using a max function
    height = driver.execute_script("return document.body.scrollHeight")
    chunks = 2
    chunk_size = int(height / chunks)
    for i in range(chunks-1):
        # scroll to the bottom of the page
        pyautogui.screenshot('screenshots/my_screenshot_'+ str(i) +'.png')
        pyautogui.scroll(-chunk_size)
        # wait for the page to load
        time.sleep(0.2)

    # print all files names in the screenshots directory

    image_list = []
    for filename in os.listdir('screenshots'):
        if filename.endswith('.png'):
            img = cv2.imread(os.path.join('screenshots', filename))
            if img is not None:
                image_list.append(img)
    print(image_list)
    # stitch together images
    stitched_image = cv2.vconcat(image_list)
    
    if(os.path.exists('screenshots/stitched_image.png')):
        os.remove('screenshots/stitched_image.png')

    cv2.imwrite('screenshots/stitched_image.png', stitched_image)
    
    # stich together all images in the screenshots directory

    driver.execute_script("console.log('hello world');")
    time.sleep(10)
    driver.quit()




def populate_ingredient_list(url_list):
    debug = True
    IL = IngredientList()
    ingredientText = ''

    filter_list=["optional", "tsp", "tbsp", "cup", "oz", "lb", "g", "kg", "ml", "l", "pinch", "dash", "can", "jar", "bottle", "slice", "slices","sliced", "piece", "pieces", "stalk", "stalks", "head", "heads", "leaf", "leaves", "bunch", "bunches", "bag", "bags", "box", "boxes", "package", "packages", "container", "containers", "bowl", "bowls", "pint", "pints", "quart", "quarts", "gallon", "gallons", "stick", "sticks", "sprig", "sprigs", "sprinkle", "sprinkles", "handful", "handfuls", "pinch", "pinches", "dash", "dashes", "teaspoon", "teaspoons", "tablespoon", "tablespoons", "clove", "cloves", "head", "heads", "inch", "inches", "ounce", "ounces", "pound", "pounds", "gram", "grams", "kilogram", "kilograms", "milliliter", "milliliters", "liter", "liters", "milligram", "milligrams", "gallon", "gallons", "quart", "quarts", "pint", "pints", "cup", "cups", "tablespoon", "tablespoons", "teaspoon", "teaspoons", "pinch", "pinches", "dash", "dashes", "sprinkle", "sprinkles", "handful", "handfuls", "slice", "slices", "piece", "pieces", "stalk", "stalks", "head", "heads", "leaf", "leaves", "bunch", "bunches", "bag", "bags", "box", "boxes", "package", "packages", "container", "containers", "bowl", "bowls", "stick", "sticks", "sprig", "sprigs", "sprinkle", "sprinkles", "handful", "handfuls", "pinch", "pinches", "dash", "dashes", "teaspoon", "teaspoons", "tablespoon"]
    conjunctions = 'cause|after|agin|albeit|also|altho|although|an|and|and/or|as|assuming|because|before|being|both|but|conjunction|directly|either|ere|ergo|except|excepting|for|how|howbeit|however|if|immediately|instantly|lest|like|neither|nor|notwithstanding|now|once|only|or|ossia|plus|provided|providing|save|saving|seeing|since|sith|slash|so|supposing|syne|than|that|tho|though|til|till|unless|until|what|when|whenas|whence|whencesoever|whenever|whensoever|where|whereas|whereat|whereby|wherefrom|wherein|whereinto|whereof|wheresoever|wherethrough|whereto|whereupon|wherever|wherewith|wherewithal|whether|while|whiles|whilst|whither|why|without|yet'
    

    # add the ingredients to the list
    # ingredient_list_array = get_ingredients_gpt(url_list)
    ingredient_list_array = get_ingredients_gpt_txt(url_list)
    for ingredient in ingredient_list_array:
        print("Ingredient: ", ingredient)
        text = ingredient.split(",")
        for line in text:
            print("line: ", line)\
            # filter out everything that is not a character, a space, or a number
            line = re.sub(r'[^a-z0-9\s$]', '', line)
            # # remove all conjunctions from the line
            line = re.sub(r'\b(?:to|of|cause|after|agin|albeit|also|altho|although|an|and|and/or|as|assuming|because|before|being|both|but|conjunction|directly|either|ere|ergo|except|excepting|for|how|howbeit|however|if|immediately|instantly|lest|like|neither|nor|notwithstanding|now|once|only|or|ossia|plus|provided|providing|save|saving|seeing|since|sith|slash|so|supposing|syne|than|that|tho|though|til|till|unless|until|what|when|whenas|whence|whencesoever|whenever|whensoever|where|whereas|whereat|whereby|wherefrom|wherein|whereinto|whereof|wheresoever|wherethrough|whereto|whereupon|wherever|wherewith|wherewithal|whether|while|whiles|whilst|whither|why|without|yet)\b', '', line)
            amount = re.findall(r'\d+', line)
            # # // get unit from line
            unit = re.findall(r'\b(?:optional|tsp|tbsp|cup|oz|lb|g|kg|ml|l|pinch|dash|can|jar|bottle|slice|slices|sliced|piece|pieces|stalk|stalks|head|heads|leaf|leaves|bunch|bunches|bag|bags|box|boxes|package|packages|container|containers|bowl|bowls|pint|pints|quart|quarts|gallon|gallons|stick|sticks|sprig|sprigs|sprinkle|sprinkles|handful|handfuls|pinch|pinches|dash|dashes|teaspoon|teaspoons|tablespoon|tablespoons|clove|cloves|head|heads|inch|inches|ounce|ounces|pound|pounds|gram|grams|kilogram|kilograms|milliliter|milliliters|liter|liters|milligram|milligrams|gallon|gallons|quart|quarts|pint|pints|cup|cups|tablespoon|tablespoons|teaspoon|teaspoons|pinch|pinches|dash|dashes|sprinkle|sprinkles|handful|handfuls|slice|slices|piece|pieces|stalk|stalks|head|heads|leaf|leaves|bunch|bunches|bag|bags|box|boxes|package|packages|container|containers|bowl|bowls|stick|sticks|sprig|sprigs|sprinkle|sprinkles|handful|handfuls|pinch|pinches|dash|dashes|teaspoon|teaspoons|tablespoon)\b', line)
            # # // get name from line
            name = re.findall(r'[a-z]+', line)
            # # // remove amount and unit from name
            for a in amount:
                try: name.remove(a)
                except ValueError: pass
            for u in unit:
                try: name.remove(u)
                except ValueError: pass
            # # // rejoin name
            name = " ".join(name)
            # # // add to ingredient list
            IL.add_ingredient(Ingredient(name, amount, unit))
            print("ADDING INGREDIENT", name)
            print("AMOUNT", amount)
            print("UNIT", unit)
            # IL.add_ingredient(Ingredient(line))
            # IL.add_ingredient(ingredient)
        # for line in txt:
        #     if(len(line) > 0):
        #         # if the line is not empty, we add it to the temp string because it is part of the ingredient
        #         temp += " " + line
        #         print("this is a line we add:", temp)
        #         print("length of chars in line: ", len(line))
        #     else: 
        #         # # if the line is empty, we add the temp string to the list of ingredients and reset the temp string
        #         # temp = temp.lower()
        #         # # filter out everything that is not a character, a space, or a number
        #         # temp = re.sub(r'[^a-z0-9\s$]', '', temp)
        #         # # remove all conjunctions from the line
        #         # temp = re.sub(r'\b(?:to|of|cause|after|agin|albeit|also|altho|although|an|and|and/or|as|assuming|because|before|being|both|but|conjunction|directly|either|ere|ergo|except|excepting|for|how|howbeit|however|if|immediately|instantly|lest|like|neither|nor|notwithstanding|now|once|only|or|ossia|plus|provided|providing|save|saving|seeing|since|sith|slash|so|supposing|syne|than|that|tho|though|til|till|unless|until|what|when|whenas|whence|whencesoever|whenever|whensoever|where|whereas|whereat|whereby|wherefrom|wherein|whereinto|whereof|wheresoever|wherethrough|whereto|whereupon|wherever|wherewith|wherewithal|whether|while|whiles|whilst|whither|why|without|yet)\b', '', temp)
        #         # amount = re.findall(r'\d+', temp)
        #         # # // get unit from line
        #         # unit = re.findall(r'\b(?:optional|tsp|tbsp|cup|oz|lb|g|kg|ml|l|pinch|dash|can|jar|bottle|slice|slices|sliced|piece|pieces|stalk|stalks|head|heads|leaf|leaves|bunch|bunches|bag|bags|box|boxes|package|packages|container|containers|bowl|bowls|pint|pints|quart|quarts|gallon|gallons|stick|sticks|sprig|sprigs|sprinkle|sprinkles|handful|handfuls|pinch|pinches|dash|dashes|teaspoon|teaspoons|tablespoon|tablespoons|clove|cloves|head|heads|inch|inches|ounce|ounces|pound|pounds|gram|grams|kilogram|kilograms|milliliter|milliliters|liter|liters|milligram|milligrams|gallon|gallons|quart|quarts|pint|pints|cup|cups|tablespoon|tablespoons|teaspoon|teaspoons|pinch|pinches|dash|dashes|sprinkle|sprinkles|handful|handfuls|slice|slices|piece|pieces|stalk|stalks|head|heads|leaf|leaves|bunch|bunches|bag|bags|box|boxes|package|packages|container|containers|bowl|bowls|stick|sticks|sprig|sprigs|sprinkle|sprinkles|handful|handfuls|pinch|pinches|dash|dashes|teaspoon|teaspoons|tablespoon)\b', temp)
        #         # # // get name from line
        #         # name = re.findall(r'[a-z]+', temp)
        #         # # // remove amount and unit from name
        #         # for a in amount:
        #         #     try: name.remove(a)
        #         #     except ValueError: pass
        #         # for u in unit:
        #         #     try: name.remove(u)
        #         #     except ValueError: pass
        #         # # // rejoin name
        #         # name = " ".join(name)
        #         # # // add to ingredient list
        #         # IL.add_ingredient(Ingredient(name, amount, unit))
        #         # print("ADDING INGREDIENT", name)
        #         # print("AMOUNT", amount)
        #         # print("UNIT", unit)
        #         # print("NAME", "X" + name + "X")
        #         IL.add_ingredient(Ingredient(temp))
        #         temp = ""
        # IL.showList()
        result = ""
        ingredient_flag = True
        ingredient_found = False

        # IL = IngredientList()
        # Test = Ingredient("test")
        # IL.add_ingredient(Ingredient("italian seasoning"))
        # IL.add_ingredient(Ingredient("brazil nut"))
        # IL.add_ingredient(Ingredient("Lemon"))
        # IL.add_ingredient(Ingredient("Garlic"))
        # IL.add_ingredient(Ingredient("Turmeric")) 

    # TODO: debug code to correctly add ingredients to the list
        

        # for line in txt:
        #     start_word = line.split(" ")[0] 
        #     if start_word == "Ingredients":
        #         ingredient_found = True
        #         ingredient_flag = True
        #         line = line.split(" ")
        #         for word in line:
        #             print ("IN THE FOR LOOP\n", word)
        #             result += word + "$ "
        #         result = result[:-2]
        #         print(result)
        #         continue
        #     # elif line == "Directions":
        #     #     print("DIRECTIONS\n")
        #     #     ingredient_flag = False
        #     #     continue
        #     if line != '' or line != "":
        #         print("line is:" + line)
        #         # if(ingredient_flag and ingredient_found):
        #         #     # add_grocery_item(line)
                    
        #         #     line = line.lower()
        #         #     # filter out everything that is not a character, a space, or a number
        #         #     line = re.sub(r'[^a-z0-9\s$]', '', line)
        #         #     # remove all conjunctions from the line
        #         #     line = re.sub(r'\b(?:to|of|cause|after|agin|albeit|also|altho|although|an|and|and/or|as|assuming|because|before|being|both|but|conjunction|directly|either|ere|ergo|except|excepting|for|how|howbeit|however|if|immediately|instantly|lest|like|neither|nor|notwithstanding|now|once|only|or|ossia|plus|provided|providing|save|saving|seeing|since|sith|slash|so|supposing|syne|than|that|tho|though|til|till|unless|until|what|when|whenas|whence|whencesoever|whenever|whensoever|where|whereas|whereat|whereby|wherefrom|wherein|whereinto|whereof|wheresoever|wherethrough|whereto|whereupon|wherever|wherewith|wherewithal|whether|while|whiles|whilst|whither|why|without|yet)\b', '', line)
        #         #     # # remove all food adjectives from the line
        #         #     line = re.sub(r'\b(?:)\b', '', line)
                    
        #         #     amount = re.findall(r'\d+', line)
        #         #     # // get unit from line
        #         #     unit = re.findall(r'\b(?:optional|tsp|tbsp|cup|oz|lb|g|kg|ml|l|pinch|dash|can|jar|bottle|slice|slices|sliced|piece|pieces|stalk|stalks|head|heads|leaf|leaves|bunch|bunches|bag|bags|box|boxes|package|packages|container|containers|bowl|bowls|pint|pints|quart|quarts|gallon|gallons|stick|sticks|sprig|sprigs|sprinkle|sprinkles|handful|handfuls|pinch|pinches|dash|dashes|teaspoon|teaspoons|tablespoon|tablespoons|clove|cloves|head|heads|inch|inches|ounce|ounces|pound|pounds|gram|grams|kilogram|kilograms|milliliter|milliliters|liter|liters|milligram|milligrams|gallon|gallons|quart|quarts|pint|pints|cup|cups|tablespoon|tablespoons|teaspoon|teaspoons|pinch|pinches|dash|dashes|sprinkle|sprinkles|handful|handfuls|slice|slices|piece|pieces|stalk|stalks|head|heads|leaf|leaves|bunch|bunches|bag|bags|box|boxes|package|packages|container|containers|bowl|bowls|stick|sticks|sprig|sprigs|sprinkle|sprinkles|handful|handfuls|pinch|pinches|dash|dashes|teaspoon|teaspoons|tablespoon)\b', line)
        #         #     # // get name from line
        #         #     name = re.findall(r'[a-z]+', line)
        #         #     # // remove amount and unit from name
        #         #     for a in amount:
        #         #         try: name.remove(a)
        #         #         except ValueError: pass
        #         #     for u in unit:
        #         #         try: name.remove(u)
        #         #         except ValueError: pass
        #         #     # // rejoin name
        #         #     name = " ".join(name)
        #         #     # // add to ingredient list
        #         #     IL.add_ingredient(Ingredient(name))
        #         #     print("ADDING INGREDIENT", name)
        #         #     print("AMOUNT", amount)
        #         #     print("UNIT", unit)
        #         #     print("NAME", "X" + name + "X")

        # # IL.showList()
    return IL


