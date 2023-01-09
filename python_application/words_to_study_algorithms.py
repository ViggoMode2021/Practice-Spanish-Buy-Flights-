from flask import render_template, session, redirect, url_for, Blueprint
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv, find_dotenv
import boto3

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

words_to_study_algorithms = Blueprint("words_to_study_algorithms", __name__)

@words_to_study_algorithms.route('/words_to_study_algorithms_adjectives')
def words_to_study_algorithms_adjectives():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        category_name = 'adjectives'

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'correct', "adjectives"))

        user_practice_records_correct = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'incorrect', "adjectives"))

        user_practice_records_incorrect = cursor.fetchone()[0]

        if user_practice_records_correct < user_practice_records_incorrect:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that you should study more. You got this!'
        elif user_practice_records_correct == 0 and user_practice_records_incorrect == 0:
            study_suggestion = f'You do not have any correct or incorrect attempts for the category: {category_name}.'
        else:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that your grasp of this concept is quite strong. Keep on keeping on!'

        cursor.execute('SELECT * FROM user_practice_records WHERE username = %s AND category_name = %s;', (session['username'], "adjectives"))

        user_practice_records_by_category = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_practice_records_by_category.html', username=session['username'],
                               title='My flights!', user_practice_records_by_category=user_practice_records_by_category,
                               category_name=category_name,user_practice_records_correct=user_practice_records_correct,
                               user_practice_records_incorrect=user_practice_records_incorrect, study_suggestion=study_suggestion)

    return redirect(url_for('sign_up'))

@words_to_study_algorithms.route('/words_to_study_algorithms_places')
def words_to_study_algorithms_places():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        category_name = 'places'

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'correct', "places"))

        user_practice_records_correct = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'incorrect', "places"))

        user_practice_records_incorrect = cursor.fetchone()[0]

        if user_practice_records_correct < user_practice_records_incorrect:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that you should study more. You got this!'
        elif user_practice_records_correct == 0 and user_practice_records_incorrect == 0:
            study_suggestion = f'You do not have any correct or incorrect attempts for the category: {category_name}.'
        else:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that your grasp of this concept is quite strong. Keep on keeping on!'

        cursor.execute('SELECT * FROM user_practice_records WHERE username = %s AND category_name = %s;', (session['username'], "places"))

        user_practice_records_by_category = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_practice_records_by_category.html', username=session['username'],
                               title='My flights!', user_practice_records_by_category=user_practice_records_by_category,
                               category_name=category_name, user_practice_records_correct=user_practice_records_correct,
                               user_practice_records_incorrect=user_practice_records_incorrect, study_suggestion=study_suggestion)

    return redirect(url_for('sign_up'))

@words_to_study_algorithms.route('/words_to_study_algorithms_times')
def words_to_study_algorithms_times():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        category_name = 'times'

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'correct', "times"))

        user_practice_records_correct = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'incorrect', "times"))

        user_practice_records_incorrect = cursor.fetchone()[0]

        if user_practice_records_correct < user_practice_records_incorrect:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that you should study more. You got this!'
        elif user_practice_records_correct == 0 and user_practice_records_incorrect == 0:
            study_suggestion = f'You do not have any correct or incorrect attempts for the category: {category_name}.'
        else:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that your grasp of this concept is quite strong. Keep on keeping on!'

        cursor.execute('SELECT * FROM user_practice_records WHERE username = %s AND category_name = %s;', (session['username'], "times"))

        user_practice_records_by_category = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_practice_records_by_category.html', username=session['username'],
                               title='My flights!', user_practice_records_by_category=user_practice_records_by_category,
                               category_name=category_name, user_practice_records_correct=user_practice_records_correct,
                               user_practice_records_incorrect=user_practice_records_incorrect, study_suggestion=study_suggestion)

    return redirect(url_for('sign_up'))

@words_to_study_algorithms.route('/words_to_study_algorithms_numbers')
def words_to_study_algorithms_numbers():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        category_name = 'numbers'

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'correct', "numbers"))

        user_practice_records_correct = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'incorrect', "numbers"))

        user_practice_records_incorrect = cursor.fetchone()[0]

        if user_practice_records_correct < user_practice_records_incorrect:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that you should study more. You got this!'
        elif user_practice_records_correct == 0 and user_practice_records_incorrect == 0:
            study_suggestion = f'You do not have any correct or incorrect attempts for the category: {category_name}.'
        else:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that your grasp of this concept is quite strong. Keep on keeping on!'

        cursor.execute('SELECT * FROM user_practice_records WHERE username = %s AND category_name = %s;', (session['username'], "numbers"))

        user_practice_records_by_category = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_practice_records_by_category.html', username=session['username'],
                               title='My flights!', user_practice_records_by_category=user_practice_records_by_category,
                               category_name=category_name,user_practice_records_correct=user_practice_records_correct,
                               user_practice_records_incorrect=user_practice_records_incorrect, study_suggestion=study_suggestion)

    return redirect(url_for('sign_up'))

@words_to_study_algorithms.route('/words_to_study_algorithms_foods_and_drinks')
def words_to_study_algorithms_foods_and_drinks():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        category_name = 'foods and drinks'

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'correct', "foods and drinks"))

        user_practice_records_correct = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'incorrect', "foods and drinks"))

        user_practice_records_incorrect = cursor.fetchone()[0]

        if user_practice_records_correct < user_practice_records_incorrect:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that you should study more. You got this!'
        elif user_practice_records_correct == 0 and user_practice_records_incorrect == 0:
            study_suggestion = f'You do not have any correct or incorrect attempts for the category: {category_name}.'
        else:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that your grasp of this concept is quite strong. Keep on keeping on!'

        cursor.execute('SELECT * FROM user_practice_records WHERE username = %s AND category_name = %s;', (session['username'], "foods and drinks"))

        user_practice_records_by_category = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_practice_records_by_category.html', username=session['username'],
                               title='My flights!', user_practice_records_by_category=user_practice_records_by_category,
                               category_name=category_name,user_practice_records_correct=user_practice_records_correct,
                               user_practice_records_incorrect=user_practice_records_incorrect, study_suggestion=study_suggestion)

    return redirect(url_for('sign_up'))

@words_to_study_algorithms.route('/words_to_study_algorithms_greetings_and_farewells')
def words_to_study_algorithms_greetings_and_farewells():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        category_name = 'greetings and farewells'

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'correct', "greetings and farewells"))

        user_practice_records_correct = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'incorrect', "greetings and farewells"))

        user_practice_records_incorrect = cursor.fetchone()[0]

        if user_practice_records_correct < user_practice_records_incorrect:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that you should study more. You got this!'
        elif user_practice_records_correct == 0 and user_practice_records_incorrect == 0:
            study_suggestion = f'You do not have any correct or incorrect attempts for the category: {category_name}.'
        else:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that your grasp of this concept is quite strong. Keep on keeping on!'

        cursor.execute('SELECT * FROM user_practice_records WHERE username = %s AND category_name = %s;', (session['username'], "greetings and farewells"))

        user_practice_records_by_category = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_practice_records_by_category.html', username=session['username'],
                               title='My flights!', user_practice_records_by_category=user_practice_records_by_category,
                               category_name=category_name, user_practice_records_correct=user_practice_records_correct,
                               user_practice_records_incorrect=user_practice_records_incorrect, study_suggestion=study_suggestion)

    return redirect(url_for('sign_up'))

@words_to_study_algorithms.route('/words_to_study_algorithms_dates')
def words_to_study_algorithms_dates():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        category_name = 'dates'

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'correct', "dates"))

        user_practice_records_correct = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'incorrect', "dates"))

        user_practice_records_incorrect = cursor.fetchone()[0]

        if user_practice_records_correct < user_practice_records_incorrect:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that you should study more. You got this!'
        elif user_practice_records_correct == 0 and user_practice_records_incorrect == 0:
            study_suggestion = f'You do not have any correct or incorrect attempts for the category: {category_name}.'
        else:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that your grasp of this concept is quite strong. Keep on keeping on!'

        cursor.execute('SELECT * FROM user_practice_records WHERE username = %s AND category_name = %s;', (session['username'], "dates"))

        user_practice_records_by_category = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_practice_records_by_category.html', username=session['username'],
                               title='My flights!', user_practice_records_by_category=user_practice_records_by_category,
                               category_name=category_name, user_practice_records_correct=user_practice_records_correct,
                               user_practice_records_incorrect=user_practice_records_incorrect, study_suggestion=study_suggestion)

    return redirect(url_for('sign_up'))

@words_to_study_algorithms.route('/words_to_study_algorithms_weather')
def words_to_study_algorithms_weather():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        category_name = 'weather'

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'correct', "weather"))

        user_practice_records_correct = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'incorrect', "weather"))

        user_practice_records_incorrect = cursor.fetchone()[0]

        if user_practice_records_correct < user_practice_records_incorrect:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that you should study more. You got this!'
        elif user_practice_records_correct == 0 and user_practice_records_incorrect == 0:
            study_suggestion = f'You do not have any correct or incorrect attempts for the category: {category_name}.'
        else:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that your grasp of this concept is quite strong. Keep on keeping on!'

        cursor.execute('SELECT * FROM user_practice_records WHERE username = %s AND category_name = %s;', (session['username'], "weather"))

        user_practice_records_by_category = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_practice_records_by_category.html', username=session['username'],
                               title='My flights!', user_practice_records_by_category=user_practice_records_by_category,
                               category_name=category_name, user_practice_records_correct=user_practice_records_correct,
                               user_practice_records_incorrect=user_practice_records_incorrect, study_suggestion=study_suggestion)

    return redirect(url_for('sign_up'))

@words_to_study_algorithms.route('/words_to_study_algorithms_questions')
def words_to_study_algorithms_questions():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        category_name = 'weather'

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'correct', "questions"))

        user_practice_records_correct = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT (*) FROM user_practice_records WHERE username = %s AND correct_incorrect = %s AND category_name = %s;', (session['username'], 'incorrect', "questions"))

        user_practice_records_incorrect = cursor.fetchone()[0]

        if user_practice_records_correct < user_practice_records_incorrect:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that you should study more. You got this!'
        elif user_practice_records_correct == 0 and user_practice_records_incorrect == 0:
            study_suggestion = f'You do not have any correct or incorrect attempts for the category: {category_name}.'
        else:
            study_suggestion = f'The ratio of correct {category_name} to incorrect {category_name} indicates that your grasp of this concept is quite strong. Keep on keeping on!'

        cursor.execute('SELECT * FROM user_practice_records WHERE username = %s AND category_name = %s;', (session['username'], "questions"))

        user_practice_records_by_category = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_practice_records_by_category.html', username=session['username'],
                               title='My flights!', user_practice_records_by_category=user_practice_records_by_category,
                               category_name=category_name, user_practice_records_correct=user_practice_records_correct,
                               user_practice_records_incorrect=user_practice_records_incorrect,study_suggestion=study_suggestion)

    return redirect(url_for('sign_up'))


