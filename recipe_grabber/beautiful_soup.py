import requests
from bs4 import BeautifulSoup
from chatgpt3 import get_ingredients_gpt_txt
# URL of the webpage you want to extract text from
url = "https://www.recipetineats.com/spaghetti-bolognese/"


# create a curl request to url

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the text on the webpage
text = soup.get_text()

# Remove newlines and extra spaces in the text
text = " ".join(text.split())

# print the amount of words in the text
print(len(text)/4)
ingredients = get_ingredients_gpt_txt(text)
# print the ingredients from the list, each on a new line
for ingredient in ingredients:
    # format the print statement print a new line after each ingredient
    print(ingredient)
    print("\n")
# Print the extracted text
# output the text to a text file
with open("output.txt", "w") as text_file:
    text_file.write(text)

# print(text)
