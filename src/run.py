""" Run file """
from src.database.database_manager import get_quizzes
from src.database.quiz_parser import parse_quiz_text, QuizModel
from src.question_model import LearningModel

QUIZ_DB_PATH = './data/quiz.db'


def get_quiz_text(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()


def get_quiz_model(file_path: str) -> QuizModel:
    return parse_quiz_text(get_quiz_text(file_path))


def run_learning(model: LearningModel) -> None:
    """WIP: IT is only a draft of a concept how this function should work.
    There are a few learning steps in a learning model. This function runs question from each of them.
    If question is answered correctly it is being moved to next level.
    """
    for level_number, level in enumerate(model.learning_levels[:-1]):
        print(f'Questions from level {level_number}')
        for question in level:
            print(question.text)
            correct_answer_number = 0
            for answer_number, answer in enumerate(question.answers, 1):
                print(answer_number, answer.text)
                if answer.is_correct:
                    correct_answer_number = answer_number
            user_answer = input()
            if int(user_answer.strip()) == correct_answer_number:
                print('Correct answer! \n')
                model.move_to_next_level(level_number, level.index(question))
            else:
                print('Wrong answer :( \n')
                model.move_to_lower_level(level_number, level.index(question))
    if model.is_anything_to_learn():
        run_learning(model)


def run(input_file: str) -> None:
    model = get_quizzes(input_file)[0] # For now run only first quiz
    learning_model = LearningModel.create_from_quiz_model(model)
    print('Quiz name: ', model.name)
    print('Number of questions: ', len(model.questions), '\n')
    # run_questions(model)
    run_learning(learning_model)


if __name__ == '__main__':
    run(QUIZ_DB_PATH)
