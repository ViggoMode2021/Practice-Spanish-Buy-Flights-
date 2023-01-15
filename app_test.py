import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv, find_dotenv
import boto3
import pytest
from splinter import driver
from dotenv import load_dotenv, find_dotenv
import pytest
from time import sleep
#https://qxf2.com/blog/github-actions-to-execute-test-against-localhost-at-ci-stage/

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

#Fixture for Chrome
@pytest.fixture(scope="class")
def chrome_driver_init(request):
    chrome_driver = webdriver.Chrome()
    request.cls.driver = chrome_driver
    chrome_driver.get("https://practicespanishbuyflights.com/")
    load_dotenv(find_dotenv())
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env-pytest")
    load_dotenv(dotenv_path)
    yield
    chrome_driver.close()

@pytest.mark.usefixtures("chrome_driver_init")
class BasicTest:
    pass
class Test_URL(BasicTest):
        def test_open_url(self):
            find_title = self.driver.find_element(By.TAG_NAME, "h6") 
            assert find_title.text == "Practice Spanish, Buy Flights!"
            sleep(5)
        
        def test_login_boxes_and_button(self):
            username = self.driver.find_element(By.NAME, ('username'))
            test_username = os.getenv("test_username")
            username.send_keys(test_username)
            sleep(2)
            test_password = os.getenv("test_password")
            self.driver.find_element(By.NAME, ("password")).send_keys(test_password)
            sleep(2)
            self.driver.find_element(By.ID, "submit_button").click()
            home_page = self.driver.find_element(By.TAG_NAME, ('h4'))
            sleep(5)
            assert home_page.text == "Please select a level to practice a topic!" 




        