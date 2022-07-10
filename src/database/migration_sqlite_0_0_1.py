"""Migration file for SQLite database. It should generate new database if it does not exist,
and update existing if its version does not match with current.
"""
import sqlite3
from collections import namedtuple
from os import path

version_format = namedtuple("version_format", "major minor patch")
DATA_PATH = 'data'
VERSION = version_format(0, 0, 1)
DEFAULT_DATABASE = f'{DATA_PATH}/quiz.db'


def migrate_if_needed(db_path: str) -> None:
    """This function should migrate database if the version is older that current schema.
    This is initial version of the database, so no update won't be needed.
    """
    print(f'There is nothing to do database \'{db_path}\' already exists.')


def create_database(db_path: str):
    """Create a database connection to a SQLite database. """
    conn = None
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS version (major INTEGER, minor INTEGER, patch INTEGER);')
        cursor.execute(f'INSERT INTO version (major, minor, patch) '
                       f'VALUES({VERSION.major}, {VERSION.minor}, {VERSION.patch});')
        cursor.execute('CREATE TABLE IF NOT EXISTS quiz ('
                       'id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT, date DATETIME);')
        connection.commit()

        cursor.execute('CREATE TABLE IF NOT EXISTS question ('
                       'id INTEGER PRIMARY KEY, '
                       'quiz_id INTEGER NOT NULL, '
                       'text TEXT NOT NULL, '
                       'image_path TEXT, '
                       'notes TEXT, '
                       'user_notes TEXT, '
                       'FOREIGN KEY(quiz_id) REFERENCES quiz(id));')
        connection.commit()

        cursor.execute('CREATE TABLE IF NOT EXISTS answer ('
                       'id INTEGER PRIMARY KEY, '
                       'question_id INTEGER NOT NULL, '
                       'quiz_id INTEGER NOT NULL, '
                       'text TEXT NOT NULL, '
                       'is_correct BOOLEAN, '
                       'FOREIGN KEY(question_id) REFERENCES question(id));')
        connection.commit()
        cursor.close()
    except sqlite3.Error as err:
        print(f'Error occurred while trying to create {db_path} database:\n{err}')
    finally:
        if conn:
            conn.close()


def if_db_exists(db_path: str) -> bool:
    """Check if database in path exists. """
    return path.exists(db_path)


def run(db_path: str) -> None:
    """Generate new database if it does not exist, and update existing if its version does not match with current."""
    if if_db_exists(db_path):
        migrate_if_needed(db_path)
    else:
        create_database(db_path)


if __name__ == '__main__':
    run(DEFAULT_DATABASE)
