"""Unit tests for data models from question_model module. """
import copy
from typing import List
from unittest import TestCase

from src.question_model import LearningModel, QuizModel, QuestionModel, AnswerModel, QuestionUserDataModel


class LearningModelUnitTests(TestCase):
    """Unit tests for QuestionModel class. """

    @classmethod
    def setUpClass(cls):
        """Sety up before any of the tests. Define data needed in tests. """
        cls.questions = [QuestionModel(id=1, text='question 1', answers=[
            AnswerModel(id=1, text='answer 1', is_correct=True),
            AnswerModel(id=2, text='answer 2', is_correct=False),
            AnswerModel(id=3, text='answer 3', is_correct=False)], user_data=QuestionUserDataModel()),
                     QuestionModel(id=2, text='question 2', answers=[
                         AnswerModel(id=4, text='answer 4', is_correct=False),
                         AnswerModel(id=5, text='answer 5', is_correct=True),
                         AnswerModel(id=6, text='answer 6', is_correct=True)
                     ], user_data=QuestionUserDataModel(level=3, correct_answer=1)),
                     QuestionModel(id=3, text='question 3', answers=[
                         AnswerModel(id=7, text='answer 7', is_correct=False)], user_data=QuestionUserDataModel())
                     ]
        cls.quiz_model = QuizModel(id=1, name='quiz name', questions=cls.questions)

    def test_create_from_quiz_model(self):
        """Check if creating LearningModel from quiz model works correctly. """
        # TODO padding
        expected_result = LearningModel.parse_obj(
            {"learning_levels":
                [[{"id": 1, "text": "question 1", "answers": [{"id": 1, "text": "answer 1", "is_correct": True}, {"id": 2, "text": "answer 2", "is_correct": False}, {"id": 3, "text": "answer 3", "is_correct": False}], "user_data": {"level": 0, "correct_answer": 0}, "image_path": None, "comment": None, "correct_answers": 0, "wrong_answers": 0}, {"id": 3, "text": "question 3", "answers": [{"id": 7, "text": "answer 7", "is_correct": False}], "user_data": {"level": 0, "correct_answer": 0, "comment": None}, "image_path": None, "comment": None, "correct_answers": 0, "wrong_answers": 0}], [], [], [{"id": 2, "text": "question 2", "answers": [{"id": 4, "text": "answer 4", "is_correct": False}, {"id": 5, "text": "answer 5", "is_correct": True}, {"id": 6, "text": "answer 6", "is_correct": True}], "user_data": {"level": 3, "correct_answer": 1, "comment": None}, "image_path": None, "comment": None, "correct_answers": 0, "wrong_answers": 0}], []]}
        )

        self.assertEqual(expected_result, LearningModel.create_from_quiz_model(self.quiz_model))

    def test_iteration(self):
        """Base test for iterating over questions. """
        learning_model = LearningModel.create_from_quiz_model(self.quiz_model)

        try:
            for i in range(20):
                next(learning_model)
        except BaseException as exc:
            self.fail(f"Exception occurred while iterating the learning model: {exc}")

    def test_stop_iteration(self):
        """When all the questions are on the highest level the StopIteration exception should be raised. """
        questions: List[QuestionModel] = copy.deepcopy(self.questions)
        MAX_LEVEL = 5 # TODO use common constant value
        for single_question in questions:
            single_question.user_data.level = MAX_LEVEL - 1

        quiz_model = QuizModel(id=1, name='quiz with no iterations', questions=questions)
        learning_model = LearningModel.create_from_quiz_model(quiz_model)

        with self.assertRaises(StopIteration) as err:
            next(learning_model)

        self.assertEqual('Study finished, every question is on the top level of study.', err.exception.value)
