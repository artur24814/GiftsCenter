from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

import click
import os

from flask import current_app, g

from dotenv import load_dotenv
from core.db_questions import CREATE_DB, CREATE_USERS_TABLE, CREATE_TABLE_USER_FRIENDS, CREATE_TABLE_USERS_ACTIONS, CREATE_TABLE_ITEMS, CREARE_TABLE_ACTIONS
import sqlite3

load_dotenv()


DB = os.getenv('DB')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

#get db for testing
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def create_conn(testing=False):
    try:
        if current_app.config['TESTING'] is True or testing:
            cnx = sqlite3.connect(current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            cursor = cnx.cursor()
            return cnx, cursor
    except Exception:
        cnx = connect(database=DB, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cnx.autocommit = True
        cursor = cnx.cursor()
        return cnx, cursor


def init_db(test=False):
    if test is True:
        db = get_db()
        #get testing schema
        with current_app.open_resource(f'{os.getcwd()}/tests/schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
    else:
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

            try:
                cursor.execute(CREATE_TABLE_USER_FRIENDS)
                print('Table User Friends created')
            except DuplicateTable as e:
                print('Table user friends exist: ', e)


            cnx.close()

        except OperationalError as e:
            print('Connection Error: ', e)


@click.command('init-db')
def init_db_command():
    """Create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)

