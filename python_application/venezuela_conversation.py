from flask import Blueprint, render_template, request, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import boto3
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

BOT_ID = os.getenv("BOT_ID")
BOT_ALIAS = os.getenv("BOT_ALIAS")

# End environment variables #

venezuela_conversation = Blueprint("venezuela_conversation", __name__)

@venezuela_conversation.route('/venezuela_conversation_page', methods=['GET'])
def venezuela_conversation_page():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('DELETE FROM lex_convo WHERE username = %s;', [session['username']])

        conn.commit()

        cursor.close()
        conn.close()

        return render_template("venezuela_conversation_page.html", overall_score=overall_score)

    return redirect(url_for('sign_up'))

@venezuela_conversation.route('/venezuela_websocket', methods=['GET'])
def venezuela_websocket():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('DELETE FROM lex_convo WHERE username = %s;', [session['username']])

        conn.commit()

        cursor.close()
        conn.close()

        return render_template("venezuela_conversation_page.html", overall_score=overall_score)

    return redirect(url_for('sign_up'))

@venezuela_conversation.route('/venezuela_chatbot', methods=['POST'])
def venezuela_chatbot():
    if 'loggedin' in session:
        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            sent_message = request.form.get('venezuela_conversation')

            translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

            result = translate.translate_text(Text=sent_message,
                                          SourceLanguageCode="es", TargetLanguageCode="en")

            answer_translation = (result.get('TranslatedText'))

            cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

            overall_score = cursor.fetchone()[0]

            date = datetime.date.today()

            format_code = '%m-%d-%y'

            date_today = date.strftime(format_code)

            timezone = pytz.timezone('US/Eastern')
            now = datetime.datetime.now(tz=timezone)
            current_time = now.strftime("%I:%M %p")

            cursor.execute("SELECT * FROM dictionary_of_words WHERE username = %s AND spanish_word = %s;", (session['username'], sent_message))
            spanish_word_dictionary_check = cursor.fetchone()

            if sent_message.startswith("¿") and sent_message.endswith("?") and not spanish_word_dictionary_check:
                cursor.execute("INSERT INTO dictionary_of_words (english_word, spanish_word, username, date_added_on, time_added_on, category) VALUES (%s,%s,%s,%s,%s,%s);", (answer_translation, sent_message, session['username'], date_today, current_time, 'questions'))
                updated_overall_score_5 = overall_score + 2

                cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))

                conn.commit()

            client = boto3.client('lexv2-runtime')

            response = client.recognize_text(
            botId=BOT_ID,
            botAliasId=BOT_ALIAS,
            localeId='es_419',
            sessionId='test_session',
            text=sent_message)

            bot_response = response["messages"][0]['content']

            timezone = pytz.timezone('US/Eastern')
            now = datetime.datetime.now(tz=timezone)

            current_time = now.strftime("%I:%M %p")

            cursor.execute("INSERT INTO lex_convo (username, time_sent, sent_message, received_message) VALUES (%s,%s,%s,%s);", (session['username'], current_time,
                                                                                                                                 sent_message, bot_response))
            conn.commit()

            cursor.execute('SELECT * FROM lex_convo WHERE username = %s;', [session['username']])

            lex_conversation = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template("venezuela_conversation_page.html", lex_conversation=lex_conversation, overall_score=overall_score)

        except:
            sent_message = request.form.get('venezuela_conversation')

            timezone = pytz.timezone('US/Eastern')
            now = datetime.datetime.now(tz=timezone)
            current_time = now.strftime("%I:%M %p")

            cursor.execute("INSERT INTO lex_convo (username, time_sent, sent_message, received_message) VALUES (%s,%s,%s,%s);", (session['username'], current_time,
                                                                                                                                 sent_message, "Lo siento, no entiendo."))
            conn.commit()

            cursor.execute('SELECT * FROM lex_convo WHERE username = %s;', [session['username']])

            lex_conversation = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template("venezuela_conversation_page.html", lex_conversation=lex_conversation,overall_score=overall_score)

    return redirect(url_for('sign_up'))
