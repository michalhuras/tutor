from unittest import TestCase

from src.question_model import QuizModel, QuestionModel, AnswerModel
from src.database.quiz_parser import parse_quiz_text


class QuizParserTests(TestCase):
    """Unit tests for quiz text parsing function. """

    def test_quiz_with_one_question(self):
        """Test parsing quiz text with one question. """
        example_text ='''## Test quiz

#### Q1. What is 2 + 2?

![Q1](images/question1.png)

- [ ] 1
- [ ] 2
- [ ] 3
- [x] 4

[reference](https://www.google.com/)
'''
        expected_data = QuizModel(
            name='Test quiz',
            questions=[
                QuestionModel(
                    text='Q1. What is 2 + 2?',
                    answers=[
                        AnswerModel('1', False),
                        AnswerModel('2', False),
                        AnswerModel('3', False),
                        AnswerModel('4', True)],
                    comment='[reference](https://www.google.com/)',
                    image_path='images/question1.png')])

        self.assertEqual(expected_data, parse_quiz_text(example_text))

    def test_quiz_with_multiple_question(self):
        """Test parsing quiz text with one question. """
        example_text = '''## Test quiz

#### Q1. What is 2 + 2?

![Q1](images/question1.png)

- [ ] 1
- [ ] 2
- [ ] 3
- [x] 4

[reference](https://www.google.com/)

#### Q2. What color is a sky?

- [ ] green
- [x] blue
- [ ] pink
- [ ] dark

**example**

```
Yes, sky is blue.
```'''
        expected_data = QuizModel(
            name='Test quiz',
            questions=[
                QuestionModel(
                    text='Q1. What is 2 + 2?',
                    answers=[
                        AnswerModel('1', False),
                        AnswerModel('2', False),
                        AnswerModel('3', False),
                        AnswerModel('4', True)],
                    comment='[reference](https://www.google.com/)',
                    image_path='images/question1.png'),
                QuestionModel(
                    text='Q2. What color is a sky?',
                    answers=[
                        AnswerModel('green', False),
                        AnswerModel('blue', True),
                        AnswerModel('pink', False),
                        AnswerModel('dark', False)],
                    comment='**example**\n```\nYes, sky is blue.\n```',)
            ])

        self.assertEqual(expected_data, parse_quiz_text(example_text))
