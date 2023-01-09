from flask import Blueprint, render_template
from flask import request, flash, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import boto3
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

# End environment variables #

spain_listening = Blueprint("spain_listening", __name__)

@spain_listening.route('/spain_listening_page', methods=['POST', 'GET'])
def spain_listening_page():
     if 'loggedin' in session:

         conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
         cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

         cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

         overall_score = cursor.fetchone()[0]

         cursor.close()
         conn.close()

         return render_template('spain_listening_page.html', overall_score=overall_score, username=session['username'])

     return redirect(url_for('sign_up'))

@spain_listening.route('/spain_listening_page_submit', methods=['POST', 'GET'])
def spain_listening_page_submit():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        spain_listening_page_1 = request.form.get("spain_listening_page_1")

        if spain_listening_page_1 == "Hello, how are you?":
            answer_1 = f'Correct, your answer was {spain_listening_page_1} and the correct answer is "Hello, how are you?."'

            updated_overall_score_5 = overall_score + 1

            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
            (updated_overall_score_5, session['username']))

            conn.commit()

        else:
            answer_1 = f'Incorrect, your answer was {spain_listening_page_1} and the correct answer is "Hello, how are you?."'

        spain_listening_page_2 = request.form.get("spain_listening_page_2")

        if spain_listening_page_2 == "¿Dónde vives?":
            answer_2 = f'Correct, your answer was {spain_listening_page_2} and the correct answer is "Where do you live?"'
            updated_overall_score_5 = overall_score + 1

            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
            (updated_overall_score_5, session['username']))

            conn.commit()

        else:
            answer_2 = f'Incorrect, your answer was {spain_listening_page_2} and the correct answer is "Where do you live?."'

        cursor.close()
        conn.close()

        print(answer_1)
        print(answer_2)

        return render_template('spain_listening_page.html', overall_score=overall_score, username=session['username'], answer_1=answer_1,
                               answer_2=answer_2
                               )

    return redirect(url_for('sign_up'))



