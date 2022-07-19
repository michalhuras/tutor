import tempfile
from pathlib import Path
from unittest import TestCase

from src.database.database_manager import add_quiz, get_quizzes, create_database
from src.question_model import QuizModel, QuestionModel, AnswerModel


class DatabaseManagerTests(TestCase):
    """Unit tests database manager module. """
    def test_add_and_get_quizzes(self):
        """ Test if functions adding and getting quizzes data to database work correctly.
        Function add_quiz and get_quizzes are being tested simultaneously.
        If any errors occur next test will be added, covering special testcases.
        Database for tests is being created in temporary directory.
        """
        answers_1 = [
            AnswerModel(text='A', is_correct=False),
            AnswerModel(text='B', is_correct=True),
            AnswerModel(text='C', is_correct=False)]
        answers_2 = [
            AnswerModel(text='1', is_correct=False),
            AnswerModel(text='2', is_correct=True),
            AnswerModel(text='3', is_correct=False)
        ]
        questions = [QuestionModel(text='Question 1', answers=answers_1),
                     QuestionModel(text='Question 2', answers=answers_2, image_path='image_path')]
        quiz = QuizModel(name='Quiz name', questions=questions)

        with tempfile.TemporaryDirectory() as tmp_directory_name:
            database_name = 'tmp_database.db'
            database_path = Path(tmp_directory_name, database_name)
            create_database(str(database_path))

            add_quiz(str(database_path), quiz)

            result = get_quizzes(str(database_path))

            self.assertEqual([quiz], result)
