import psycopg2
import psycopg2.extras
import os
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

'''def test_db_connection():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    test_query = cursor.execute("SELECT username FROM spanish_users WHERE username = 'bburnerson840@gmail.com';")

    test_result_db = cursor.fetchone()[0]

    assert test_result_db == 'bburnerson840@gmail.com'''
'''
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def order(first_entry):
    return [first_entry]


def test_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]
'''
#Fixture for Chrome
@pytest.fixture(scope="class")
def chrome_driver_init(request):
    chrome_driver = webdriver.Chrome()
    request.cls.driver = chrome_driver
    chrome_driver.get("https://practicespanishbuyflights.com/")
    print(chrome_driver.title + "this is a test")
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
            find_username = self.driver.find_element(By.NAME, ("username")).send_keys("test@gmail.com")
            self.driver.find_element_by_id("addbutton").click()


        