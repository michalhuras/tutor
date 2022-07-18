"""Database manager. It is used to add new questions to existing database. """
import sqlite3
from datetime import datetime
from sqlite3 import Error
from typing import List, Optional

from src.question_model import QuizModel, QuestionModel, AnswerModel
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


def add_quiz(database_path: str, model: QuizModel) -> None:
    """Add new quiz to existing database.
    It may raise SQLite3 exception if there will be problem with the database file.
    """
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        quiz_description = ''
        cursor.execute(f'INSERT INTO quiz (name, description, date) '
                       f'VALUES (\'{model.name}\', \'{quiz_description}\', \'{datetime.now()}\');')

        cursor.execute('select last_insert_rowid()')
        quiz_id = cursor.fetchone()[0]
        for question in model.questions:
            add_question(question, cursor, quiz_id)

        connection.commit()
        cursor.close()


def add_question(question_model: QuestionModel, cursor: sqlite3.Cursor, quiz_id: int) -> None:
    """Add new question in quiz to existing database. """
    parameters = (quiz_id,
                  question_model.text,
                  question_model.image_path if question_model.image_path else None,
                  question_model.comment if question_model.comment else None,
                  question_model.user_comments if question_model.user_comments else None)
    cursor.execute(f'INSERT INTO question (quiz_id, text, image_path, notes, user_notes) '
                   f'VALUES(?, ?, ?, ?, ?);', parameters)

    cursor.execute('select last_insert_rowid();')
    question_id = cursor.fetchone()[0]

    for answer in question_model.answers:
         add_answers(answer, cursor, quiz_id, question_id)


def add_answers(answer_model: AnswerModel, cursor: sqlite3.Cursor, quiz_id: int, question_id: int) -> None:
    """Add new answer in question to existing database. """
    parameters = (question_id, quiz_id, answer_model.text, answer_model.is_correct)
    cursor.execute(f'INSERT INTO answer (question_id, quiz_id, text, is_correct) '
                   f'VALUES(?, ?, ?, ?);', parameters)


def get_quizzes(database_path: str) -> Optional[List[QuizModel]]:
    """Returns list of object representation of quizzes stored in a database. """
    try:
        with sqlite3.connect(database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT id, name, description, date FROM quiz;')

            quizzes = []
            for quiz_data in cursor.fetchall():
                quiz_id = quiz_data[0]
                cursor.execute(
                    f'SELECT id, text, image_path, notes, user_notes FROM question WHERE quiz_id = ?;',
                    (quiz_id,))
                questions = []
                for question_data in cursor.fetchall():
                    question_id = question_data[0]
                    cursor.execute(f'SELECT text, is_correct FROM answer WHERE quiz_id = ? AND question_id = ?;',
                                   (quiz_id, question_id))
                    answers = [AnswerModel(answer_data[0], bool(answer_data[1])) for answer_data in cursor.fetchall()]
                    questions.append(QuestionModel(text=question_data[1],
                                                   image_path=question_data[2],
                                                   comment=question_data[3],
                                                   user_comments=question_data[4],
                                                   answers=answers))
                quizzes.append(QuizModel(name=quiz_data[1], questions=questions))

            cursor.close()
            return quizzes
    except Error as err:
        print(f'Error occurred while processing request:\n {err}')
