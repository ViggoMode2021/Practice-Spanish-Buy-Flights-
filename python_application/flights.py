from flask import Blueprint, render_template, request, flash, session, redirect, url_for
import psycopg2
import psycopg2.extras
import os
import datetime
import pytz
import boto3
from dotenv import load_dotenv, find_dotenv
import requests

# Start environment variables #

load_dotenv(find_dotenv())

dotenv_path = os.path.join(os.path.dirname(__file__), ".env-practice-spanish-buy-flights")
load_dotenv(dotenv_path)

DB_NAME = os.getenv("DB_NAME")

CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

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

API_KEY = os.getenv("API_KEY")

# End environment variables #

flights = Blueprint("flights", __name__)

@flights.route('/book_a_flight')
def book_a_flight():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "San Juan, Puerto Rico",
                       "True"))

        puerto_rico_flight_exists = cursor.fetchone()

        puerto_rico_flight_confirmed = ""

        if puerto_rico_flight_exists:
            puerto_rico_flight_confirmed = "Purchased!"

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "Medellín, Colombia",
                       "True"))

        colombia_flight_exists = cursor.fetchone()

        colombia_flight_confirmed = ""

        if colombia_flight_exists:
            colombia_flight_confirmed = "Purchased!"

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "Lima, Perú",
                       "True"))

        peru_flight_exists = cursor.fetchone()

        peru_flight_confirmed = ""

        if peru_flight_exists:
            peru_flight_confirmed = "Purchased!"

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "Madrid, España",
                       "True"))

        spain_flight_exists = cursor.fetchone()

        spain_flight_confirmed = ""

        if spain_flight_exists:
            spain_flight_confirmed = "Purchased!"

        # Weather forecasts below:

        cursor.close()
        conn.close()

        return render_template('book_a_flight.html', overall_score=overall_score, username=session['username'],
                               title='Book a flight!', puerto_rico_flight_confirmed=puerto_rico_flight_confirmed,
                               colombia_flight_confirmed=colombia_flight_confirmed, peru_flight_confirmed=peru_flight_confirmed,
                               spain_flight_confirmed=spain_flight_confirmed)

    return redirect(url_for('sign_up'))

@flights.route('/my_flights')
def my_flights():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT * FROM flights WHERE username = %s AND confirmed = %s;', (session['username'], "True"))

        my_flights = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('my_flights.html', overall_score=overall_score, username=session['username'],
                               title='My flights!', my_flights=my_flights)

    return redirect(url_for('sign_up'))

@flights.route('/edit_flight/<string:id>', methods=['GET'])
def edit_flight(id):
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT id FROM flights WHERE id = {0};'.format(id))
        flight_id = cursor.fetchone()[0]

        session['flight_id'] = flight_id

        cursor.execute('SELECT flight FROM flights WHERE id = {0};'.format(id))
        flight = cursor.fetchone()[0]

        cursor.execute('SELECT departure_date FROM flights WHERE id = {0};'.format(id))
        departure_date = cursor.fetchone()[0]

        cursor.execute('SELECT departure_time FROM flights WHERE id = {0};'.format(id))
        departure_time = cursor.fetchone()[0]

        cursor.execute('SELECT return_date FROM flights WHERE id = {0};'.format(id))
        return_date = cursor.fetchone()[0]

        cursor.execute('SELECT return_time FROM flights WHERE id = {0};'.format(id))
        return_time = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template("edit_flight.html", departure_date=departure_date, departure_time=departure_time,
                               return_date=return_date, return_time=return_time, flight=flight, flight_id=flight_id)

    return redirect(url_for('login'))

@flights.route('/cancel_flight', methods=['POST'])
def cancel_flight():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT departure_date FROM flights WHERE id = %s AND username = %s;", (session['flight_id'], session['username']))
        departure_date = cursor.fetchone()

        cursor.execute("SELECT departure_time FROM flights WHERE id = %s AND username = %s;", (session['flight_id'], session['username']))
        departure_time = cursor.fetchone()

        cursor.execute("SELECT return_date FROM flights WHERE id = %s AND username = %s;", (session['flight_id'], session['username']))
        return_date = cursor.fetchone()

        cursor.execute("SELECT return_time FROM flights WHERE id = %s AND username = %s;", (session['flight_id'], session['username']))
        return_time = cursor.fetchone()

        cursor.execute("SELECT price FROM flights WHERE id = %s AND username = %s;", (session['flight_id'], session['username']))
        flight_price = cursor.fetchone()[0]

        cursor.execute("DELETE FROM flights WHERE id = %s AND username = %s;", (session['flight_id'], session['username']))

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute("UPDATE spanish_users SET overall_score = %s WHERE username = %s", (overall_score + flight_price, session['username']))

        conn.commit()

        cursor.close()
        conn.close()

        for date, time, return_d, return_t in zip(departure_date, departure_time, return_date, return_time):
            flash(f'Flight successfully canceled for your destination on {date} with a time of {time} and'
                  f' a return date of {return_d} at {return_t}.')

        return redirect(url_for('flights.my_flights'))

    return redirect(url_for('sign_up'))

@flights.route('/book_colombia_flight')
def book_colombia_flight():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "Medellín, Colombia",
                       "True"))

        flight_exists_colombia = cursor.fetchone()

        if flight_exists_colombia:
            flash("You have already booked this flight.")
            cursor.close()
            conn.close()
            return redirect(url_for('flights.book_a_flight'))

        if overall_score < 350:
            flash(f"The flight to Colombia costs 350 and you only have {overall_score}, sorry.")
            cursor.close()
            conn.close()
            return redirect(url_for('flights.book_a_flight'))
        else:
            cursor.close()
            conn.close()
            return redirect(url_for('flight_colombia.book_colombia_flight_page'))

    return redirect(url_for('sign_up'))

@flights.route('/puerto_rico_flight')
def puerto_rico_flight():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "San Juan, Puerto Rico",
                       "True"))

        flight_exists = cursor.fetchone()

        if flight_exists:
            flash("You have already booked this flight.")
            cursor.close()
            conn.close()
            return redirect(url_for('flights.book_a_flight'))

        if overall_score < 130:
            flash(f"The flight to Puerto Rico costs 130 and you only have {overall_score}, sorry.")
            cursor.close()
            conn.close()
            return redirect(url_for('flights.book_a_flight'))
        else:
            cursor.close()
            conn.close()
            return redirect(url_for('flights.book_puerto_rico_flight_page'))

    return redirect(url_for('sign_up'))

@flights.route('/book_puerto_rico_flight_page')
def book_puerto_rico_flight_page():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return render_template("book_puerto_rico_flight_page.html", overall_score=overall_score)

    return redirect(url_for('sign_up'))

@flights.route('/select_dates_for_puerto_rico_trip', methods=['POST', 'GET'])
def select_dates_for_puerto_rico_trip():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        flight = "San Juan, Puerto Rico"

        price = str(130)

        date = datetime.date.today()

        format_code = '%Y%m%d'

        date_today = date.strftime(format_code)

        date_today_int = int(date_today)

        departure_years = request.form.get("departure_years")

        departure_months = request.form.get("departure_months")

        departure_days = request.form.get("departure_days")

        departure_date = departure_years + departure_months + departure_days

        departure_date_int = int(departure_date)

        departure_times = request.form.get("departure_times")

        return_years = request.form.get("return_years")

        return_months = request.form.get("return_months")

        return_days = request.form.get("return_days")

        return_date = return_years + return_months + return_days

        return_date_int = int(return_date)

        return_times = request.form.get("departure_times")

        if departure_date_int > return_date_int:
            flash("Departure date must be after today's date!")
            return redirect(request.referrer)

        if departure_date_int == return_date_int:
            flash("Return date must be after today's date!")
            return redirect(request.referrer)

        if date_today_int > return_date_int:
            flash("Return date must be prior to today's date!")
            return redirect(request.referrer)

        cursor.execute("DELETE FROM flights WHERE username = %s AND flight = %s;", (session['username'], flight))

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

        return render_template("puerto_rico_flight_pre_confirmation.html", overall_score=overall_score, departure_date=departure_date,
                               departure_times=departure_times, return_date=return_date, return_times=
                               return_times)

    return redirect(url_for('sign_up'))

@flights.route('/confirm_dates_for_puerto_rico_trip', methods=['POST', 'GET'])
def confirm_dates_for_puerto_rico_trip():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT departure_date FROM flights WHERE username = %s AND flight = %s;', (session['username'], 'San Juan, Puerto Rico'))

        departure_date = cursor.fetchone()[0]

        cursor.execute('SELECT departure_time FROM flights WHERE username = %s AND flight = %s;', (session['username'], 'San Juan, Puerto Rico'))

        departure_time = cursor.fetchone()[0]

        cursor.execute('SELECT return_date FROM flights WHERE username = %s AND flight = %s;', (session['username'], 'San Juan, Puerto Rico'))

        return_date = cursor.fetchone()[0]

        cursor.execute('SELECT return_time FROM flights WHERE username = %s AND flight = %s;', (session['username'], 'San Juan, Puerto Rico'))

        return_time = cursor.fetchone()[0]

        date = datetime.date.today()

        format_code = '%Y/%m/%d'

        date_today = date.strftime(format_code)

        timezone = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(tz=timezone)
        current_time = now.strftime("%I:%M %p")

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "San Juan, Puerto Rico",
                       "True"))

        flight_exists = cursor.fetchone()

        if not flight_exists:

            cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

            overall_score = cursor.fetchone()[0]

            cursor.execute(
                "UPDATE flights SET confirmed = %s, date_confirmed = %s, time_confirmed = %s WHERE username = %s AND flight = %s;",
                ('True', date_today, current_time, session['username'], "San Juan, Puerto Rico"))

            new_overall_score = overall_score - 130

            cursor.execute(
                "UPDATE spanish_users SET overall_score = %s WHERE username = %s;",
                (new_overall_score, session['username']))

            cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

            updated_overall_score = cursor.fetchone()[0]

            conn.commit()

        else:
            flash('You have already booked this flight.')
            return redirect(url_for('flights.select_dates_for_puerto_rico_trip'))

        return render_template("puerto_rico_trip_confirmation_page.html", departure_date=departure_date, departure_time=departure_time,
                               return_date=return_date, return_time=return_time, updated_overall_score=updated_overall_score), {"Refresh": "2; url= book_a_flight"}

    return redirect(url_for('sign_up'))

@flights.route('/book_peru_flight')
def book_peru_flight():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "Lima, Perú",
                       "True"))

        flight_exists_peru = cursor.fetchone()

        if flight_exists_peru:
            flash("You have already booked this flight.")
            cursor.close()
            conn.close()
            return redirect(url_for('flights.book_a_flight'))

        if overall_score < 433:
            flash(f"The flight to Perú costs 433 and you only have {overall_score}, sorry.")
            cursor.close()
            conn.close()
            return redirect(url_for('flights.book_a_flight'))
        else:
            cursor.close()
            conn.close()
            return redirect(url_for('flight_peru.book_peru_flight_page'))

    return redirect(url_for('sign_up'))

@flights.route('/book_spain_flight')
def book_spain_flight():
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute('SELECT overall_score FROM spanish_users WHERE username = %s;', [session['username']])

        overall_score = cursor.fetchone()[0]

        cursor.execute('SELECT * FROM flights WHERE username = %s AND flight = %s AND confirmed = %s;', (session['username'], "Madrid, España",
                       "True"))

        flight_exists_spain = cursor.fetchone()

        if flight_exists_spain:
            flash("You have already booked this flight.")
            cursor.close()
            conn.close()
            return redirect(url_for('flights.book_a_flight'))

        if overall_score < 546:
            flash(f"The flight to España costs 433 and you only have {overall_score}, sorry.")
            cursor.close()
            conn.close()
            return redirect(url_for('flights.book_a_flight'))
        else:
            cursor.close()
            conn.close()
            return redirect(url_for('flight_spain.book_spain_flight_page'))

    return redirect(url_for('sign_up'))

@flights.route('/peru_currency_converter')
def peru_currency_converter():
    if 'loggedin' in session:

         baseurl = 'https://api.getgeoapi.com/v2/currency/convert?api_key='

         from_currency = '&from=USD&'

         to_currency = 'to=PEN'

         amount = '&amount=1'

         json = '&format=json'

         base_currency_converter = baseurl + 'f1ca5e8f4bc4c6f729bbb2de20deb702c41f14d9' + from_currency + to_currency + amount + json

         api = requests.get(base_currency_converter)

         currency = api.json()

         currency_name_rate = currency['amount']

         currency_name_rate_2 = currency['rates']['PEN']['rate_for_amount']

         return render_template('peru_currency.html', base_currency_converter=base_currency_converter, currency_name_rate=currency_name_rate,
                                currency_name_rate_2=currency_name_rate_2)

@flights.route('/peru_currency_converter_request', methods=['POST'])
def peru_currency_converter_request():
    if 'loggedin' in session:

         baseurl = 'https://api.getgeoapi.com/v2/currency/convert?api_key='

         from_currency = '&from=USD&'

         to_currency = 'to=PEN'

         amount = '&amount='

         input_amount = request.form.get('input_amount')

         json = '&format=json'

         base_currency_converter = baseurl + 'f1ca5e8f4bc4c6f729bbb2de20deb702c41f14d9' + from_currency + to_currency + amount + input_amount + json

         api = requests.get(base_currency_converter)

         currency = api.json()

         currency_name_rate = currency['amount']

         currency_name_rate_2 = currency['rates']['PEN']['rate_for_amount']

         return render_template('peru_currency.html', base_currency_converter=base_currency_converter, currency_name_rate=currency_name_rate,
                                currency_name_rate_2=currency_name_rate_2)

@flights.route('/colombia_currency_converter')
def colombia_currency_converter():
    if 'loggedin' in session:

         baseurl = 'https://api.getgeoapi.com/v2/currency/convert?api_key='

         from_currency = '&from=USD&'

         to_currency = 'to=COP'

         amount = '&amount=1'

         json = '&format=json'

         base_currency_converter = baseurl + 'f1ca5e8f4bc4c6f729bbb2de20deb702c41f14d9' + from_currency + to_currency + amount + json

         api = requests.get(base_currency_converter)

         currency = api.json()

         currency_name_rate = currency['amount']

         currency_name_rate_2 = currency['rates']['COP']['rate_for_amount']

         return render_template('colombia_currency.html', base_currency_converter=base_currency_converter, currency_name_rate=currency_name_rate,
                                currency_name_rate_2=currency_name_rate_2)

@flights.route('/colombia_currency_converter_request', methods=['POST'])
def colombia_currency_converter_request():
    if 'loggedin' in session:

         baseurl = 'https://api.getgeoapi.com/v2/currency/convert?api_key='

         from_currency = '&from=USD&'

         to_currency = 'to=COP'

         amount = '&amount='

         input_amount = request.form.get('input_amount')

         json = '&format=json'

         base_currency_converter = baseurl + 'f1ca5e8f4bc4c6f729bbb2de20deb702c41f14d9' + from_currency + to_currency + amount + input_amount + json

         api = requests.get(base_currency_converter)

         currency = api.json()

         currency_name_rate = currency['amount']

         currency_name_rate_2 = currency['rates']['COP']['rate_for_amount']

         return render_template('colombia_currency.html', base_currency_converter=base_currency_converter, currency_name_rate=currency_name_rate,
                                currency_name_rate_2=currency_name_rate_2)

@flights.route('/spain_currency_converter')
def spain_currency_converter():
    if 'loggedin' in session:

         baseurl = 'https://api.getgeoapi.com/v2/currency/convert?api_key='

         from_currency = '&from=USD&'

         to_currency = 'to=EUR'

         amount = '&amount=1'

         json = '&format=json'

         base_currency_converter = baseurl + 'f1ca5e8f4bc4c6f729bbb2de20deb702c41f14d9' + from_currency + to_currency + amount + json

         api = requests.get(base_currency_converter)

         currency = api.json()

         currency_name_rate = currency['amount']

         currency_name_rate_2 = currency['rates']['EUR']['rate_for_amount']

         return render_template('spain_currency.html', base_currency_converter=base_currency_converter, currency_name_rate=currency_name_rate,
                                currency_name_rate_2=currency_name_rate_2)

@flights.route('/spain_currency_converter_request', methods=['POST'])
def spain_currency_converter_request():
    if 'loggedin' in session:

         baseurl = 'https://api.getgeoapi.com/v2/currency/convert?api_key='

         from_currency = '&from=USD&'

         to_currency = 'to=EUR'

         amount = '&amount='

         input_amount = request.form.get('input_amount')

         json = '&format=json'

         base_currency_converter = baseurl + 'f1ca5e8f4bc4c6f729bbb2de20deb702c41f14d9' + from_currency + to_currency + amount + input_amount + json

         api = requests.get(base_currency_converter)

         currency = api.json()

         currency_name_rate = currency['amount']

         currency_name_rate_2 = currency['rates']['EUR']['rate_for_amount']

         return render_template('spain_currency.html', base_currency_converter=base_currency_converter, currency_name_rate=currency_name_rate,
                                currency_name_rate_2=currency_name_rate_2)
