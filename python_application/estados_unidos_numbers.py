from flask import Blueprint, render_template
from flask import request, flash, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
#from num2words import num2words
import datetime
import pytz
import boto3
import random
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

estados_unidos_numbers = Blueprint("estados_unidos_numbers", __name__)

@estados_unidos_numbers.route('/number_guess_page_range', methods=['GET'])
def number_guess_page_range():
    if 'loggedin' in session:

        return render_template('number_guess_page_range.html')

    return redirect(url_for('sign_up'))

@estados_unidos_numbers.route('/number_guess_page_range_submit', methods=['POST','GET'])
def number_guess_page_range_submit():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("DELETE FROM random_numbers WHERE username = %s;", (session['username'],))
        conn.commit()

        number_guess_page_range_1 = request.form.get("number_guess_page_range_1")

        number_guess_page_range_2 = request.form.get("number_guess_page_range_2")

        global first_number_range
        first_number_range = int(number_guess_page_range_1)

        global second_number_range

        second_number_range = int(number_guess_page_range_2)

        if first_number_range > second_number_range:
            flash('Ending number needs to be higher than starting number.')
            return redirect(url_for('estados_unidos_numbers.number_guess_page_range'))

        cursor.execute("INSERT INTO random_numbers (random_number_one, random_number_two, username) VALUES (%s, %s, %s);", (first_number_range, second_number_range, session['username']))
        conn.commit()
        conn.close()
        cursor.close()

        return redirect(url_for('estados_unidos_numbers.number_guess_page_us'))

    return redirect(url_for('sign_up'))

@estados_unidos_numbers.route('/number_guess_page_us', methods=['POST','GET'])
def number_guess_page_us():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()

        session['overall_score'] = overall_score[0]

        cursor.execute('SELECT random_number_one FROM random_numbers WHERE username = %s;', [session['username']])

        random_number_one = cursor.fetchone()[0]

        cursor.execute('SELECT random_number_two FROM random_numbers WHERE username = %s;', [session['username']])

        random_number_two = cursor.fetchone()[0]

        global num_1
        num_1 = random.randint(random_number_one, random_number_two)

        cursor.close()
        conn.close()

        date = datetime.date.today()

        format_code = '%m-%d-%Y'

        date_object = date.strftime(format_code)

        return render_template('number_guess_page_us.html', username=session['username'], overall_score=session['overall_score'],
                               date_object=date_object, num_1=num_1, first_number_range=first_number_range, second_number_range=second_number_range)

    return redirect(url_for('sign_up'))

@estados_unidos_numbers.route('/number_guess_submit_us', methods=['POST', 'GET'])
def number_guess_submit_us():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score_for_points = cursor.fetchone()[0]

        date = datetime.date.today()

        format_code = '%m-%d-%y'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        number_guess_submit = request.form.get("number_guess_submit")

        translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        global num_1
        num_2 = num2words(num_1)

        result = translate.translate_text(Text=num_2,
                                          SourceLanguageCode="en", TargetLanguageCode="es")

        answer = (result.get('TranslatedText'))

        if answer == number_guess_submit:

            printed_answer_number = f"Correct!, Your answer was '{number_guess_submit}' and the correct answer was '{answer}'!"
            updated_overall_score_5 = overall_score_for_points + 1
            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], answer))
            spanish_word_dictionary_check = cursor.fetchone()

            if spanish_word_dictionary_check:
                pass
            else:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (num_1, answer, session['username'], date_today, current_time, 'numbers'))

                cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('numbers', num_1, answer, 'correct', date_today, current_time, session['username']))

        else:
            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, date_added, time_added, username) VALUES (%s,%s,%s,%s,%s,%s,%s);", ('numbers', num_1, answer, 'incorrect', date_today, current_time, session['username']))

            printed_answer_number = f"Incorrect, Your answer was '{number_guess_submit}' and the correct answer was '{answer}'!"

        conn.commit()
        cursor.close()
        conn.close()

        return render_template('number_guess_page_us.html', username=session['username'], overall_score=session['overall_score'],
                               printed_answer_number=printed_answer_number)

    return redirect(url_for('sign_up'))
