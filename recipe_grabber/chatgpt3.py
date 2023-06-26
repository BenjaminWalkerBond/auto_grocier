import os
import openai

file = open("config.txt", "r")

openai_config = file.read().split("\n")
openai.organization = openai_config[2]
openai.api_key = openai_config[3]
# filter the json object by the json attribute "id" and print it
# list = openai.Model.list()
# list.data.sort(key=lambda x: x.id)
# for model in list.data:
#     print(model.id)


def get_ingredients_gpt(url_list):

    ingredient_list = []

    for url in url_list:

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Please grab the ingredients from this url and return them in a comma seperated list: " + url + " \n"}
            ]
        )
        print("chat gpt response: " + completion.choices[0].message.content)
        verified = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Please verify that the following text seperates each distinct ingredient by a comma: " + completion.choices[0].message.content + " \n. If it does not, please insert commas where appropriate and return the list of comma separated ingredients. Do not include any other text."}
            ],
            # frequency_penalty=2.0,
        )  

        ingredient_list.append(verified.choices[0].message.content)
    return ingredient_list

def get_ingredients_gpt_txt(txt):

    ingredient_list = []

    # get the amount of character in the text
    char_count = len(txt)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "user", "content": "Please grab the ingredients and their measurements from the following text and return them in a comma seperated list in this format: INGREDIENT: AMOUNT UNIT. Make sure to only grab the ingredients from the ingredient section, and do not count ingredients twice. The ingredient section will look like this: Ingredients1 pound wild caught large shrimp with shells4 tablespoons extra virgin olive oil , divided4 cloves garlic , pressed or minced1 teaspoon kosher salt½ teaspoon red pepper flakes4 tablespoons butter⅓ cup white wine or chicken stock2 tablespoons fresh lemon juice , or ½ lemon1 tablespoon minced parsley" + txt + " \n"}
        ]
    )

    verified = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Please verify that the following text seperates each distinct ingredient by a comma: " + completion.choices[0].message.content + " \n. If it does not, please insert commas where appropriate and return ONLY the list of comma separated ingredients. DO NOT include any other text."}
        ],
        # frequency_penalty=2.0,
    )  

    ingredient_list.append(verified.choices[0].message.content)
    return ingredient_list
