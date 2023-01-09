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

# Start environment variables #

load_dotenv(find_dotenv())

dotenv_path = os.path.join(os.path.dirname(__file__), ".env-practice-spanish-buy-flights")
load_dotenv(dotenv_path)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

DB_NAME = os.getenv("DB_NAME")

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

# End environment variables #

argentina_places = Blueprint("argentina_places", __name__)

@argentina_places.route('/place_guess_page_argentina', methods=['GET'])
def place_guess_page_argentina():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'places' AND username = %s;", (session['username'],))
        my_dictionary_places_count = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_places WHERE username = %s;", (session['username'],))

        conn.commit()

        date = datetime.date.today()

        format_code = '%m-%d-%Y'

        date_object = date.strftime(format_code)

        word_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_places.txt"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_place = random.choice(words)

        cursor.execute("INSERT INTO random_places (random_place, username) VALUES (%s, %s);", (random_place, session['username']))
        conn.commit()
        conn.close()
        cursor.close()

        return render_template('place_guess_page_argentina.html', username=session['username'], overall_score=overall_score,
                               date_object=date_object, random_place=random_place, my_dictionary_places_count=my_dictionary_places_count)

@argentina_places.route('/place_guess_page_argentina_with_ir', methods=['GET'])
def place_guess_page_argentina_with_ir():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_places WHERE username = %s;", (session['username'],))

        conn.commit()

        date = datetime.date.today()

        format_code = '%m-%d-%Y'

        date_object = date.strftime(format_code)

        word_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_places_with_ir"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_place_with_ir = random.choice(words)

        cursor.execute("INSERT INTO random_places (random_place, username) VALUES (%s, %s);", (random_place_with_ir, session['username']))
        conn.commit()
        conn.close()
        cursor.close()

        return render_template('place_guess_page_argentina.html', username=session['username'], overall_score=overall_score,
                               date_object=date_object, random_place_with_ir=random_place_with_ir)

    return redirect(url_for('sign_up'))

@argentina_places.route('/place_guess_page_argentina_submit', methods=['POST'])
def place_guess_page_argentina_submit():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT random_place FROM random_places WHERE username = %s;', [session['username']])

        random_place = cursor.fetchone()[0]

        translate_3 = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result_random_place = translate_3.translate_text(Text=random_place,
                                                  SourceLanguageCode="en", TargetLanguageCode="es")

        random_place_answer = (result_random_place.get('TranslatedText'))

        date = datetime.date.today()

        format_code = '%m-%d-%y'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        place_guess_page_argentina_submit = request.form.get('place_guess_page_argentina_submit')

        if random_place_answer == place_guess_page_argentina_submit:

            printed_answer_argentina_place = f"Correct!, Your answer was '{place_guess_page_argentina_submit}' and the correct answer was '{random_place_answer}'!"
            updated_overall_score_5 = overall_score + 1
            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))

            conn.commit()

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], random_place_answer))
            spanish_word_dictionary_check = cursor.fetchone()

            if spanish_word_dictionary_check:
                pass
            else:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (random_place, random_place_answer, session['username'], date_today, current_time, 'places'))
                cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('places', random_place, random_place_answer, 'correct', date_today, current_time, session['username']))

                cursor.execute("DELETE FROM random_places WHERE username = %s;", (session['username'],))
                conn.commit()

        else:
            printed_answer_argentina_place = f"Incorrect, Your answer was '{place_guess_page_argentina_submit}' and the correct answer was '{random_place_answer}'!"
            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('places', random_place, random_place_answer, 'incorrect', date_today, current_time, session['username']))

            cursor.execute("DELETE FROM random_places WHERE username = %s;", (session['username'],))

            conn.commit()

        cursor.close()
        conn.close()

        return render_template('place_guess_page_argentina.html', username=session['username'], overall_score=overall_score,
                               date_today=date_today, printed_answer_argentina_place=printed_answer_argentina_place,
                               random_place=random_place)

    return redirect(url_for('sign_up'))
