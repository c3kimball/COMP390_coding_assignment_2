#  Craig Kimball 10/13/22
#  COMP390

import requests
import sqlite3
import json

import database_functions


def main():
    database_functions.make_database("https://data.nasa.gov/resource/gh4g-9sfh.json")

if __name__ == '__main__':
    main()
