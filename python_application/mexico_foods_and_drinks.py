from flask import Blueprint, render_template
from flask import request, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import urllib
import urllib.request
import random
import boto3
import datetime
import pytz
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

dotenv_path = os.path.join(os.path.dirname(__file__), ".env-practice-spanish-buy-flights")
load_dotenv(dotenv_path)

DB_NAME = os.getenv("DB_NAME")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

client = boto3.client('secretsmanager', region_name='us-east-1')

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

load_dotenv(find_dotenv())

mexico_foods_and_drinks = Blueprint("mexico_foods_and_drinks", __name__)

@mexico_foods_and_drinks.route('/mexico_foods_and_drinks_page', methods=['GET'])
def mexico_foods_and_drinks_page():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE username = %s AND category = 'foods and drinks';", (session['username'],))

        word_learned_count = cursor.fetchone()[0]

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'foods and drinks' AND username = %s;", (session['username'],))
        my_dictionary_foods_and_drinks_count = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_food_or_drink WHERE username = %s;", (session['username'],))

        conn.commit()

        food_and_drink_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_foods_and_drinks"
        response = urllib.request.urlopen(food_and_drink_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_food_or_drink = random.choice(words)

        cursor.execute("INSERT INTO random_food_or_drink (random_food_or_drink, username) VALUES (%s, %s);", (random_food_or_drink, session['username']))
        conn.commit()
        conn.close()
        cursor.close()

        return render_template('mexico_foods_and_drinks_page.html', username=session['username'], overall_score=overall_score,
                            random_food_or_drink=random_food_or_drink, word_learned_count=word_learned_count,
                               my_dictionary_foods_and_drinks_count=my_dictionary_foods_and_drinks_count)

@mexico_foods_and_drinks.route('/mexico_foods_and_drinks_submit', methods=['POST'])
def mexico_foods_and_drinks_submit():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT random_food_or_drink FROM random_food_or_drink WHERE username = %s;', [session['username']])

        random_food_or_drink = cursor.fetchone()[0]

        date = datetime.date.today()

        format_code = '%m-%d-%y'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        translate_5 = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result_random_food_or_drink = translate_5.translate_text(Text=random_food_or_drink,
                                                  SourceLanguageCode="en", TargetLanguageCode="es")

        result_random_food_or_drink_answer = (result_random_food_or_drink.get('TranslatedText'))

        random_food_or_drink_submit = request.form.get('random_food_or_drink_submit')

        if result_random_food_or_drink_answer.replace(".","") == random_food_or_drink_submit:

            printed_answer_food_or_drink = f"Correct!, Your answer was '{random_food_or_drink_submit}' and the correct answer was '{result_random_food_or_drink_answer}'!"
            updated_overall_score_5 = overall_score + 1
            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], result_random_food_or_drink_answer))
            spanish_word_dictionary_check = cursor.fetchone()

            if spanish_word_dictionary_check:
                pass
            else:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (random_food_or_drink, result_random_food_or_drink_answer, session['username'], date_today, current_time, 'foods and drinks'))
                cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('foods and drinks', random_food_or_drink, result_random_food_or_drink_answer, 'correct', date_today, current_time, session['username']))

                cursor.execute("DELETE FROM random_places WHERE username = %s;", (session['username'],))
                conn.commit()

        else:
            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('foods and drinks', random_food_or_drink, result_random_food_or_drink_answer, 'incorrect', date_today, current_time, session['username']))

            printed_answer_food_or_drink = f"Incorrect, Your answer was '{random_food_or_drink_submit}' and the correct answer was '{result_random_food_or_drink_answer}'!"
            cursor.execute("DELETE FROM random_food_or_drink WHERE username = %s;", (session['username'],))
            conn.commit()

        cursor.close()
        conn.close()

        return render_template('mexico_foods_and_drinks_page.html', username=session['username'], overall_score=overall_score,
                               printed_answer_food_or_drink=printed_answer_food_or_drink,
                               random_food_or_drink=random_food_or_drink)

    return redirect(url_for('sign_up'))
