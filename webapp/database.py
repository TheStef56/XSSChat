import mysql.connector as c
from mysql.connector import pooling
from datetime import datetime
import secrets


class Database:
    def __init__(self, host, dbusername, dbpassword, dbname):
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=10,
            host=host,
            user=dbusername,
            password=dbpassword,
            database=dbname
        )

    def _exec_query(self, query, params=None, commit=False, fetch=True):
        conn = None
        cursor = None
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()

            cursor.execute(query, params or ())

            if commit:
                conn.commit()

            if fetch:
                return cursor.fetchall()

            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()  # returns connection to pool

    # ---------------- USERS ---------------- #

    def get_user(self, username, password):
        return self._exec_query(
            "SELECT * FROM user WHERE username = %s AND password = %s",
            (username, password)
        )

    def get_user_by_name(self, username):
        return self._exec_query(
            "SELECT * FROM user WHERE username = %s",
            (username,)
        )
    
    def get_user_by_email(self, email):
        return self._exec_query(
            "SELECT * FROM user WHERE email = %s",
            (email,)
        )

    def get_users(self):
        return self._exec_query("SELECT * FROM user")

    def register(self, email, username, password):
        self._exec_query(
            "INSERT INTO user (email, username, password) VALUES (%s, %s, %s)",
            (email, username, password),
            commit=True,
            fetch=False
        )

    def change_password(self, username, password):
        self._exec_query(
            "UPDATE user SET password = %s WHERE username = %s",
            (password, username),
            commit=True,
            fetch=False
        )

    # ---------------- TOKENS ---------------- #

    def set_token(self, username, password):
        token = secrets.token_hex(8)

        self._exec_query(
            "UPDATE user SET token = %s WHERE username = %s AND password = %s",
            (token, username, password),
            commit=True,
            fetch=False
        )

        return token

    def delete_token(self, token):
        self._exec_query(
            "UPDATE user SET token = NULL WHERE token = %s",
            (token,),
            commit=True,
            fetch=False
        )

    def get_user_by_token(self, token):
        return self._exec_query(
            "SELECT * FROM user WHERE token = %s",
            (token,)
        )

    # ---------------- MESSAGES ---------------- #

    def get_messages(self):
        return self._exec_query("SELECT * FROM message")

    def insert_message(self, token, message):
        user = self._exec_query(
            "SELECT id, username FROM user WHERE token = %s",
            (token,)
        )

        if not user:
            return

        user_id, username = user[0]

        self._exec_query(
            "INSERT INTO message (user_id, username, message, date) VALUES (%s, %s, %s, %s)",
            (user_id, username, message, datetime.now()),
            commit=True,
            fetch=False
        )