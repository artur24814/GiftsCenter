from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

import click
from flask import current_app, g

from dotenv import load_dotenv
import os

load_dotenv()

CREATE_DB = "CREATE DATABASE flask_database;"

CREATE_USERS_TABLE = """CREATE TABLE users(
 id serial PRIMARY KEY, 
 username varchar(255) UNIQUE,
 hashed_password varchar(80))"""

CREARE_TABLE_ACTIONS = '''CREATE TABLE actions(
 id SERIAL PRIMARY KEY,
 id_user INTEGER REFERENCES users(id) ON DELETE CASCADE,
 title varchar(255) NOT NULL,
 descriptions varchar(500),
 date DATE,
 img varchar(1000))
'''  # data - YYYY-MM-DD

CREATE_TABLE_ITEMS = '''CREATE TABLE items(
 id SERIAL PRIMARY KEY,
 id_action INTEGER REFERENCES actions(id) ON DELETE CASCADE,
 id_user INTEGER REFERENCES users(id) ON DELETE CASCADE,
 text varchar(500),
 yes_no BOOLEAN)
'''

ADD_USER_TABLE_ITEMS = '''ALTER TABLE items ADD id_user INTEGER 
REFERENCES users(id) ON DELETE CASCADE'''

CREATE_TABLE_USERS_ACTIONS = """CREATE TABLE users_actions(
id SERIAL PRIMARY KEY,
id_user INTEGER REFERENCES users(id) ON DELETE CASCADE,
id_action INTEGER REFERENCES actions(id) ON DELETE CASCADE)
"""

DB = os.getenv('DB')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


def create_conn():
    cnx = connect(database=DB, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)  # host=DB_HOST, port=DB_PORT
    cnx.autocommit = True
    cursor = cnx.cursor()
    return cnx, cursor


def init_db():
    try:
        try:
            cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)  # host=DB_HOST, port=DB_PORT
            cnx.autocommit = True
            cursor = cnx.cursor()
            cursor.execute(CREATE_DB)
            print('Database created')
        except DuplicateDatabase as e:
            print('Database exist: ', e)
        cnx, cursor = create_conn()
        try:
            cursor.execute(CREATE_USERS_TABLE)
            print('Table Users created')
        except DuplicateTable as e:
            print('Table users exist: ', e)

        try:
            cursor.execute(CREARE_TABLE_ACTIONS)
            print('Table actions created')
        except DuplicateTable as e:
            print('Table actions exist: ', e)

        try:
            cursor.execute(CREATE_TABLE_ITEMS)
            print('Table Items created')
        except DuplicateTable as e:
            print('Table itemss exist: ', e)
        try:
            cursor.execute(CREATE_TABLE_USERS_ACTIONS)
            print('Table Users Actions created')
        except DuplicateTable as e:
            print('Table users actions exist: ', e)

        cnx.close()

    except OperationalError as e:
        print('Connection Error: ', e)


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)

