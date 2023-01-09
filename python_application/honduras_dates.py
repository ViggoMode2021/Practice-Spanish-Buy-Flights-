from flask import Blueprint, render_template, request, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import random
import boto3
import ast
import datetime
import pytz
from dotenv import load_dotenv, find_dotenv
import urllib

# Start environment variables #

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

# End environment variables #

honduras_dates = Blueprint("honduras_dates", __name__)

@honduras_dates.route('/honduras_dates_page', methods=['GET'])
def honduras_dates_page():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        word_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_places.txt"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()

        words = ast.literal_eval(long_txt)

        random_place = random.choice(words)

        global random_date

        random_date = random.choice(list(random_place.items()))

        global random_date_english
        random_date_english = random_date[0]

        global random_date_spanish
        random_date_spanish = random_date[1]

        cursor.close()
        conn.close()

        return render_template("honduras_dates.html", overall_score=overall_score, random_date=random_date,
                               random_date_english=random_date_english, random_date_spanish=random_date_spanish)

    return redirect(url_for('sign_up'))

@honduras_dates.route('/honduras_dates_submit', methods=['POST'])
def honduras_dates_submit():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        honduras_dates_submit_button = request.form.get('honduras_dates_submit_button')

        translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result = translate.translate_text(Text=honduras_dates_submit_button,
                                          SourceLanguageCode="es", TargetLanguageCode="en")

        answer_translation = (result.get('TranslatedText')).replace("do", "")

        date = datetime.date.today()

        format_code = '%m-%d-%y'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        single_quote = "'"

        global random_greeting_or_farewell_spanish

        if honduras_dates_submit_button == random_date_spanish:
            printed_answer_date = f"Correct! Your answer was '{honduras_dates_submit_button}' and the correct answer was '{random_date_spanish}'!"
            updated_overall_score_5 = overall_score + 1

            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))

            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, username, date_added, time_added) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('dates', random_date_english, random_date_spanish, 'correct', session['username'], date_today, current_time))

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], honduras_dates_submit_button))
            spanish_word_dictionary_check = cursor.fetchone()

            if spanish_word_dictionary_check:
                pass
            else:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (random_date_english, random_date_spanish, session['username'], date_today, current_time, 'dates'))
                conn.commit()
        else:
            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('dates', random_date_english, random_date_spanish, 'incorrect', date_today, current_time, session['username']))
            printed_answer_date = f"Incorrect, your answer was '{honduras_dates_submit_button}' and the correct answer was '{random_date_spanish}'!"

            It_means = "It means"
            conn.commit()
            cursor.close()
            conn.close()

        return render_template("honduras_dates.html", overall_score=overall_score,
                               printed_answer_date=printed_answer_date, answer_translation=answer_translation,
                               It_means=It_means, single_quote=single_quote)

    return redirect(url_for('sign_up'))
