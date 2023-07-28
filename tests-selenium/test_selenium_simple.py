import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get('https://google.com')

def test_search_example(selenium):
    """ Search some phrase in google and make a screenshot of the page. """

    # Open google search page:
    selenium.get('https://google.com')

    time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!

    # Find the field for search text input:
    search_input = driver.find_element(By.NAME, "q")

    # Enter the text for search:
    search_input.clear()
    search_input.send_keys('first test')
    search.send_keys(Keys.RETURN)

    time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!

    # Click Search:
    search_button = selenium.find_element(By.NAME,'btnK')
    search_button.click()


    time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!

    # Make the screenshot of browser window:
    selenium.save_screenshot('result.png')