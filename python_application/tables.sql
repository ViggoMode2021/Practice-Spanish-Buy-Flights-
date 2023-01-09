CREATE TABLE random_places(
random_place TEXT,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE dictionary_of_words(
ID SERIAL PRIMARY KEY,
english_word TEXT,
spanish_word TEXT,
username TEXT,
date_added_on TEXT,
time_added_on TEXT,
category TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE random_times (
random_time TEXT,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE random_adjectives (
random_adjectives TEXT,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE flights (
ID SERIAL PRIMARY KEY,
flight TEXT,
price INT,
departure_date DATE,
departure_time TIME,
return_date DATE,
return_time TIME,
confirmed BOOLEAN,
date_confirmed TEXT,
time_confirmed TEXT,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE random_places(
ID INT PRIMARY KEY,
random_place TEXT,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

INSERT INTO spanish_users(username,overall_score,account_creation_date)
VALUES ('ryansviglione@gmail.com', 40, 7-12-2022);

CREATE TABLE spanish_users(
username TEXT UNIQUE,
overall_score INT,
account_creation_date TEXT);

ALTER TABLE spanish_users ADD COLUMN delete_account_code INT;

CREATE TABLE random_numbers(
random_number_one INT,
random_number_two INT,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE upload_recordings(
recording_name TEXT,
date_upload TEXT,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE user_practice_records (
ID SERIAL PRIMARY KEY,
category_name TEXT,
english_word TEXT,
spanish_word TEXT,
correct_incorrect TEXT,
date_added VARCHAR,
time_added VARCHAR,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE random_speaking (
recording TEXT,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE random_food_or_drink (
random_food_or_drink TEXT,
username TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);

CREATE TABLE lex_convo (
ID SERIAL PRIMARY KEY,
username TEXT,
time_sent TEXT,
sent_message TEXT,
received_message TEXT,
FOREIGN KEY ("username") REFERENCES spanish_users("username") ON DELETE CASCADE);
