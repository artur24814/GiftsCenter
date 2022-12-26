"""
SQL question for command 'init_db'
"""

CREATE_DB = "CREATE DATABASE flask_database;"

CREATE_USERS_TABLE = """CREATE TABLE users(
 id serial PRIMARY KEY, 
 username varchar(255) UNIQUE,
 hashed_password varchar(80),
 email VARCHAR(200))"""

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
ADD_USER_EMAIL_FIELD = '''ALTER TABLE users ADD email VARCHAR(200)
'''

ADD_USER_TABLE_ITEMS = '''ALTER TABLE items ADD id_user INTEGER 
REFERENCES users(id) ON DELETE CASCADE'''

CREATE_TABLE_USERS_ACTIONS = """CREATE TABLE users_actions(
id SERIAL PRIMARY KEY,
id_user INTEGER REFERENCES users(id) ON DELETE CASCADE,
id_action INTEGER REFERENCES actions(id) ON DELETE CASCADE)
"""

CREATE_TABLE_USER_FRIENDS = """CREATE TABLE friends(
id SERIAL PRIMARY KEY,
id_user INTEGER REFERENCES users(id) ON DELETE CASCADE,
friend INTEGER REFERENCES users(id) ON DELETE CASCADE)
"""