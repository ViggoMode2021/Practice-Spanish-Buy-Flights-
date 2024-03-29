import os
from dotenv import load_dotenv, find_dotenv
import pytest
from splinter import driver
from dotenv import load_dotenv, find_dotenv
import pytest
from time import sleep
#https://qxf2.com/blog/github-actions-to-execute-test-against-localhost-at-ci-stage/
# chromeOptions: args: ["--headless", "--disable-gpu", "--window-size=1920,1080", "--no-sandbox", "--allowed-ips=108.0.5359.71"]  binary: "/usr/bin/google-chrome-stable"
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')

#Fixture for Chrome
@pytest.fixture(scope="class")
def chrome_driver_init(request):
    chrome_driver = webdriver.Chrome(chrome_options=options)
    request.cls.driver = chrome_driver
    chrome_driver.get("https://practicespanishbuyflights.com/")
    load_dotenv(find_dotenv())
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-pytest")
    load_dotenv(dotenv_path)
    yield
    chrome_driver.close()

#Fixture for Chrome
@pytest.fixture(scope="class")
def site_login(request):
    chrome_driver = webdriver.Chrome(chrome_options=options)
    request.cls.driver = chrome_driver
    chrome_driver.get("https://practicespanishbuyflights.com/")
    load_dotenv(find_dotenv())
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-pytest")
    load_dotenv(dotenv_path)
    username = chrome_driver.find_element(By.NAME, ('username'))
    test_username = os.getenv("test_username")
    username.send_keys(test_username)
    sleep(2)
    test_password = os.getenv("test_password")
    chrome_driver.find_element(By.NAME, ("password")).send_keys(test_password)
    sleep(2)
    chrome_driver.find_element(By.ID, "submit_button").click()
    yield
    chrome_driver.close()

@pytest.mark.usefixtures("site_login")
class Test_Levels():
        def test_open_colombia_verbs(self):
            self.driver.find_element(By.ID, "colombia_verbs").click()
            find_colombia_title = self.driver.find_element(By.TAG_NAME, ('h5'))
            assert find_colombia_title.text == "Verbs - Colombia"
            self.driver.find_element(By.ID, "level_selector").click()
            sleep(3)

        def test_open_argentina_places(self):
            self.driver.find_element(By.ID, "argentina_places").click()
            find_argentina_title = self.driver.find_element(By.TAG_NAME, ('h5'))
            assert find_argentina_title.text == "Places - Argentina"
            self.driver.find_element(By.ID, "level_selector").click()
            sleep(3)

        def test_open_peru_speaking(self):
            self.driver.find_element(By.ID, "peru_speaking").click()
            find_peru_title = self.driver.find_element(By.TAG_NAME, ('h5'))
            assert find_peru_title.text == "Speaking Page - Perú"
            self.driver.find_element(By.ID, "level_selector").click()
            sleep(3)

        def test_open_paraguay_adjectives(self):
            self.driver.find_element(By.ID, "paraguay_adjectives").click()
            find_paraguay_title = self.driver.find_element(By.TAG_NAME, ('h5'))
            assert find_paraguay_title.text == "Adjectives - Paraguay"
            self.driver.find_element(By.ID, "level_selector").click()
            sleep(3)

        def test_open_mexico_foods_and_drinks(self):
            self.driver.find_element(By.ID, "mexico_foods_and_drinks").click()
            find_mexico_title = self.driver.find_element(By.TAG_NAME, ('h5'))
            assert find_mexico_title.text == "Foods + Drinks - México"
            self.driver.find_element(By.ID, "level_selector").click()
            sleep(3)
            
        def test_open_ecuador_verb_conjugation(self):
            self.driver.find_element(By.ID, "ecuador_verb_conjugation").click()
            find_ecuador_title = self.driver.find_element(By.TAG_NAME, ('h1'))
            assert find_ecuador_title.text == "Verb conjugation practice tense selector"
            self.driver.find_element(By.ID, "level_selector").click()
            sleep(3)
        
        def test_open_guatemala_greetings_and_farewells(self):
            self.driver.find_element(By.ID, "guatemala_greetings_and_farewells").click()
            find_guatemala_title = self.driver.find_element(By.TAG_NAME, ('h5'))
            assert find_guatemala_title.text == "Guatemala - Greetings and farewells"
            self.driver.find_element(By.ID, "level_selector").click()
            sleep(3)

# if no space:
#sudo docker system prune -a