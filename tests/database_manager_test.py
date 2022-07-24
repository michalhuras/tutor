import tempfile
from pathlib import Path
from unittest import TestCase

from src.database.database_manager import DatabaseManager
from src.question_model import QuizModel, QuestionModel, AnswerModel, QuestionProgress


class DatabaseManagerTests(TestCase):
    """Unit tests database manager module. """
    @classmethod
    def setUpClass(cls):
        """Create empty database in temporary directory before any test starts. """
        tmp_dir = tempfile.TemporaryDirectory()
        database_name = 'tmp_database.db'
        database_path = str(Path(tmp_dir.name, database_name))
        DatabaseManager.create_database(database_path)
        cls.tmp_dir = tmp_dir
        cls.database_manager = DatabaseManager(database_path)

    @classmethod
    def tearDownClass(cls) -> None:
        """This function is called after tests in this entire class have run.
        It deletes temporary directory used for tests.
        """
        cls.tmp_dir.cleanup()

    def setUp(self):
        """Erase old record from database and insert default values for every test. """
        self.database_manager.erase_all_quizzes()

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
        first_quiz = QuizModel(name='First quiz', questions=questions)
        second_quiz = QuizModel(name='Second quiz', questions=[])
        self.first_quiz = first_quiz
        self.second_quiz = second_quiz
        self.database_manager.add_quiz(first_quiz)
        self.database_manager.add_quiz(second_quiz)

    def test_get_quizzes(self):
        """ Test if function getting quizzes data from database work correctly. """
        result = self.database_manager.get_quizzes()
        self.assertEqual([self.first_quiz, self.second_quiz], result)

    def test_get_quizzes_names(self):
        """Check if the get_quizzes_names function returns all the quizzes names from database. """
        expected_result = [self.first_quiz.name, self.second_quiz.name]

        result = self.database_manager.get_quizzes_names()
        self.assertEqual(expected_result, result)

    def test_add_quiz(self):
        """Test adding single quiz to an existing database. """
        answers = [
            AnswerModel(text='100', is_correct=False),
            AnswerModel(text='200', is_correct=True),
            AnswerModel(text='300', is_correct=False)
        ]
        question_progress = QuestionProgress(level=4, correct_answer=3)
        # question_progress = None
        questions = [QuestionModel(text='Question 1', answers=answers, progress=question_progress)]
        new_quiz = QuizModel(name='New quiz', questions=questions)

        initial_state = self.database_manager.get_quizzes()
        self.assertFalse(new_quiz in initial_state)

        self.database_manager.add_quiz(new_quiz)
        final_state = self.database_manager.get_quizzes()
        self.assertTrue(new_quiz in final_state)

    def test_get_quiz(self):
        """Test extracting a quiz model from database base on his name. """
        expected_result = self.first_quiz
        quiz_name = expected_result.name

        result = self.database_manager.get_quiz(quiz_name)
        self.assertEqual(expected_result, result)

    def test_erase_all_quizzes(self):
        """Test erasing every quiz in a database. """
        initial_state = self.database_manager.get_quizzes()
        self.assertTrue(len(initial_state) != 0)

        self.database_manager.erase_all_quizzes()
        final_state = self.database_manager.get_quizzes()
        self.assertTrue(len(final_state) == 0)

    def test_erase_all_quizzes(self):
        """Test erasing every quiz in a database. """
        initial_state = self.database_manager.get_quizzes()
        self.assertTrue(len(initial_state) != 0)

        self.database_manager.erase_all_quizzes()
        final_state = self.database_manager.get_quizzes()
        self.assertTrue(len(final_state) == 0)
