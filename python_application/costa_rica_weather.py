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

# End environment variables #

costa_rica_weather = Blueprint("costa_rica_weather", __name__)

@costa_rica_weather.route('/costa_rica_weather_page', methods=['GET'])
def costa_rica_weather_page():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE username = %s AND category = 'weather';", (session['username'],))

        my_dictionary_weather_count = cursor.fetchone()[0]

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        file = open("costa_rica_weather.txt", "r")

        contents = file.read()
        costa_rica_weather_dictionary = ast.literal_eval(contents)

        file.close()

        global random_weather

        random_weather = random.choice(list(costa_rica_weather_dictionary.items()))

        global random_weather_english
        random_weather_english = random_weather[0]

        global random_weather_spanish
        random_weather_spanish = random_weather[1]

        cursor.close()
        conn.close()

        return render_template("costa_rica_weather.html", overall_score=overall_score, random_weather=random_weather,
                               random_weather_english=random_weather_english, random_weather_spanish=random_weather_spanish,
                               my_dictionary_weather_count=my_dictionary_weather_count)

    return redirect(url_for('sign_up'))

@costa_rica_weather.route('/costa_rica_weather_submit', methods=['POST'])
def costa_rica_weather_submit():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        costa_rica_weather_submit_button = request.form.get('costa_rica_weather_submit_button')

        translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result = translate.translate_text(Text=costa_rica_weather_submit_button,
                                          SourceLanguageCode="es", TargetLanguageCode="en")

        answer_translation = (result.get('TranslatedText'))

        date = datetime.date.today()

        format_code = '%m-%d-%y'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        single_quote = "'"

        global random_weather_spanish

        if costa_rica_weather_submit_button == random_weather_spanish:
            printed_answer_weather = f"Correct! Your answer was '{costa_rica_weather_submit_button}' and the correct answer was '{random_weather_spanish}'!"
            updated_overall_score_5 = overall_score + 1

            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))

            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, username, date_added, time_added) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('dates', random_weather_english, random_weather_spanish, 'correct', session['username'], date_today, current_time))

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], costa_rica_weather_submit_button))
            spanish_word_dictionary_check = cursor.fetchone()

            if spanish_word_dictionary_check:
                pass
            else:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (random_weather_english, random_weather_spanish, session['username'], date_today, current_time, 'weather'))
                conn.commit()
        else:
            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('weather', random_weather_english, random_weather_spanish, 'incorrect', date_today, current_time, session['username']))
            printed_answer_weather = f"Incorrect, your answer was '{costa_rica_weather_submit_button}' and the correct answer was '{random_weather_spanish}'!"

        It_means = "It means"
        conn.commit()
        cursor.close()
        conn.close()

        return render_template("costa_rica_weather.html", overall_score=overall_score,
                               printed_answer_weather=printed_answer_weather, answer_translation=answer_translation,
                               It_means=It_means, single_quote=single_quote)

    return redirect(url_for('sign_up'))
