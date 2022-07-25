import copy
import tempfile
from pathlib import Path
from unittest import TestCase

from src.database.database_manager import DatabaseManager
from src.database.database_model import QuestionUserData
from src.question_model import QuizModel, QuestionModel, AnswerModel, QuestionUserDataModel


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
            AnswerModel(id=1, text='A', is_correct=False),
            AnswerModel(id=2, text='B', is_correct=True),
            AnswerModel(id=3, text='C', is_correct=False)]
        answers_2 = [
            AnswerModel(id=4, text='1', is_correct=False),
            AnswerModel(id=5, text='2', is_correct=True),
            AnswerModel(id=6, text='3', is_correct=False)
        ]
        questions = [QuestionModel(id=1, text='Question 1', answers=answers_1),
                     QuestionModel(id=2, text='Question 2', answers=answers_2, image_path='image_path')]
        first_quiz = QuizModel(id=1, name='First quiz', questions=questions)
        second_quiz = QuizModel(id=2, name='Second quiz', questions=[])
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
            AnswerModel(id=10, text='100', is_correct=False),
            AnswerModel(id=11, text='200', is_correct=True),
            AnswerModel(id=12, text='300', is_correct=False)
        ]
        user_data = QuestionUserDataModel(level=4, correct_answer=3)
        questions = [QuestionModel(id=10, text='Question 1', answers=answers, user_data=user_data)]
        new_quiz = QuizModel(id=10, name='New quiz', questions=questions)

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

    def test_update_question_user_data(self):
        """Test updating question user data, such as level, correct answers and notes. """
        initial_state = self.database_manager.get_quizzes()
        self.assertEqual(initial_state, [self.first_quiz, self.second_quiz])

        change_quiz = copy.deepcopy(self.first_quiz)

        self.assertEqual(None, change_quiz.questions[0].user_data)

        change_quiz.questions[0].user_data = QuestionUserDataModel(level=1, correct_answer=4, comment='new comment')
        self.database_manager.update_question_user_data(change_quiz.questions[0].user_data, change_quiz.questions[0].id)
        check_state = self.database_manager.get_quizzes()
        self.assertEqual([change_quiz, self.second_quiz], check_state)

        self.database_manager.update_question_user_data(change_quiz.questions[0].user_data, change_quiz.questions[0].id)
        check_final_state = self.database_manager.get_quizzes()
        self.assertEqual([change_quiz, self.second_quiz], check_final_state)
