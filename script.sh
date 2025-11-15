#!/bin/bash

DB_FILE=data.db

#run only if the database file is not present.
if [ ! -f "$DB_FILE" ]; then
    # create databse and tables 
    sqlite3 "$DB_FILE" < schema.sql

    #install required dependencies
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

    # generate and populate the table with
    # fake data using Python faker library
    python generate_data.py
fi


