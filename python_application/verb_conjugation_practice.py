from flask import Blueprint, render_template, request, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import random
import boto3
import ast
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

verb_conjugation_practice = Blueprint("verb_conjugation_practice", __name__)

@verb_conjugation_practice.route('/verb_conjugation_practice_page')
def verb_conjugation_practice_page():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template("verb_conjugation_practice_page.html", overall_score=overall_score)

    return redirect(url_for('sign_up'))

@verb_conjugation_practice.route('/verb_conjugation_practice_present_tense', methods=['GET'])
def verb_conjugation_practice_present_tense():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        file = open("present_tense_dictionary.txt", "r")

        contents = file.read()
        present_tense_dictionary = ast.literal_eval(contents)

        file.close()

        global random_present_tense_infinitive

        random_present_tense_infinitive = random.choice(list(present_tense_dictionary.items()))

        infinitive_verb_with_subject_pronoun = random_present_tense_infinitive[0].replace("tÃº", "tú")

        global conjugated_verb_answer
        conjugated_verb_answer = random_present_tense_infinitive[1].replace("tÃº", "tú")

        cursor.close()
        conn.close()

        return render_template("verb_conjugation_practice_present_tense_page.html", overall_score=overall_score, random_present_tense_infinitive=random_present_tense_infinitive,
                               infinitive_verb_with_subject_pronoun=infinitive_verb_with_subject_pronoun, conjugated_verb_answer=conjugated_verb_answer)

    return redirect(url_for('sign_up'))

@verb_conjugation_practice.route('/verb_conjugation_practice_present_tense_submit', methods=['POST'])
def verb_conjugation_practice_present_tense_submit():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        verb_conjugation_practice_present_tense_submit = request.form.get('verb_conjugation_practice_present_tense_submit')

        translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result = translate.translate_text(Text=verb_conjugation_practice_present_tense_submit,
                                          SourceLanguageCode="es", TargetLanguageCode="en")

        answer_translation = (result.get('TranslatedText')).replace("do", "")

        single_quote = "'"

        global conjugated_verb_answer

        if verb_conjugation_practice_present_tense_submit == conjugated_verb_answer:
            printed_answer_conjugated_verb = f"Correct! Your answer was '{verb_conjugation_practice_present_tense_submit}' and the correct answer was '{conjugated_verb_answer}'!"
            updated_overall_score_5 = overall_score + 1

            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))
        else:
            printed_answer_conjugated_verb = f"Incorrect, your answer was '{verb_conjugation_practice_present_tense_submit}' and the correct answer was '{conjugated_verb_answer}'!"

        It_means = "It means"
        conn.commit()
        cursor.close()
        conn.close()

        return render_template("verb_conjugation_practice_present_tense_page.html", overall_score=overall_score,
                               printed_answer_conjugated_verb=printed_answer_conjugated_verb, answer_translation=answer_translation,
                               It_means=It_means,single_quote=single_quote)

    return redirect(url_for('sign_up'))

@verb_conjugation_practice.route('/verb_conjugation_practice_present_tense_irregular', methods=['GET'])
def verb_conjugation_practice_present_tense_irregular():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        file_2 = open("present_tense_irregular_dictionary.txt", "r")

        contents_2 = file_2.read()
        present_tense_irregular_dictionary = ast.literal_eval(contents_2)

        file_2.close()

        global random_present_tense_irregular_infinitive

        random_present_tense_irregular_infinitive = random.choice(list(present_tense_irregular_dictionary.items()))

        infinitive_irregular_verb_with_subject_pronoun = random_present_tense_irregular_infinitive[0].replace("tÃº", "tú")

        global conjugated_verb_answer_irregular
        conjugated_verb_answer_irregular = random_present_tense_irregular_infinitive[1].replace("tÃº", "tú")

        cursor.close()
        conn.close()

        return render_template("verb_conjugation_irregular_practice_present_tense_page.html", overall_score=overall_score, random_present_tense_irregular_infinitive=random_present_tense_irregular_infinitive,
                               infinitive_irregular_verb_with_subject_pronoun=infinitive_irregular_verb_with_subject_pronoun, conjugated_verb_answer_irregular=conjugated_verb_answer_irregular)

    return redirect(url_for('sign_up'))

@verb_conjugation_practice.route('/verb_conjugation_practice_present_tense_irregular_submit', methods=['POST'])
def verb_conjugation_practice_present_tense_irregular_submit():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        verb_conjugation_practice_irregular_present_tense_submit = request.form.get('verb_conjugation_practice_irregular_present_tense_submit')

        translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

        result = translate.translate_text(Text=verb_conjugation_practice_irregular_present_tense_submit,
                                          SourceLanguageCode="es", TargetLanguageCode="en")

        answer_translation = (result.get('TranslatedText')).replace("do", "")

        single_quote = "'"

        global conjugated_verb_answer_irregular

        if verb_conjugation_practice_irregular_present_tense_submit == conjugated_verb_answer_irregular:
            printed_answer_conjugated_verb = f"Correct! Your answer was '{verb_conjugation_practice_irregular_present_tense_submit}' and the correct answer was '{conjugated_verb_answer_irregular}'!"
            updated_overall_score_5 = overall_score + 1

            cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                           (updated_overall_score_5, session['username']))
        else:
            printed_answer_conjugated_verb = f"Incorrect, your answer was '{verb_conjugation_practice_irregular_present_tense_submit}' and the correct answer was '{conjugated_verb_answer_irregular}'!"

        It_means = "It means"
        conn.commit()
        cursor.close()
        conn.close()

        return render_template("verb_conjugation_irregular_practice_present_tense_page.html", overall_score=overall_score,
                               printed_answer_conjugated_verb=printed_answer_conjugated_verb, answer_translation=answer_translation,
                               It_means=It_means, single_quote=single_quote)

    return redirect(url_for('sign_up'))




