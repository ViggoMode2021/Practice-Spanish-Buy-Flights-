from flask import Blueprint, render_template
from flask import request, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import random
import boto3
import datetime
from dotenv import load_dotenv, find_dotenv
import ast
import pytz

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

colombia_verbs = Blueprint("colombia_verbs", __name__)

@colombia_verbs.route('/word_guess_page_colombia', methods=['GET'])
def word_guess_page_colombia():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        boto3.client('translate', region_name="us-east-1")

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'verbs' AND username = %s;", (session['username'],))
        my_dictionary_verbs_count = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_verbs WHERE username = %s;", (session['username'],))

        conn.commit()

        date = datetime.date.today()

        format_code = '%m-%d-%Y'

        date_object = date.strftime(format_code)

        file = open("verbs.txt", "r")

        contents = file.read()
        verbs_dictionary = ast.literal_eval(contents)

        file.close()

        global random_verb

        random_verb = random.choice(list(verbs_dictionary.items()))

        global random_verb_english
        random_verb_english = random_verb[0]

        global random_verb_spanish
        random_verb_spanish = random_verb[1].replace("tÃº", "tú")

        cursor.close()
        conn.close()

        return render_template('word_guess_page_colombia.html', username=session['username'], overall_score=overall_score,
                               date_object=date_object, random_verb=random_verb, my_dictionary_verbs_count=my_dictionary_verbs_count,
                               random_verb_english=random_verb_english, random_verb_spanish=random_verb_spanish)

    return redirect(url_for('sign_up'))

@colombia_verbs.route('/word_guess_page_colombia_present_tense', methods=['GET'])
def word_guess_page_colombia_present_tense():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        boto3.client('translate', region_name="us-east-1")

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'verbs' AND username = %s;", (session['username'],))
        my_dictionary_verbs_count = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_verbs WHERE username = %s;", (session['username'],))

        conn.commit()

        date = datetime.date.today()

        format_code = '%m-%d-%Y'

        date_object = date.strftime(format_code)

        file = open("verbs.txt", "r")

        contents = file.read()
        verbs_dictionary = ast.literal_eval(contents)

        file.close()

        global random_verb

        random_verb = random.choice(list(verbs_dictionary.items()))

        global random_verb_english
        random_verb_english = random_verb[0]

        global random_verb_spanish
        random_verb_spanish = random_verb[1].replace("tÃº", "tú")

        cursor.close()
        conn.close()

        return render_template('word_guess_page_colombia.html', username=session['username'], overall_score=overall_score,
                               date_object=date_object, random_verb_english=random_verb_english, random_verb_spanish=random_verb_spanish)

    return redirect(url_for('sign_up'))

@colombia_verbs.route('/word_guess_page_colombia_submit', methods=['POST'])
def word_guess_page_colombia_submit():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        date = datetime.date.today()

        format_code = '%m-%d-%Y'

        date_object = date.strftime(format_code)

        word_guess_page_colombia_submit = request.form.get('word_guess_page_colombia_submit')

        translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result = translate.translate_text(Text=word_guess_page_colombia_submit,
                                          SourceLanguageCode="es", TargetLanguageCode="en")

        answer_translation = result.get('TranslatedText')

        date = datetime.date.today()

        format_code = '%m-%d-%y'

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        global random_verb_spanish_selection

        if random_verb_spanish == word_guess_page_colombia_submit:

            printed_answer_colombia_word = f"Correct!, Your answer was '{word_guess_page_colombia_submit}' and the correct answer was '{random_verb_spanish}'!"
            updated_overall_score_5 = overall_score + 1
            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], random_verb_spanish))
            spanish_word_dictionary_check = cursor.fetchone()

            if spanish_word_dictionary_check:
                pass
            else:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (random_verb_english, random_verb_spanish, session['username'], date_object, current_time, 'verbs'))
                cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, username) VALUES (%s,%s,%s,%s,%s);", ('verbs', random_verb_english, random_verb_spanish, 'correct', session['username']))
                conn.commit()

        else:
            printed_answer_colombia_word = f"Incorrect, Your answer was '{word_guess_page_colombia_submit}' and the correct answer was '{random_verb_spanish}'!"
            cursor.execute("INSERT INTO user_practice_records (category_name, english_word, spanish_word, correct_incorrect, username) VALUES (%s,%s,%s,%s,%s);", ('verbs', random_verb_english, random_verb_spanish, 'incorrect', session['username']))
            conn.commit()

        cursor.close()
        conn.close()

        return render_template('word_guess_page_colombia.html', username=session['username'], overall_score=overall_score,
                               date_object=date_object, printed_answer_colombia_word=printed_answer_colombia_word,
                               random_verb=random_verb, answer_translation=answer_translation)

    return redirect(url_for('sign_up'))
