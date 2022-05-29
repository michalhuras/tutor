""" Run file """
from quiz_parser import parse_quiz_text, QuizModel
from src.question_model import LearningModel

INPUT_FILE_ATH = './data/test_quiz.md'
RESULT_FILE = 'result.txt' # TODO


def get_quiz_text(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()


def get_quiz_model(file_path: str) -> QuizModel:
    return parse_quiz_text(get_quiz_text(file_path))


def run_learning(model: LearningModel) -> None:
    for question in model.learning_levels[:10]: # TODO delete [:10]
        print(question.text)
        for answer_number, answer in enumerate(question.answers):
            print(answer_number, answer)
        user_answer = input()
        if int(user_answer.strip()) == question.correct_answer:
            print('Congratulations!!!')


def run(input_file: str) -> None:
    model = get_quiz_model(input_file)
    learning_model = LearningModel.create_from_quiz_model(model)
    print('Quiz name: ', model.name)
    print('Number of questions: ', len(model.questions), '\n')
    # run_questions(model)
    run_learning(learning_model)


if __name__ == '__main__':
    run(INPUT_FILE_ATH)
