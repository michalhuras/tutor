from unittest import TestCase

from src.question_model import QuizModel, QuestionModel
from src.quiz_parser import parse_quiz_text


class QuizParserTests(TestCase):
    """ TODO """
    def test_simple(self):
        """ TODO """
        example_text ='''## Test quiz

#### Q1. What is 2 + 2?

- [ ] 1
- [ ] 2
- [ ] 3
- [x] 4

[reference](https://www.google.com/)
'''
        result_data = QuizModel(name='Test quiz', questions=[QuestionModel(text='Q1. What is 2 + 2?', answers=[
            '1', '2', '3', '4'], correct_answer=3, comment='[reference](https://www.google.com/)')])

        self.assertEqual(result_data, parse_quiz_text(example_text))
