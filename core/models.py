from core.core_security import hash_password
from flask import current_app, url_for
from flask_mail import Mail, Message

import datetime


class User:
    def __init__(self, username='', password='', salt=''):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def create_user(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def get_user_by_id(cursor, id_):
        sql = 'SELECT id, username, hashed_password FROM users WHERE id=%s'
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))  # (username, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    def check_user(self, cursor):
        sql = 'SELECT id, username, hashed_password FROM users WHERE username=%s AND hashed_password=%s'
        cursor.execute(sql, (self.username, self._hashed_password))
        data = cursor.fetchone()
        if data:
            return True
        else:
            return None

    @staticmethod
    def get_all(cursor):
        sql = "SELECT id, username, hashed_password FROM users"

        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self._id,))
        self._id = -1
        return True

    @staticmethod
    def search(cursor, question):
        sql = "SELECT id, username, hashed_password FROM users WHERE username ILIKE %s"
        cursor.execute(sql, ('%'+ question + '%',))
        users = []
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

class Actions:
    def __init__(self, id_user, title, descriptions, date, image):
        self._id = -1

        self.id_user = id_user
        self.title = title
        self.descriptions = descriptions
        self.date = date
        self.img = image

    @property
    def id(self):
        return self._id

    def create(self, cursor):
        if User.get_user_by_id(cursor=cursor, id_=self.id_user) is None:
            return False

        if self._id == -1:
            if self.check_data() is False:
                return 'Error date format!'

            sql = """INSERT INTO actions (id_user, title, descriptions, date, img)
            VALUES(%s, %s, %s, %s, %s) RETURNING id
            """
            values = (self.id_user, self.title, self.descriptions, self.date, self.img)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()
            return True
        else:
            if self.check_data() is False:
                return 'Error date format!'
            sql = """UPDATE actions SET id_user=%s, title=%s, descriptions=%s, date=%s, img=%s WHERE id=%s
            """
            values = (self.id_user, self.title, self.descriptions, self.date, self.img, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def set_users_action(cursor, user_id):
        sql = "SELECT * FROM actions WHERE id_user=%s"

        cursor.execute(sql, (user_id,))
        actions = []
        for row in cursor.fetchall():
            id_, id_user, title, descriptions, date, img = row
            loaded_action = Actions(id_user, title, descriptions, date, img)
            loaded_action._id = id_
            actions.append(loaded_action)
        return actions

    @staticmethod
    def get_all(cursor):
        sql = "SELECT * FROM actions"

        cursor.execute(sql)
        actions = []
        for row in cursor.fetchall():
            id_, id_user, title, descriptions, date, img = row
            loaded_action = Actions(id_user, title, descriptions, date, img)
            loaded_action._id = id_
            actions.append(loaded_action)
        return actions

    @staticmethod
    def get_by_id(cursor, id):
        sql = "SELECT * FROM actions WHERE id=%s"

        cursor.execute(sql, (id,))
        data = cursor.fetchone()
        if data:
            id_, id_user, title, descriptions, date, img = data
            loaded_action = Actions(id_user, title, descriptions, date, img)
            loaded_action._id = id_
            return loaded_action

    def check_data(self):
        try:
            date = self.date.split('-')

            if len(date[0]) == 4 and 0 < int(date[1]) < 13 and 0 < int(date[2]) < 32 and int(date[0]) > 0:
                now = datetime.datetime.now()
                asken_date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
                if now > asken_date:
                    print(asken_date)
                    print(now)
                    return False
            return True
        except Exception:
            return False

    def delete(self, cursor):
        sql = 'DELETE FROM actions WHERE id=%s'

        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

    def set_image(self, cursor, img):
        if self._id == -1:
            'First save image'
        else:
            imagepath = 'media/' + img
            sql = "UPDATE actions SET image=%s WHERE id=%s"
            values = (imagepath, self._id)
            cursor.execute(sql, values)
            return True


    @staticmethod
    def search(cursor, question):
        sql = "SELECT * FROM actions WHERE title ILIKE %s"
        cursor.execute(sql, ("%" + question + "%",))
        actions = []
        for row in cursor.fetchall():
            id_, id_user, title, descriptions, date, img = row
            loaded_action = Actions(id_user, title, descriptions, date, img)
            loaded_action._id = id_
            actions.append(loaded_action)
        return actions


class Items:
    def __init__(self, id_action, text, yes_no, id_user):
        self._id = -1
        self.id_actions = id_action
        self.text = text
        self.yes_no = yes_no
        self.id_user = id_user

    @property
    def id(self):
        return self._id

    def create(self, cursor):
        if Actions.get_by_id(cursor, self.id_actions) is None:
            return False
        if self._id == -1:
            sql = """INSERT INTO items (id_action, text, yes_no, id_user) 
                    VALUES (%s, %s, %s, %s) RETURNING id"""
            values = (self.id_actions, self.text, self.yes_no, self.id_user)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()
            return True
        else:
            sql = """UPDATE items SET id_action=%s, text=%s, yes_no=%s, id_user=%s WHERE id=%s"""
            values = (self.id_actions, self.text, self.yes_no, self.id_user, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def get_items(cursor, id_action):
        sql = """SELECT * FROM items WHERE id_action=%s"""
        items = []
        cursor.execute(sql, (id_action,))
        for row in cursor.fetchall():
            id_, id_action_, text, yes_no, id_user = row
            loaded_item = Items(id_action_, text, yes_no, id_user)
            loaded_item._id = id_
            items.append(loaded_item)
        return items

    @staticmethod
    def get_by_id(cursor, id):
        sql = "SELECT * FROM items WHERE id=%s"
        cursor.execute(sql, (id,))
        data = cursor.fetchone()
        if data:
            id_, id_action_, text, yes_no, id_user = data
            loaded_item = Items(id_action_, text, yes_no, id_user)
            loaded_item._id = id_
            return loaded_item

    @staticmethod
    def check_user(cursor, id_user, id_action):
        sql = "SELECT * FROM items WHERE id_action=%s and id_user=%s"
        cursor.execute(sql, (id_action, id_user))
        if len(cursor.fetchall()) == 0:
            return True
        else:
            return False

class UsersActions:
    def __init__(self, id_user, id_action):
        self._id = -1
        self.id_user = id_user
        self.id_action = id_action

    @property
    def id(self):
        return self._id

    def create(self, cursor):
        if self._id == -1 and self.check_user(cursor) is True:
            sql = """INSERT INTO users_actions (id_user, id_action) 
            VALUES (%s, %s) RETURNING id"""
            values = (self.id_user, self.id_action)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()
            user = User.get_user_by_id(cursor, self.id_user)
            action = Actions.get_by_id(cursor, self.id_action)
            mail = Mail(current_app)
            msg = Message('Hello', sender='flaskApp@gmail.com', recipients=['artur24814@gmail.com'])
            msg.body = f"Hello {user.username}, your was invited to {action.title} {url_for('main.action', id=action.id)}!!!"
            mail.send(msg)
            return True
        else:
            return False

    def check_user(self, cursor):
        sql = "SELECT * FROM users_actions WHERE id_user=%s and id_action=%s"
        values = (self.id_user, self.id_action)
        cursor.execute(sql, values)
        if len(cursor.fetchall()) == 0:
            return True
        else:
            return False

    @staticmethod
    def get_all_users(cursor, id_action):
        sql = "SELECT id_user FROM users_actions WHERE id_action=%s"
        values = (id_action, )
        cursor.execute(sql, values)
        users = []
        for row in cursor.fetchall():
            id_user = row
            loaded_user = User.get_user_by_id(cursor, id_user)
            users.append(loaded_user)
        return users

class UserFriends:

    def __init__(self, id_user, friend):
        self._id = -1
        self.id_user = id_user
        self.friend = friend

    @property
    def id(self):
        return self._id

    def create(self, cursor):
        if self._id == -1 and self.check_friend(cursor) is True:
            sql = """INSERT INTO friends (id_user, friend)
            VALUES (%s, %s) RETURNING id"""
            values = (self.id_user, self.friend)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()
            return True
        else:
            return False

    def check_friend(self, cursor):
        sql = "SELECT * FROM friends WHERE id_user=%s and friend=%s"
        values = (self.id_user, self.friend)
        cursor.execute(sql, values)
        if len(cursor.fetchall()) == 0:
            return True
        else:
            return False

    def delete_friend(self, cursor):
        if self.check_friend(cursor) is False:
            sql = "DELETE FROM friends WHERE id_user=%s and friend=%s"
            values = (self.id_user, self.friend)
            cursor.execute(sql, values)
            return True
        else:
            return False

    @staticmethod
    def get_friends(cursor, id_user):
        sql = "SELECT friend FROM friends WHERE id_user=%s"
        cursor.execute(sql, (id_user,))
        users = []
        for row in cursor.fetchall():
            id_ = row
            loaded_user = User.get_user_by_id(cursor,id_)
            users.append(loaded_user)
        return users
