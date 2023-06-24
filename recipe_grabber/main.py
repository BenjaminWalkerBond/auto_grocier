import selenium
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException    

from classes.IngredientList import IngredientList
from classes.Ingredient import Ingredient

import time
import random
from recipe_grabber import populate_ingredient_list

    
def check_exists_by_xpath(xpath,driver):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True
def random_time():
    time.sleep(random.randint(2, 3))
def add_ingredient(ingredient, driver):
    search_bar = driver.find_element(By.XPATH,"/html/body/div/header/div[1]/div[2]/div[1]/form/div/input")
    search_bar.clear()
    random_time()
    if ingredient.get_tag() == "vegetable" or ingredient.get_tag() == "fruit":
        search_bar.send_keys("organic ", ingredient.get_name())
    else:
        search_bar.send_keys(ingredient.get_name())
    random_time()
    search_bar.send_keys(Keys.ENTER)
    random_time()
    if(check_exists_by_xpath("/html/body/div[1]/main/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/button", driver)):
        add_to_cart_button = driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/button")
        add_to_cart_button.click()
    else:
        return 0
def clear_cart(driver):
    cart_button = driver.find_element(By.XPATH, "/html/body/div/header/div[1]/div[2]/a[2]")
    cart_button.click()
    random_time()
    if (check_exists_by_xpath("/html/body/div[1]/main/div/div/div[1]/div/section[2]/div[2]/button", driver)):
        clear_cart_button = driver.find_element(By.XPATH,"/html/body/div[1]/main/div/div/div[1]/div/section[2]/div[2]/button")
        random_time()
        # scroll down half the page to make sure the button is visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        clear_cart_button.click()
        random_time()
        confirm_empty = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[2]/button[2]")
        confirm_empty.click()
        random_time()
        home = driver.find_element(By.XPATH, "//html/body/div/header/div[1]/div[2]/a[1]")
        home.click()
        random_time()
    else:
        return 0
def reserve_time_slot(driver):
    
    # try:
        # navigate to the cart
        cart_button = driver.find_element(By.XPATH, "/html/body/div/header/div[1]/div[2]/a[2]")
        cart_button.click()
        random_time()
        # click the reserve time slot button
        reserve_button = driver.find_element(By.XPATH, "/html/body/div/main/div/div/div[1]/div/section[1]/div/div/button")
        reserve_button.click()
        random_time()
        tomorrow = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div/div/div/div/div[2]/div[2]/button[2]")
        # find the evening slots sections by searching for all elements with the same class and an h3 tag with the text "Evening"
        evening_slots_header = driver.find_element(By.XPATH, "//div[@class='sc-cyxg30-0 bQqawu']/div/h3[text()='Evening']")
        # get the parent of the evening_slots element
        evening_slots_container = (evening_slots_header.find_element(By.XPATH, "..")).find_element(By.XPATH, "..")

        evening_slots_container = evening_slots_container.find_elements(By.TAG_NAME, "button")

        open_day =''
        open_time = ''
        for time in evening_slots_container:
            # check if day.accesible_name contains open
            if "free" in time.get_attribute("aria-label"):
                open_day = time
                break
            print(time.accessible_name) 



        confirm_reserve = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[2]/button[2]")
        confirm_reserve.click()
        random_time()
    # except:
    #     print("Element not found")
    #     time.sleep(20)       
def login(driver):
    login_button = driver.find_element(By.XPATH, "/html/body/div/header/div[2]/div/ul/li[1]/a[1]")
    time.sleep(4)
    login_button.click()
    random_time()
    file = open("D:\python_projects\\auto_grocier\\recipe_grabber\HEB_config.txt", "r")
    login_info = file.read().split("\n")
    email = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/fieldset/div[1]/input")
    email.send_keys(login_info[0])
    random_time()
    password = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/fieldset/div[2]/div/input")
    password.send_keys(login_info[1])
    random_time()
    login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/fieldset/div[3]/button")
    login_button.click()
    random_time()
if __name__ == '__main__':

    url_list = ["https://www.cookingclassy.com/skillet-seared-salmon-with-garlic-lemon-butter-sauce/"]
    # initialize the ingredient list
    IL = populate_ingredient_list(url_list)
    IL.showList()
    testList = IngredientList()
    # testApple = Ingredient("apple")
    # testList.add_ingredient(testApple)
    # testNoMatch = Ingredient("no match")
    # testList.add_ingredient(testNoMatch)


    # # initialize the driver
    # driver = uc.Chrome()
    # # driver.get('https://nowsecure.nl')
    # driver.get("https://heb.com")
    # random_time()
    # driver.maximize_window()

    # random_time()

    # # perform HEB site operations
    # login(driver)
    # time.sleep(10)
    # random_time()
    # driver.maximize_window()
    # clear_cart(driver)
    # random_time()

    # reserve a time slot
    # reserve_time_slot(driver)

    
    # # add all ingredients to the cart
    # for ing in IL.get_ingredients():
    #     add_ingredient(IL.remove_last_ingredient(), driver)
    #     random_time()

    # time.sleep(50)