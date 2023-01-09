from flask import Blueprint, render_template, flash, request, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import urllib
import urllib.request
import random
import boto3
import datetime
import urllib.request
from werkzeug.utils import secure_filename
import time
import json
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

s3 = boto3.client('s3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                     )
load_dotenv(find_dotenv())

BUCKET_NAME = os.getenv("BUCKET_NAME")

peru_speaking = Blueprint("peru_speaking", __name__)

@peru_speaking.route('/peru_speaking_page', methods=['POST', 'GET'])
def peru_speaking_page():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_speaking WHERE username =%s;", [session['username']])
        conn.commit()

        word_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_places.txt"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_sentence = random.choice(words)

        cursor.execute("INSERT INTO random_speaking (recording, username) VALUES (%s, %s);", (random_sentence, session['username']))

        conn.commit()

        cursor.close()
        conn.close()

        return render_template('peru_speaking_page.html', overall_score=overall_score, username=session['username'],
                               random_sentence=random_sentence)

    return redirect(url_for('sign_up'))

@peru_speaking.route('/peru_speaking_page_numbers_1_to_100', methods=['POST', 'GET'])
def peru_speaking_page_numbers_1_to_100():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_speaking WHERE username =%s;", [session['username']])
        conn.commit()

        word_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/numbers_0_to_100"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_sentence = random.choice(words)

        cursor.execute("INSERT INTO random_speaking (recording, username) VALUES (%s, %s);", (random_sentence, session['username']))

        conn.commit()

        conn.close()
        cursor.close()

        return render_template('peru_speaking_page.html', overall_score=overall_score, username=session['username'],
                               random_sentence=random_sentence)

    return redirect(url_for('sign_up'))

@peru_speaking.route('/peru_speaking_page_colors', methods=['POST', 'GET'])
def peru_speaking_page_colors():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_speaking WHERE username =%s;", [session['username']])
        conn.commit()

        word_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_colors.txt"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_sentence = random.choice(words)

        cursor.execute("INSERT INTO random_speaking (recording, username) VALUES (%s, %s);", (random_sentence, session['username']))

        conn.commit()

        conn.close()
        cursor.close()

        return render_template('peru_speaking_page.html', overall_score=overall_score, username=session['username'],
                               random_sentence=random_sentence)

    return redirect(url_for('sign_up'))

@peru_speaking.route('/peru_speaking_page_greetings_and_farewells', methods=['POST', 'GET'])
def peru_speaking_page_greetings_and_farewells():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_speaking WHERE username =%s;", [session['username']])
        conn.commit()

        word_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_greetings_and_farewells.txt"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_sentence = random.choice(words)

        cursor.execute("INSERT INTO random_speaking (recording, username) VALUES (%s, %s);", (random_sentence, session['username']))

        conn.commit()

        return render_template('peru_speaking_page.html', overall_score=overall_score, username=session['username'],
                               random_sentence=random_sentence)

    return redirect(url_for('sign_up'))

@peru_speaking.route('/peru_speaking_page_dates', methods=['POST', 'GET'])
def peru_speaking_page_dates():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("DELETE FROM random_speaking WHERE username =%s;", [session['username']])
        conn.commit()

        word_url = "https://raw.githubusercontent.com/ViggoMode2021/Spanish_game_website_resources/main/english_dates"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        random_sentence = random.choice(words)

        cursor.execute("INSERT INTO random_speaking (recording, username) VALUES (%s, %s);", (random_sentence, session['username']))

        conn.commit()

        return render_template('peru_speaking_page.html', overall_score=overall_score, username=session['username'],
                               random_sentence=random_sentence)

    return redirect(url_for('sign_up'))

@peru_speaking.route('/upload', methods=['POST', 'GET'])
def upload():
    if 'loggedin' in session:
        if request.method == 'POST':
            img = request.files['file']
            if img:
                try:
                    date = datetime.date.today()

                    format_code = '%m-%d-%Y'

                    date_object = date.strftime(format_code)

                    email = [session['username']]
                    email_save = "  email  " + str(email)
                    global filename
                    filename = secure_filename(img.filename + email_save)
                    img.save(filename)
                    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

                    global cursor
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                    cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

                    global overall_score
                    overall_score = cursor.fetchone()[0]

                    cursor.execute("INSERT INTO upload_recordings (recording_name, date_upload, username) VALUES (%s, %s, %s);", (filename, date_object, session['username']))
                    conn.commit()

                    cursor.execute("SELECT recording FROM random_speaking WHERE username = %s;", [session['username']])
                    random_sentence = cursor.fetchone()[0]
                    print(random_sentence)

                    cursor.execute("SELECT recording FROM random_speaking WHERE username = %s;", [session['username']])
                    random_sentence = cursor.fetchone()[0]

                    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

                    global translated_sentence
                    translated_sentence = translate.translate_text(Text=random_sentence,
                                              SourceLanguageCode="en", TargetLanguageCode="es")

                    translated_sentence_copy = (translated_sentence.get('TranslatedText'))

                    s3.upload_file(
                        Bucket=BUCKET_NAME,
                        Filename=filename,
                        Key=filename
                    )
                    client = boto3.client('transcribe', region_name="us-east-1")
                    client.start_transcription_job(
                TranscriptionJobName=filename,
                LanguageCode='es-ES',
                MediaFormat='mp3',
                Media={
                    'MediaFileUri': f's3://spanishapprekognition/{filename}'
                }
            )
                except:
                    cursor.close()
                    conn.close()
                    flash('File upload format incorrect.')
                    return redirect(url_for("peru_speaking.peru_speaking_page", username=session['username']))
            max_tries = 60
            while max_tries > 0:
                max_tries -= 1
                client = boto3.client('transcribe', region_name="us-east-1")
                job = client.get_transcription_job(TranscriptionJobName=filename)
                job_status = job['TranscriptionJob']['TranscriptionJobStatus']
                print(job_status)
                if job_status in ['COMPLETED', 'FAILED']:
                    if job_status == 'COMPLETED':
                        response = urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                        data = json.loads(response.read())
                        print(data)
                        text = data['results']['transcripts'][0]['transcript']
                        user_result = text.replace(".","")
                        if user_result.lower() == translated_sentence_copy:
                            s3.delete_objects(
                            Bucket=BUCKET_NAME,
                            Delete={
                                'Objects': [
                                    {
                                        'Key': filename
                                    }
                                ]
                            }
                            )
                            updated_overall_score_5 = overall_score + 3

                            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                            (updated_overall_score_5, session['username']))

                            cursor.execute("DELETE FROM upload_recordings WHERE username = %s;", (session['username'],))
                            conn.commit()

                            client.delete_transcription_job(
                                TranscriptionJobName=filename
                            )
                            flash("Correct, you just received 3 points!")
                        else:
                            os.remove(filename)
                            flash("Incorrect, please try again!")

                            client.delete_transcription_job(
                                TranscriptionJobName=filename
                            )
                    break
                else:
                    time.sleep(10)
            else:
                os.remove(filename)
                cursor.close()
                conn.close()
                flash('No file has been selected to upload. Please click "Choose File button".')
                return redirect(url_for("peru_speaking.peru_speaking_page", username=session['username']))
        cursor.close()
        conn.close()
        return render_template("peru_speaking_page.html", username=session['username'], user_result=user_result,
                               translated_sentence_copy=translated_sentence_copy,
                               overall_score=overall_score, random_sentence=random_sentence)

    return redirect(url_for('sign_up'))
