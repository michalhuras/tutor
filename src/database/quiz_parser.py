""" Quiz txt file parser """
import re

from src.question_model import QuizModel, QuestionModel, AnswerModel


def parse_quiz_text(text: str) -> QuizModel:
    """Parse text and return quiz model structure. """
    text_lines = text.split('\n')
    text_lines = [line for line in text_lines if line]
    quiz_name = re.search(r'^## (.+?)$', text_lines[0]).group(1)
    questions = []
    question_text = ''
    answers = []
    comment = ''
    first_element = True
    image_path = None

    for line in text_lines[1:]:
        if line.startswith('####'):
            if not first_element:
                questions.append(QuestionModel(
                    text=question_text, answers=answers, image_path=image_path, comment=comment.rstrip()))
                answers = []
                comment = ''
                image_path = None
            else:
                first_element = False
            question_text = re.search(r'^#### (.+?)$', line).group(1)
        elif line.startswith('-'):
            is_correct = False
            if re.match(r'^- \[x\]', line):
                is_correct = True
            answers.append(AnswerModel(text=re.search(r'^- \[.\] (.+?)$', line).group(1), is_correct=is_correct))
        elif line.startswith('!['):
            image_path = re.search(r'^!\[.*\]\((.+?)\)$', line).group(1)
        else:
            comment += f'{line}\n'
    questions.append(QuestionModel(text=question_text, answers=answers, image_path=image_path, comment=comment.rstrip()))

    return QuizModel(name=quiz_name, questions=questions)
