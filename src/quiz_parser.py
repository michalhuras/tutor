""" TODO """
import re

from src.question_model import QuizModel, QuestionModel


def parse_quiz_text(text: str) -> QuizModel:
    text_lines = text.split('\n')
    text_lines = [line for line in text_lines if line]
    quiz_name = re.search(r'^## (.+?)$', text_lines[0]).group(1)
    questions = []
    question_text = ''
    answers = []
    correct_answer = 0
    comment = ''
    first_element = True

    for line in text_lines[1:]:
        if line.startswith('####'):
            if not first_element:
                questions.append(QuestionModel(question_text, answers, correct_answer, comment))
                answers = []
            else:
                first_element = False
            question_text = re.search(r'^#### (.+?)$', line).group(1)
        elif line.startswith('-'):
            answers.append(re.search(r'^- \[.\] (.+?)$', line).group(1))
            if line.startswith('- [x]'):
                correct_answer = len(answers) - 1
        else:
            comment = line
    questions.append(QuestionModel(question_text, answers, correct_answer, comment))

    return QuizModel(quiz_name, questions)
