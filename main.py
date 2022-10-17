#  Craig Kimball 10/13/22
#  COMP390

import requests
import sqlite3
import json

import database_functions


def main():
    """Gathers a list of meteorites on Earth from NASA's website and filters them into tables base on where they landed."""
    all_meteors = database_functions.get_json_data("https://data.nasa.gov/resource/gh4g-9sfh.json")
    print(all_meteors)

if __name__ == '__main__':
    main()
