from flask import Blueprint, render_template
from flask import request, flash, session, redirect, url_for
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

paraguay_adjectives = Blueprint("paraguay_adjectives", __name__)

@paraguay_adjectives.route('/paraguay_adjectives_page', methods=['GET'])
def paraguay_adjectives_page():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'adjectives' AND username = %s;", (session['username'],))
        my_dictionary_adjectives_count = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_adjectives WHERE username = %s;", (session['username'],))

        conn.commit()

        adjective_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_adjectives"
        response = urllib.request.urlopen(adjective_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_adjective = random.choice(words)

        cursor.execute("INSERT INTO random_adjectives (random_adjectives, username) VALUES (%s, %s);", (random_adjective, session['username']))
        conn.commit()
        conn.close()
        cursor.close()

        return render_template('paraguay_adjectives.html', username=session['username'], overall_score=overall_score,
                            random_adjective=random_adjective,my_dictionary_adjectives_count=my_dictionary_adjectives_count)

@paraguay_adjectives.route('/paraguay_adjectives_submit', methods=['POST'])
def paraguay_adjectives_submit():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT random_adjectives FROM random_adjectives WHERE username = %s;', [session['username']])

        random_adjective = cursor.fetchone()[0]

        translate_4 = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result_random_adjective = translate_4.translate_text(Text=random_adjective,
                                                  SourceLanguageCode="en", TargetLanguageCode="es")

        random_adjective_answer = (result_random_adjective.get('TranslatedText'))

        date = datetime.date.today()

        format_code = '%m-%d-%y'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        random_adjective_submit = request.form.get('random_adjective_submit')

        if random_adjective_answer.replace(".","") == random_adjective_submit:

            printed_answer_paraguay_adjective = f"Correct!, Your answer was '{random_adjective_submit}' and the correct answer was '{random_adjective_answer}'!"
            updated_overall_score_5 = overall_score + 1
            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))

            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, username, date_added, time_added) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('adjectives', random_adjective, random_adjective_answer, 'correct', session['username'], date_today, current_time))

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], random_adjective_answer))
            spanish_word_dictionary_check = cursor.fetchone()

            if spanish_word_dictionary_check:
                pass
            else:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (random_adjective, random_adjective_answer, session['username'], date_today, current_time, 'adjectives'))
                conn.commit()
        else:
            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('adjectives', random_adjective, random_adjective_answer, 'incorrect', date_today, current_time, session['username']))

            printed_answer_paraguay_adjective = f"Incorrect, Your answer was '{random_adjective_submit}' and the correct answer was '{random_adjective_answer}'!"
            cursor.execute("DELETE FROM random_adjectives WHERE username = %s;", (session['username'],))
            conn.commit()

        cursor.close()
        conn.close()

        return render_template('paraguay_adjectives.html', username=session['username'], overall_score=overall_score,
                               printed_answer_paraguay_adjective=printed_answer_paraguay_adjective,
                               random_adjective_answer=random_adjective_answer)

    return redirect(url_for('sign_up'))
