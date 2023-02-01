from flask import Flask, render_template, request, flash, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import boto3
from dotenv import load_dotenv, find_dotenv
import datetime
from botocore.exceptions import ClientError

# Module imports -
from puerto_rico_time_problems import puerto_rico_time_problems
from estados_unidos_numbers import estados_unidos_numbers
from colombia_verbs import colombia_verbs
from argentina_places import argentina_places
from peru_speaking import peru_speaking
from spain_listening import spain_listening
from paraguay_adjectives import paraguay_adjectives
from mexico_foods_and_drinks import mexico_foods_and_drinks
from verb_conjugation_practice import verb_conjugation_practice
from guatemala_greetings_and_farewells import guatemala_greetings_and_farewells
from honduras_dates import honduras_dates
from costa_rica_weather import costa_rica_weather
from venezuela_conversation import venezuela_conversation

#Module imports for misc functionalities and pages
from flights import flights
from flight_colombia import flight_colombia
from flight_peru import flight_peru
from flight_spain import flight_spain
from words_to_study_algorithms import words_to_study_algorithms

# For main app. This file contains functions in relation to user authentication and other miscellaneous tasks.
application = Flask(__name__)

# Blueprints for Spanish practice .py files. These are broken up into modules for different pages/tasks.
application.register_blueprint(puerto_rico_time_problems)
application.register_blueprint(words_to_study_algorithms)
application.register_blueprint(estados_unidos_numbers)
application.register_blueprint(colombia_verbs)
application.register_blueprint(argentina_places)
application.register_blueprint(peru_speaking)
application.register_blueprint(spain_listening)
application.register_blueprint(paraguay_adjectives)
application.register_blueprint(mexico_foods_and_drinks)
application.register_blueprint(verb_conjugation_practice)
application.register_blueprint(guatemala_greetings_and_farewells)
application.register_blueprint(honduras_dates)
application.register_blueprint(costa_rica_weather)
application.register_blueprint(venezuela_conversation)

# Blueprints for .py files for flights:

application.register_blueprint(flights)
application.register_blueprint(flight_colombia)
application.register_blueprint(flight_peru)
application.register_blueprint(flight_spain)

#@ Load and assign environment variables below:

load_dotenv(find_dotenv())

dotenv_path = os.path.join(os.path.dirname(__file__), ".env-practice-spanish-buy-flights")
load_dotenv(dotenv_path)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

DB_NAME = os.getenv("DB_NAME")

secret_name_COGNITO_USER_CLIENT_ID = "arn:aws:secretsmanager:us-east-1:583715230104:secret:Cognito_User_Client_ID-ft88TW"
region_name = "us-east-1"

# Create a Secrets Manager client!
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

SECRET_KEY = get_secret_value_response_5['SecretString']

application.secret_key = SECRET_KEY

# End environment variables #

@application.route('/')
def sign_up():
    return render_template("sign_up.html")

@application.route('/sign_up_submit', methods=['POST'])
def sign_up_submit():
    try:
        email_sign_up = request.form.get("email_sign_up")
        password_sign_up = request.form.get("password_sign_up")

        client = boto3.client("cognito-idp", region_name="us-east-1")

        # The below code, will do the sign-up
        client.sign_up(
            ClientId=COGNITO_USER_CLIENT_ID,
            Username=email_sign_up,
            Password=password_sign_up,
            UserAttributes=[{"Name": "email", "Value": email_sign_up}],
        )

        session['loggedin'] = True

        session['username'] = email_sign_up

        return redirect(url_for('authenticate_page'))

    except ClientError as e:
        flash("Incorrect credentials or user is already in the system.")
        return redirect(url_for('sign_up'))

@application.route('/authenticate_page', methods=['GET'])
def authenticate_page():
    if 'loggedin' in session:
        return render_template('authenticate.html')

    return redirect(url_for('sign_up'))

@application.route('/authenticate', methods=['POST'])
def authenticate():
    try:
        if 'loggedin' in session:
            authentication_code = request.form.get('authentication_code')
            client = boto3.client("cognito-idp", region_name="us-east-1")

            client.confirm_sign_up(
                ClientId=COGNITO_USER_CLIENT_ID,
                Username=session['username'],
                ConfirmationCode=authentication_code,
                ForceAliasCreation=False
            )

            flash('You have authenticated!')

            date = datetime.date.today()

            format_code = '%m-%d-%Y'

            date_object = date.strftime(format_code)

            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cursor.execute(
                "INSERT INTO spanish_users (username, overall_score, account_creation_date) VALUES (%s, %s, %s);",
                (session['username'], 0, date_object))

            conn.commit()

            cursor.close()
            conn.close()

            session.pop('username')

            return redirect(url_for('sign_up'))

    except ClientError as e:
        flash("Incorrect authentication code")
        return redirect(url_for('authenticate_page'))

    return redirect(url_for('sign_up'))

@application.route('/login_page', methods=['POST', 'GET'])
def login_page():
    return render_template('sign_up.html')

@application.route('/login', methods=['POST', 'GET'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        client = boto3.client("cognito-idp", region_name="us-east-1")

        client.initiate_auth(
            ClientId=COGNITO_USER_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )

        session['loggedin'] = True

        session['username'] = username

        return redirect(url_for('level_selector'))

    except:
        flash('Username or password incorrect, or user is not in the system.')
        return redirect(url_for('sign_up'))

@application.route('/home', methods=['GET'])
def home_page():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        score = cursor.fetchone()[0]

        cursor.execute('SELECT account_creation_date FROM spanish_users WHERE username = %s;', [session['username']])

        account_creation_date = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('home_page.html', username=session['username'], score=score, account_creation_date=account_creation_date)

    return redirect(url_for('login'))

@application.route('/my_dictionary')
def my_dictionary():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s;', (session['username'],))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- all words"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE username = %s;", (session['username'],))
        my_dictionary_total_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_total_count=my_dictionary_total_count)

    return redirect(url_for('login'))

@application.route('/my_dictionary_places')
def my_dictionary_places():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s AND category = %s ORDER BY '
                       'date_added_on ASC;', (session['username'], 'places'))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- places"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'places' AND username = %s;", (session['username'],))
        my_dictionary_places_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_places_count=my_dictionary_places_count)

    return redirect(url_for('login'))

@application.route('/my_dictionary_times')
def my_dictionary_times():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s AND category = %s ORDER BY '
                       'date_added_on ASC;', (session['username'], 'times'))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- times"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'times' AND username = %s;", (session['username'],))
        my_dictionary_times_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_times_count=my_dictionary_times_count)

    return redirect(url_for('login'))

@application.route('/my_dictionary_numbers')
def my_dictionary_numbers():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s AND category = %s ORDER BY '
                       'date_added_on ASC;', (session['username'], 'numbers'))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- numbers"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'numbers' AND username = %s;", (session['username'],))
        my_dictionary_numbers_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_numbers_count=my_dictionary_numbers_count)

    return redirect(url_for('login'))

@application.route('/my_dictionary_adjectives')
def my_dictionary_adjectives():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s AND category = %s ORDER BY '
                       'date_added_on ASC;', (session['username'], 'adjectives'))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- adjectives"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'adjectives' AND username = %s;", (session['username'],))
        my_dictionary_adjectives_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_adjectives_count=my_dictionary_adjectives_count)

    return redirect(url_for('login'))

@application.route('/my_dictionary_foods_and_drinks')
def my_dictionary_foods_and_drinks():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s AND category = %s ORDER BY '
                       'date_added_on ASC;', (session['username'], 'foods and drinks'))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- foods and drinks"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'foods and drinks' AND username = %s;", (session['username'],))
        my_dictionary_foods_and_drinks_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_foods_and_drinks_count=my_dictionary_foods_and_drinks_count)

    return redirect(url_for('login'))

@application.route('/my_dictionary_greetings_and_farewells')
def my_dictionary_greetings_and_farewells():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s AND category = %s ORDER BY '
                       'date_added_on ASC;', (session['username'], 'greetings and farewells'))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- greetings and farewells"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'greetings and farewells' AND username = %s;", (session['username'],))
        my_dictionary_greetings_and_farewells_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_greetings_and_farewells_count=my_dictionary_greetings_and_farewells_count)

    return redirect(url_for('login'))

@application.route('/my_dictionary_dates')
def my_dictionary_dates():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s AND category = %s ORDER BY '
                       'date_added_on ASC;', (session['username'], 'dates'))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- dates"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'dates' AND username = %s;", (session['username'],))
        my_dictionary_dates_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_dates_count=my_dictionary_dates_count)

    return redirect(url_for('login'))

@application.route('/my_dictionary_weather')
def my_dictionary_weather():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s AND category = %s ORDER BY '
                       'date_added_on ASC;', (session['username'], 'weather'))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- weather"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'weather' AND username = %s;", (session['username'],))
        my_dictionary_weather_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_weather_count=my_dictionary_weather_count)

    return redirect(url_for('login'))

@application.route('/my_dictionary_questions')
def my_dictionary_questions():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT id, english_word, spanish_word, date_added_on, time_added_on, category FROM dictionary_of_words WHERE username = %s AND category = %s ORDER BY '
                       'date_added_on ASC;', (session['username'], 'questions'))

        my_dictionary = cursor.fetchall()

        dictionary_sort_type = "- questions"

        cursor.execute("SELECT COUNT (*) FROM dictionary_of_words WHERE category = 'questions' AND username = %s;", (session['username'],))
        my_dictionary_questions_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('my_dictionary.html', overall_score=overall_score, username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, dictionary_sort_type=dictionary_sort_type,
                               my_dictionary_questions_count=my_dictionary_questions_count)

    return redirect(url_for('login'))

@application.route('/study_list')
def study_list():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT COUNT (*) FROM user_practice_records WHERE category_name = 'verbs' AND correct_incorrect = 'correct' AND username = %s;", (session['username'],))
        verbs_correct = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'verbs' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        verbs_incorrect = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'adjectives' AND correct_incorrect = 'correct' AND username = %s;", (session['username'],))
        adjectives_correct = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'adjectives' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        adjectives_incorrect = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'times' AND correct_incorrect = 'correct' AND username = %s;", (session['username'],))
        times_correct = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'times' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        times_incorrect = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'numbers' AND correct_incorrect = 'correct' AND username = %s;", (session['username'],))
        numbers_correct = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'numbers' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        numbers_incorrect = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'places' AND correct_incorrect = 'correct' AND username = %s;", (session['username'],))
        places_correct = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'places' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        places_incorrect = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'foods and drinks' AND correct_incorrect = 'correct' AND username = %s;", (session['username'],))
        foods_and_drinks_correct = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'foods and drinks' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        foods_and_drinks_incorrect = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'greetings and farewells' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        greetings_and_farewells_correct = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'greetings and farewells' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        greetings_and_farewells_incorrect = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'dates' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        dates_correct = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'dates' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        dates_incorrect = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'weather' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        weather_correct = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (correct_incorrect) FROM user_practice_records WHERE category_name = 'weather' AND correct_incorrect = 'incorrect' AND username = %s;", (session['username'],))
        weather_incorrect = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT (*) FROM user_practice_records WHERE username = %s;", (session['username'],))
        total_practice_records = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('study_list.html', username=session['username'],
                               title='My dictionary!', my_dictionary=my_dictionary, verbs_correct=verbs_correct, verbs_incorrect=verbs_incorrect,
                               numbers_correct=numbers_correct, numbers_incorrect=numbers_incorrect, places_correct=places_correct, times_correct=times_correct,
                               times_incorrect=times_incorrect, places_incorrect=places_incorrect, adjectives_correct=adjectives_correct, adjectives_incorrect=adjectives_incorrect,
                               foods_and_drinks_correct=foods_and_drinks_correct, foods_and_drinks_incorrect=foods_and_drinks_incorrect, total_practice_records=total_practice_records,
                               greetings_and_farewells_correct=greetings_and_farewells_correct, greetings_and_farewells_incorrect=greetings_and_farewells_incorrect,dates_correct=dates_correct,
                               dates_incorrect=dates_incorrect, weather_correct=weather_correct, weather_incorrect=weather_incorrect)

    return redirect(url_for('login'))

@application.route('/reset_study_list', methods=['POST'])
def reset_study_list():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("DELETE FROM user_practice_records WHERE username = %s;", (session['username'],))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('study_list'))

    return redirect(url_for('login'))

@application.route('/delete_practice_record/<string:id>', methods=['POST'])
def delete_practice_record(id):
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT spanish_word FROM user_practice_records WHERE id = {0};".format(id))

        spanish_word_record = cursor.fetchone()[0]

        cursor.execute("DELETE FROM user_practice_records WHERE id = {0};".format(id))

        conn.commit()

        cursor.close()
        conn.close()

        flash(f"Record deleted successfully for '{spanish_word_record}'.")

        return redirect(request.referrer)

    return redirect(url_for('sign_up'))

@application.route('/delete_dictionary_entry/<string:id>', methods=['POST'])
def delete_dictionary_entry(id):
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT spanish_word FROM dictionary_of_words WHERE id = {0};".format(id))

        spanish_word_entry = cursor.fetchone()[0]

        cursor.execute("DELETE FROM dictionary_of_words WHERE id = {0};".format(id))

        conn.commit()

        cursor.close()
        conn.close()

        flash(f"Entry deleted successfully for '{spanish_word_entry}'.")

        return redirect(request.referrer)

    return redirect(url_for('sign_up'))

@application.route('/flashcards')
def flashcards():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT english_word, spanish_word, date_added_on FROM dictionary_of_words WHERE username = %s;', (session['username'],))

        my_dictionary = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('flashcards.html', overall_score=overall_score, username=session['username'],
                               title='My flashcards!', my_dictionary=my_dictionary)

    return redirect(url_for('login'))

@application.route('/level_selector', methods=['GET'])
def level_selector():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()

        session['overall_score'] = overall_score[0]

        cursor.execute('SELECT account_creation_date FROM spanish_users WHERE username = %s;', [session['username']])

        account_creation_date = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template('level_selector.html', username=session['username'], overall_score=session['overall_score'], account_creation_date=account_creation_date)

    return redirect(url_for('login'))

@application.route('/delete_account', methods=['GET'])
def delete_account():
    if 'loggedin' in session:

        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()

        session['overall_score'] = overall_score[0]

        cursor.close()
        conn.close()

        return render_template('delete_account.html', username=session['username'], overall_score=session['overall_score'])

    return redirect(url_for('login'))

@application.route('/delete_account_submit', methods=['POST'])
def delete_account_submit():
    if 'loggedin' in session:
        try:
            username_delete = request.form.get('username_delete')

            client = boto3.client('cognito-idp', region_name="us-east-1")

            client.admin_delete_user(
            UserPoolId='us-east-1_0EguHE3d6',
            Username=username_delete
            )

            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cursor.execute("DELETE FROM spanish_users WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM flights WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM random_numbers WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM random_places WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM random_verbs WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM dictionary_of_words WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM user_practice_records WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM random_food_or_drink WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM random_adjectives WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM random_speaking WHERE username = %s;", (session['username'],))
            cursor.execute("DELETE FROM upload_recordings WHERE username = %s;", (session['username'],))

            conn.commit()

            cursor.close()
            conn.close()

            flash('You have successfully deleted your account!')

            return redirect(url_for('main_page'))
        except:
            flash('Username incorrect or user is not in the system.')
            return redirect(url_for('delete_account'))

@application.route('/forgot_password_page', methods=['GET'])
def forgot_password_page():
    return render_template('forgot_password_page.html')

@application.route('/request_password_reset', methods=['POST', 'GET'])
def request_password_reset():

    email_forgot_password = request.form.get('email_forgot_password')

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute('SELECT username FROM spanish_users WHERE username = %s;', (email_forgot_password,))

    username_confirmation = cursor.fetchone()

    conn.close()
    cursor.close()

    if username_confirmation:

        client = boto3.client("cognito-idp", region_name="us-east-1")
        # Initiating the Authentication,
        client.forgot_password(
            ClientId=COGNITO_USER_CLIENT_ID,
            Username=email_forgot_password
        )

        session['username'] = email_forgot_password
        return render_template('authenticate_new_password.html')
    else:
        flash('User is not in system!')
        return render_template('forgot_password_page.html')

@application.route('/confirm_forgot_password', methods=['POST', 'GET'])
def confirm_forgot_password():
        try:
            username_new_password = request.form.get('username_new_password')
            authentication_code_new_password = request.form.get('authentication_code_new_password')
            new_password = request.form.get('new_password')

            client = boto3.client("cognito-idp", region_name="us-east-1")

            client.confirm_forgot_password(
                ClientId=COGNITO_USER_CLIENT_ID,
                Username=username_new_password,
                ConfirmationCode=authentication_code_new_password,
                Password=new_password
            )
            flash(f'Password reset successfully for {username_new_password}.')
            return redirect(url_for('login'))

        except:
            flash('One or more fields are incorrect. Please try again.')
            return render_template('authenticate_new_password.html')

@application.route('/main_page')
def main_page():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('overall_score', None)
   # Redirect to login page
   return render_template('sign_up.html')

if __name__ == '__main__':
    application.run(debug=False, host='0.0.0.0', port=80)
