#  Craig Kimball 10/13/22
#  Functions that access NASA's meteorite database

import requests
import sqlite3
import json


def get_json_data(website):
    """Returns a json object from the url provided.
     If the request is unsuccessful the program will stop."""

    try:
        response_obj = requests.get(website)
        json_obj = response_obj.json()
        return json_obj
    except requests.exceptions.RequestException as requests_error:
        print(f"Error in getting getting data: {requests_error}")
        raise SystemExit()


def create_database(json_obj):
    """Creates an SQL database from json_obj."""

    db_connection = None  # Just a failsafe in case the try block is never reached

    try:
        db_name = 'all_meteorites.db'
        db_connection = sqlite3.Connection(db_name)
        db_cursor = db_connection.cursor()

        db_cursor.execute('''CREATE TABLE IF NOT EXISTS meteorite_data_all(
                        name TEXT,
                        id INTEGER,
                        nametype TEXT,
                        recclass TEXT,
                        mass TEXT,
                        fall TEXT,
                        year TEXT,
                        reclat TEXT,
                        reclong TEXT,
                        geolocation TEXT,
                        states TEXT,
                        counties TEXT);''')

        db_cursor.execute('''DELETE FROM meteorite_data_all''')

    except sqlite3.Error as db_error:
        print(f"A database error has occured: {db_error}")
        return None
    finally:
        if db_connection:
            db_connection.close()
        print("Job's done.")

