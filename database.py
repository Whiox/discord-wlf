import os
import time
import sqlite3
from dotenv import load_dotenv
from discord import ApplicationContext


load_dotenv()

class Database:
    def __init__(self):
        db_uri = os.getenv('DB_URI')
        if db_uri.startswith("sqlite:////"):
            db_path = db_uri.replace("sqlite:////", "/", 1)
        elif db_uri.startswith("sqlite:///"):
            db_path = db_uri.replace("sqlite:///", "", 1)
        else:
            db_path = db_uri

        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = lambda cursor, row: row
        self.create_tables()

    def _execute_query(self, query, params=None):
        """Базовый метод для выполнения запросов"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or [])
            self.connection.commit()
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as error:
            print(f"Ошибка выполнения запроса: {error}")
            return None

    def get_ping(self, user_id):
        """Проверка скорости доступа к базе данных"""
        start_time = time.time()
        query = """
                SELECT *
                  FROM users
                 WHERE user_id = ?
                """
        self._execute_query(query, [user_id])
        return time.time() - start_time

    def add_user(self, ctx: ApplicationContext):
        """Добавление пользователя в базу данных"""
        query = """
        INSERT INTO users (user_id, color, timestamp)
             VALUES (?, ?, ?)
        """
        self._execute_query(query, [ctx.user.id, "ffffff", int(time.time())])

    def check_user(self, user_id):
        """Проверка на наличие пользователя в базе данных"""
        query = """
        SELECT *
          FROM users
         WHERE user_id = ?
        """
        user = self._execute_query(query, [user_id])
        return False if not user else True

    def get_private(self, user_id):
        """Получение статуса приватности пользователя"""
        query = """
        SELECT private
          FROM users
         WHERE user_id = ?
        """
        result = self._execute_query(query, [user_id])
        # Если значение равно 1 - приватный, иначе - нет
        return True if result and result[0][0] == 1 else False

    def set_private(self, user_id, private):
        """Установка статуса приватности пользователя"""
        query = """
        UPDATE users
           SET private = ?
         WHERE user_id = ?
        """
        self._execute_query(query, [1 if private else 0, user_id])

    def get_color(self, user_id):
        """Получение цвета указанного пользователем"""
        query = """
        SELECT color
          FROM users
         WHERE user_id = ?
        """
        result = self._execute_query(query, [user_id])
        return result[0][0] if result else None

    def set_color(self, user_id, color):
        """Установка цвета указанному пользователю"""
        query = """
        UPDATE users 
           SET color = ?
         WHERE user_id = ?
        """
        self._execute_query(query, [color, user_id])

    def get_first_command(self, user_id):
        """Получение информации о первой команде пользователя (timestamp)"""
        query = """
        SELECT timestamp
          FROM users
         WHERE user_id = ?
        """
        response = self._execute_query(query, [user_id])
        return response[0][0] if response else None

    def create_users_table(self):
        """Создание таблицы users"""
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            color TEXT,
            private INTEGER NOT NULL DEFAULT 0,
            timestamp INTEGER NOT NULL
        )
        """
        self._execute_query(query)

    def create_tables(self):
        self.create_users_table()
