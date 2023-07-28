import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


pytest.driver = webdriver.Chrome()
pytest.driver.get("https://petfriends.skillfactory.ru")
element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('PycharmProjects\sele\tests-selenium\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('petuh@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    text_h1 = pytest.driver.find_element(By.TAG_NAME, 'h1').text
    assert text_h1 == "PetFriends"
    # Нажимаем на кнопку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
    # Проверяем, что находимся на странице пользователя
    text_h2 = pytest.driver.find_element(By.TAG_NAME, 'h2').text
    assert text_h2 == "Petuh"

    yield pytest.driver

    pytest.driver.quit()

def test_show_my_pets(testing):
   pytest.driver = testing
   images = pytest.driver.find_elements(By.XPATH, '.card-deck .card-img-top')
   names = pytest.driver.find_elements(By.XPATH, '.card-deck .card-title')
   descriptions = pytest.driver.find_elements(By.XPATH, '.card-deck .card-text')

   for i in range(len(names)):
       assert images[i].get_attribute('src') != ''
       assert names[i].text != ''
       assert descriptions[i].text != ''
       assert ', ' in descriptions[i]
       parts = descriptions[i].text.split(", ")
       assert len(parts[0]) > 0
       assert len(parts[1]) > 0

images = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located(By.CSS_SELECTOR, ".card-deck .card-img-top"))
names = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located(By.CSS_SELECTOR, ".card-deck .card-title"))
descriptions = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located(By.CSS_SELECTOR, ".card-deck .card-text"))


def my_pets_clickable(by, desc):

    wait = WebDriverWait(pytest.driver, 10)
    by = by.upper()
    if by == 'XPATH':
        wait.until(EC.element_to_be_clickable((By.XPATH, desc))).click()
        if by == 'ID':
            wait.until(EC.element_to_be_clickable((By.ID, desc))).click()
            if by == 'LINK_TEXT':
                wait.until(EC.element_to_be_clickable((By.LINK_TEXT, desc))).click()
                my_pets_clickable('link_text', 'Moи питомцы')

       #Нажимаем на кнопку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()
        # Проверяем, что находимся на странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Petuh"
    

def test_pets_num(testing):
   pytest.driver = testing
   # Получаем количество питомцев пользователя
   pets_num = int(testing.find_element(By.XPATH, "//div[@class='.col-sm-4 left']").text.split("\n")[1].split(":")[1].strip())
   print(pets_num)
   # Получаем количество питомцев на странице
   pets_list = testing.find_elements(By.XPATH, "//tbody/tr")
   print(len(pets_list))
   assert int(pets_num) == len(pets_list), \
   f'Количество питомцев у пользователя - ({pets_num}) не равно количеству питомцев на странице - ({pets_list})'


def test_pets_names(testing):
   all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   all_pets_data = [pet.text for pet in all_pets]
   print(all_pets)
   uniq_pets = set(all_pets_data)
   if len(all_pets_data) == len(uniq_pets):
       print("Все питомцы имеют разные имена")

   else:
       print("В списке есть питомцы c повторяющимися данными:")
   assert len(all_pets_data) == len(uniq_pets)
   not_uniq_pets = set([pet.text for pet in all_pets if all_pets_data.count(pet.text) > 1])
   print(f'Повторяющиеся питомцы {not_uniq_pets}')


