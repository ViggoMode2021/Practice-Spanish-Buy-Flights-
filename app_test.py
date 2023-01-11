import psycopg2
import psycopg2.extras
import os
import boto3
import pytest
from splinter import Browser

#from python_application.application import sign_up
#import python_application.application as app

DB_NAME = os.getenv("DB_NAME")

secret_name_COGNITO_USER_CLIENT_ID = "arn:aws:secretsmanager:us-east-1:583715230104:secret:Cognito_User_Client_ID-ft88TW"
region_name = "us-east-1"

# Create a Secrets Manager client
client = boto3.client('secretsmanager', region_name='us-east-1')

get_secret_value_response = client.get_secret_value(
            SecretId=secret_name_COGNITO_USER_CLIENT_ID
        )

COGNITO_USER_CLIENT_ID = get_secret_value_response['SecretString']

secret_name_DATABASE_HOST = "arn:aws:secretsmanager:us-east-1:583715230104:secret:DB_ENDPOINT-OgYTNa"

get_secret_value_response_2 = client.get_secret_value(
    SecretId=secret_name_DATABASE_HOST
)

DB_HOST = get_secret_value_response_2['SecretString']

secret_name_DATABASE_PASS = "arn:aws:secretsmanager:us-east-1:583715230104:secret:DB_PASS-hqj9lH"

get_secret_value_response_3 = client.get_secret_value(
    SecretId=secret_name_DATABASE_PASS
)

DB_PASS = get_secret_value_response_3['SecretString']

secret_name_DB_USER = "arn:aws:secretsmanager:us-east-1:583715230104:secret:DB_USER-lyKZpQ"

get_secret_value_response_4 = client.get_secret_value(
    SecretId=secret_name_DB_USER
)

DB_USER = get_secret_value_response_4['SecretString']

secret_name_SECRET_KEY = "arn:aws:secretsmanager:us-east-1:583715230104:secret:SECRET_KEY-C502Wx"

get_secret_value_response_5 = client.get_secret_value(
    SecretId=secret_name_SECRET_KEY
)

def test_db_connection():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    test_query = cursor.execute("SELECT username FROM spanish_users WHERE username = 'bburnerson840@gmail.com';")

    test_result_db = cursor.fetchone()[0]

    assert test_result_db == 'bburnerson840@gmail.com'

@pytest.fixture()
def setup(request):
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())

    chrome_options = Options()
    options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
    for option in options:
        chrome_options.add_argument(option)

    request.cls.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


    yield request.cls.driver
    request.cls.driver.close()

def test_text_present():
    browser = Browser()
    url = 'https://practicespanishbuyflights.com/'
    browser.visit(url)
    assert browser.is_text_present('Practice Spanish, Buy Flights!')
    browser.quit()

def test_text_present():
    browser = Browser()
    url = 'https://practicespanishbuyflights.com/'
    browser.visit(url)
    assert browser.is_text_present('Practice Spanish, Buy Flights!')
    browser.quit()

def test_search_engine_optimization(browser):
    """Test using real browser."""
    url = "http://www.google.com"
    browser.visit(url)
    browser.fill('q', 'Practice Spanish Buy Flights')
    # Find and click the 'search' button
    button = browser.find_by_name('btnK')
    # Interact with elements
    button.click()
    assert browser.is_text_present('Practice Spanish Buy Flights!'), "Not found - let's get on that SEO GAME LIKE A GURU!"
