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

guatemala_greetings_and_farewells = Blueprint("guatemala_greetings_and_farewells", __name__)

@guatemala_greetings_and_farewells.route('/guatemala_greetings_and_farewells_page', methods=['GET'])
def guatemala_greetings_and_farewells_page():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'greetings and farewells' AND username = %s;", (session['username'],))
        my_dictionary_greetings_and_farewells_count = cursor.fetchone()[0]

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        file = open("greetings_and_farewells_dictionary.txt", "r")

        contents = file.read()
        greetings_and_farewells_dictionary = ast.literal_eval(contents)

        file.close()

        global random_greeting_or_farewell

        random_greeting_or_farewell = random.choice(list(greetings_and_farewells_dictionary.items()))

        global random_greeting_or_farewell_english
        random_greeting_or_farewell_english = random_greeting_or_farewell[0]

        global random_greeting_or_farewell_spanish
        random_greeting_or_farewell_spanish = random_greeting_or_farewell[1]

        cursor.close()
        conn.close()

        return render_template("guatemala_greetings_and_farewells_page.html", overall_score=overall_score, random_greeting_or_farewell=random_greeting_or_farewell,
                               random_greeting_or_farewell_english=random_greeting_or_farewell_english, random_greeting_or_farewell_spanish=random_greeting_or_farewell_spanish,
                               my_dictionary_greetings_and_farewells_count=my_dictionary_greetings_and_farewells_count)

    return redirect(url_for('sign_up'))

@guatemala_greetings_and_farewells.route('/guatemala_greetings_and_farewells_submit', methods=['POST'])
def guatemala_greetings_and_farewells_submit():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        guatemala_greetings_and_farewells_submit_button = request.form.get('guatemala_greetings_and_farewells_submit_button')

        translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result = translate.translate_text(Text=guatemala_greetings_and_farewells_submit_button,
                                          SourceLanguageCode="es", TargetLanguageCode="en")

        answer_translation = (result.get('TranslatedText')).replace("do", "")

        date = datetime.date.today()

        format_code = '%m-%d-%y'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        single_quote = "'"

        random_greeting_or_farewell_spanish_display = random_greeting_or_farewell[1]

        if guatemala_greetings_and_farewells_submit_button == random_greeting_or_farewell_spanish:
            printed_answer_greetings_or_farewell = f"Correct! Your answer was '{guatemala_greetings_and_farewells_submit_button}' and the correct answer was '{random_greeting_or_farewell_spanish_display}'!"
            updated_overall_score_5 = overall_score + 1

            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))
            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, username, date_added, time_added) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('greetings and farewells', random_greeting_or_farewell_english, random_greeting_or_farewell_spanish, 'correct', session['username'], date_today, current_time))

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], random_greeting_or_farewell_spanish))
            spanish_word_dictionary_check = cursor.fetchone()

            if spanish_word_dictionary_check:
                pass
            else:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (random_greeting_or_farewell_english, random_greeting_or_farewell_spanish, session['username'], date_today, current_time, 'greetings and farewells'))
                conn.commit()
        else:
            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('greetings and farewells', random_greeting_or_farewell_english, random_greeting_or_farewell_spanish, 'incorrect', date_today, current_time, session['username']))
            printed_answer_greetings_or_farewell = f"Incorrect, your answer was '{guatemala_greetings_and_farewells_submit_button}' and the correct answer was '{random_greeting_or_farewell_spanish_display}'!"

        It_means = "It means"
        conn.commit()
        cursor.close()
        conn.close()

        return render_template("guatemala_greetings_and_farewells_page.html", overall_score=overall_score,
                               printed_answer_greetings_or_farewell=printed_answer_greetings_or_farewell, answer_translation=answer_translation,
                               It_means=It_means, single_quote=single_quote)

    return redirect(url_for('sign_up'))

@guatemala_greetings_and_farewells.route('/guatemala_chatbot', methods=['POST'])
def guatemala_chatbot():
    if 'loggedin' in session:

        client = boto3.client('lexv2-runtime')

        response = client.recognize_text(
        botId='WNDVSKTNZ8',
        botAliasId='8KKRXSEBX1',
        localeId='en_US',
        sessionId='test_session',
        text=request.form.get('guatemala_chatbot'))

        response = response["messages"][0]['content']

        return render_template("guatemala_greetings_and_farewells_page.html", response=response)

    return redirect(url_for('sign_up'))
