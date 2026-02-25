"""
simple-example init.py

Run this script once before starting the example to create and
initialize the sqlite state used by the PLCs.
"""

from sqlite3 import OperationalError

from minicps.states import SQLiteState
from utils import PATH, SCHEMA, SCHEMA_INIT


if __name__ == "__main__":

    try:
        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)
        print("{} successfully created.".format(PATH))
    except OperationalError:
        print("{} already exists.".format(PATH))

