from flask import Blueprint, render_template,request, flash, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import datetime
import pytz
import boto3
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

flight_peru = Blueprint("flight_peru", __name__)

@flight_peru.route('/book_peru_flight_page')
def book_peru_flight_page():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template("book_peru_flight_page.html", overall_score=overall_score)

    return redirect(url_for('sign_up'))

@flight_peru.route('/select_dates_for_peru_trip', methods=['POST', 'GET'])
def select_dates_for_peru_trip():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        flight = "Lima, Perú"

        price = str(433)

        date = datetime.date.today()

        format_code = '%Y%m%d'

        date_today = date.strftime(format_code)

        date_today_int = int(date_today)

        departure_years = request.form.get("departure_years_peru")

        departure_months = request.form.get("departure_months_peru")

        departure_days = request.form.get("departure_days_peru")

        departure_date = departure_years + departure_months + departure_days

        departure_date_int = int(departure_date)

        departure_times = request.form.get("departure_times_peru")

        return_years = request.form.get("return_years_peru")

        return_months = request.form.get("return_months_peru")

        return_days = request.form.get("return_days_peru")

        return_date = return_years + return_months + return_days

        return_date_int = int(return_date)

        return_times = request.form.get("departure_times_peru")

        if departure_date_int > return_date_int:
            flash("Departure date must be after today's date!")
            return redirect(request.referrer)

        if departure_date_int == return_date_int:
            flash("Return date must be after today's date!")
            return redirect(request.referrer)

        if date_today_int > return_date_int:
            flash("Return date must be prior to today's date!")
            return redirect(request.referrer)

        cursor.execute("DELETE FROM flights WHERE flight = %s AND username = %s;", (session['username'], flight))

        conn.commit()

        cursor.execute(
            "INSERT INTO flights (flight, price, departure_date, departure_time, return_date, return_time, confirmed, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
            (flight, price, departure_date, departure_times, return_date, return_times, None, session['username']))

        conn.commit()

        cursor.close()
        conn.close()

        slash = "/"

        departure_date = departure_years + slash + departure_months + slash + departure_days

        return_date = return_years + slash + return_months + slash + return_days

        return render_template("peru_flight_pre_confirmation.html", overall_score=overall_score, departure_date=departure_date,
                               departure_times=departure_times, return_date=return_date, return_times=
                               return_times)

    return redirect(url_for('sign_up'))

@flight_peru.route('/confirm_dates_for_peru_trip', methods=['POST', 'GET'])
def confirm_dates_for_peru_trip():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT departure_date FROM flights WHERE username = %s AND flight = %s;', (session['username'], 'Lima, Perú'))

        departure_date = cursor.fetchone()[0]

        print(departure_date)

        cursor.execute('SELECT departure_time FROM flights WHERE username = %s AND flight = %s;', (session['username'], 'Lima, Perú'))

        departure_time = cursor.fetchone()[0]

        cursor.execute('SELECT return_date FROM flights WHERE username = %s AND flight = %s;', (session['username'], 'Lima, Perú'))

        return_date = cursor.fetchone()[0]

        cursor.execute('SELECT return_time FROM flights WHERE username = %s AND flight = %s;', (session['username'], 'Lima, Perú'))

        return_time = cursor.fetchone()[0]

        date = datetime.date.today()

        format_code = '%Y/%m/%d'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "Lima, Perú",
                       "True"))

        flight_exists = cursor.fetchone()

        if not flight_exists:

            cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

            overall_score = cursor.fetchone()[0]

            cursor.execute(
                "UPDATE flights SET confirmed = %s, date_confirmed = %s, time_confirmed = %s WHERE username = %s AND flight = %s;",
                ('True', date_today, current_time, session['username'], "Lima, Perú"))

            new_overall_score = overall_score - 433

            cursor.execute(
                "UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                (new_overall_score, session['username']))

            cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

            updated_overall_score = cursor.fetchone()[0]

            conn.commit()

        else:
            flash('You have already booked this flight.')
            return redirect(url_for('flight_peru.select_dates_for_peru_trip'))

        return render_template("peru_trip_confirmation_page.html", departure_date=departure_date, departure_time=departure_time,
                               return_date=return_date, return_time=return_time, updated_overall_score=updated_overall_score), {"Refresh": "2; url= book_a_flight"}

    return redirect(url_for('sign_up'))
