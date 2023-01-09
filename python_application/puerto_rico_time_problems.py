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

puerto_rico_time_problems = Blueprint("puerto_rico_time_problems", __name__)

# code functions below

@puerto_rico_time_problems.route('/time_problems_puerto_rico', methods=['GET'])
def time_problems_puerto_rico():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_times WHERE username = %s;", (session['username'],))

        conn.commit()

        time_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_times.txt"
        response = urllib.request.urlopen(time_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_time = random.choice(words)

        cursor.execute("INSERT INTO random_times (random_time, username) VALUES (%s, %s);", (random_time, session['username']))
        conn.commit()
        conn.close()
        cursor.close()

        return render_template('time_problems_puerto_rico.html', username=session['username'], overall_score=overall_score,
                            random_time=random_time)

@puerto_rico_time_problems.route('/time_problems_puerto_rico_submit', methods=['POST'])
def time_problems_puerto_rico_submit():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT random_time FROM random_times WHERE username = %s;', [session['username']])

        random_time = cursor.fetchone()[0]

        translate_4 = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result_random_time = translate_4.translate_text(Text=random_time,
                                                  SourceLanguageCode="en", TargetLanguageCode="es")

        random_time_answer = (result_random_time.get('TranslatedText'))

        time_guess_page_puerto_rico_submit = request.form.get('time_guess_page_puerto_rico_submit')

        date = datetime.date.today()

        format_code = '%m-%d-%y'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        if random_time_answer.replace(".","") == time_guess_page_puerto_rico_submit:

            printed_answer_puerto_rico_time = f"Correct!, Your answer was '{time_guess_page_puerto_rico_submit}' and the correct answer was '{random_time_answer}'!"
            updated_overall_score_5 = overall_score + 2
            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))
            cursor.execute("INSERT INTO user_practice_records (category_name, correct_incorrect, english_word, spanish_word, username, date_added, time_added) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('times', random_time, time_guess_page_puerto_rico_submit, 'correct', session['username'], date_today, current_time))

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], time_guess_page_puerto_rico_submit))
            spanish_word_dictionary_check = cursor.fetchone()

            if spanish_word_dictionary_check:
                pass
            else:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (random_time, time_guess_page_puerto_rico_submit, session['username'], date_today, current_time, 'times'))

        else:
            printed_answer_puerto_rico_time = f"Incorrect, Your answer was '{time_guess_page_puerto_rico_submit}' and the correct answer was '{random_time_answer}'!"
            cursor.execute("DELETE FROM random_times WHERE username = %s;", (session['username'],))
            cursor.execute("INSERT INTO user_practice_records (category_name, correct_incorrect, english_word, spanish_word, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('times', random_time, time_guess_page_puerto_rico_submit, 'incorrect', date_today, current_time, session['username']))

        conn.commit()
        cursor.close()
        conn.close()

        return render_template('time_problems_puerto_rico.html', username=session['username'], overall_score=overall_score,
                               printed_answer_puerto_rico_time=printed_answer_puerto_rico_time,
                               random_time=random_time)

    return redirect(url_for('sign_up'))


