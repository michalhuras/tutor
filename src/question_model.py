from dataclasses import dataclass, field
from typing import List, Optional

from pydantic import conlist


@dataclass
class AnswerModel:
    """Answer to a question model class. """
    text: str
    is_correct: bool


@dataclass
class QuestionModel:
    """Single question model class. """
    text: str
    answers: List[AnswerModel]
    image_path: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    user_comments: Optional[str] = field(default=None)


@dataclass
class QuizModel:
    """Class for keeping track of an item in inventory."""
    name: str
    questions: List[QuestionModel]


class LearningQuestion(QuestionModel):
    """ TODO
    There should be max 5 levels
    After 3 correct answers in a row question is upgraded to next level.
    After 3 failure answers in a row question is degraded to lower level
    """
    correct_answers: int = 0
    wrong_answers: int = 0

    def get_answer_info(self):
        """Print correct and failure answers information. """
        return f'Correct answers: {self.correct_answers}\nWrong answers: {self.wrong_answers}'

    def submit_correct_answer(self):
        """Submit correct answer. """
        self.correct_answers += 1

    def submit_wrong_answer(self):
        """Submit wrong answer. """
        self.wrong_answers += 1


NUMBER_OF_LEVELS = 5

@dataclass
class LearningModel:
    """ There are 5 levels. At the beginning every question starts in first level.
    After defined number of tries with positive answers it is promoted to next level.
    The higher the question is, the lower probability should be that it is going to be asked. """
    # NUMBER_OF_LEVELS = 5

    learning_levels: conlist(List[LearningQuestion], min_items=NUMBER_OF_LEVELS, max_items=NUMBER_OF_LEVELS)

    def get_number_of_questions_on_levels(self) -> List[int]:
        """Get number of questions on every level """
        return [len(list_of_questions) for list_of_questions in self.learning_levels]

    def upgrade_question(self, current_level, index) -> None:
        """Erase question from current level and add it to the next level.
        If the question is already on the highest level nothing will happen.
        """
        if current_level == NUMBER_OF_LEVELS - 1:
            return

        question = self.learning_levels[current_level].pop(index)
        self.learning_levels[current_level + 1].append(question)

    def move_to_next_level(self, current_level, index) -> None:
        """Erase question from current level and add it to the previous level.
        If the question is already on the lowest level nothing will happen.
        """
        _lowest_level = 0
        if current_level == _lowest_level:
            return

        question = self.learning_levels[current_level].pop(index)
        self.learning_levels[current_level - 1].append(question)

    @classmethod
    def create_from_quiz_model(cls, quiz_model: QuizModel): # TODO co tu dopisać zamiast LearningModel?
        """ TODO """
        return cls(learning_levels=[quiz_model.questions, [], [], [], []])
