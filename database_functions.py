#  Craig Kimball 10/13/22
#  Functions that access NASA's meteorite database

import requests
import sqlite3
import json


def get_json_data(website):
    """Returns a json object from the website link provided.
     If the request is unsuccessful the program will stop."""

    try:
        response_obj = requests.get(website)
        json_obj = response_obj.json()
        return json_obj
    except requests.exceptions.RequestException as e:
        print(f"Error in getting getting data: {e}")
        raise SystemExit()

