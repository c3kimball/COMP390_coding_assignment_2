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


def convert_dict_to_string(dict_entry):
    """Decodes a json dictionary value into plain text"""
    if dict_entry.get('geolocation', None) is None:
        return None
    return json.dumps(dict_entry['geolocation'])


def create_meteorite_database(json_obj):
    """Creates an SQL database of all the meteorites. Returns a 1 if a database error occurred."""

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

        for dict_entry in json_obj:
            db_cursor.execute('''INSERT INTO meteorite_data_all VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (dict_entry.get('name', None),
                               int(dict_entry.get('id', None)),
                               dict_entry.get('nametype', None),
                               dict_entry.get('recclass', None),
                               dict_entry.get('mass', None),
                               dict_entry.get('fall', None),
                               dict_entry.get('year', None),
                               dict_entry.get('reclat', None),
                               dict_entry.get('reclong', None),
                               convert_dict_to_string(dict_entry),
                               dict_entry.get(':@computed_region_cbhk_fwbd', None),
                               dict_entry.get(':@computed_region_nnqa_25f4', None)))
        db_connection.commit()

    except sqlite3.Error as db_error:
        print(f"A database error has occurred: {db_error}")
        return 1

    finally:
        if db_connection:
            db_connection.close()


def create_region_databases():
    """If there is a nice and neat way to create 7 SQL tables, that's what I would want this to do.
    But for now, I will focus on making only 1 region, Europe, because that has the highest concentration of meteorites"""

    db_connection = None

    try:
        db_name = 'europe_region.db'
        db_connection = sqlite3.Connection(db_name)
        db_cursor = db_connection.cursor()

        db_cursor.execute('''CREATE TABLE IF NOT EXISTS europe_region(
            name TEXT,
            mass TEXT,
            reclat TEXT,
            reclong TEXT);''')

        db_cursor.execute('''DELETE FROM europe_region''')
        db_connection.commit()
        print("committed changes")

    except sqlite3.Error as region_error:
        print(f"Error in creating region databases: {region_error}")
        return 1

    finally:
        if db_connection:
            db_connection.close()
