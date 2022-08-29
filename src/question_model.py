"""Data models. """
import random
from typing import List, Optional, ClassVar

from pydantic import conlist, BaseModel, Field


class AnswerModel(BaseModel):
    """Answer to a question model class. """
    id: Optional[int]
    text: str
    is_correct: bool

    class Config:
        """Configuration set for a model class. """
        orm_mode = True


MAX_LEVEL = 5 # TODO


class QuestionUserDataModel(BaseModel):
    """ Question progress model class. """
    level: int = Field(default_factory=lambda: 0, ge=0, lt=MAX_LEVEL)
    correct_answer: int = 0
    comment: Optional[str]

    class Config:
        """Configuration set for a model class. """
        orm_mode = True


# Correct answers needed to move question to the next level
NEEDED_CORRECT_ANSWERS: List[int] = [3, 4, 5, 6]
NUMBER_OF_LEVELS = 5


class QuestionModel(BaseModel):
    """Single question model class. """
    id: Optional[int]
    text: str
    answers: List[AnswerModel]
    user_data: Optional[QuestionUserDataModel] = Field(default=None)
    image_path: Optional[str] = Field(default=None)
    comment: Optional[str] = Field(default=None)

    class Config:
        """Configuration set for a model class. """
        orm_mode = True

    def correct_answer(self) -> None:
        """React on a correct answer. Increase number of correct answers and if it is needed move to next level. """
        if self.user_data.level == NUMBER_OF_LEVELS - 1:
            return

        self.user_data.correct_answer += 1
        if self.user_data.correct_answer >= NEEDED_CORRECT_ANSWERS[self.user_data.level]:
            self.user_data.correct_answer = 0
            old_level = self.user_data.level
            self.user_data.level = old_level + 1

    def incorrect_answer(self) -> None:
        """React to an incorrect answer. Zero the number of correct answers. """
        self.user_data.correct_answer = 0


class QuizModel(BaseModel):
    """Class for keeping track of an item in inventory."""
    id: Optional[int]
    name: str
    questions: List[QuestionModel]
    description: Optional[str]
    date: Optional[str]

    class Config:
        """Configuration set for a model class. """
        orm_mode = True


class LearningModel(BaseModel):
    """ There are 5 levels. At the beginning every question starts in first level.
    After defined number of tries with positive answers it is promoted to next level.
    The higher the question is, the lower probability should be that it is going to be asked. """
    NUMBER_OF_LEVELS: ClassVar[int] = 5
    learning_levels: conlist(List[QuestionModel], min_items=NUMBER_OF_LEVELS, max_items=NUMBER_OF_LEVELS)

    def __iter__(self):
        """Return iterator - self. """
        return self

    def __next__(self):
        """Get next question to iterate. Draw a learning level to chose question from, next choose question from it. """
        questions_on_levels = self.get_number_of_questions_on_levels()
        if not self.is_anything_to_learn():
            raise StopIteration('Study finished, every question is on the top level of study.')
        levels_probability = [0.5, 0.3, 0.1, 0.07, 0.03]

        level_contain_elements = [1 if len(level) else 0 for level in self.learning_levels]
        levels_probability_not_empty = \
            [multiplier * multiplicand for multiplier, multiplicand in zip(levels_probability, level_contain_elements)]
        choose_level = self.learning_levels[random.choices([i for i in range(self.NUMBER_OF_LEVELS)],
                                                           weights=levels_probability_not_empty)[0]]

        try:
            question = random.choice(choose_level)
        except IndexError:
            return next(self)
        return question

    def get_number_of_questions_on_levels(self) -> List[int]:
        """Get number of questions on every level """
        return [len(list_of_questions) for list_of_questions in self.learning_levels]

    def update_question(self, question: QuestionModel) -> None:
        """Update level of the question if it is needed. """
        if question not in self.learning_levels[question.user_data.level]:
            self.learning_levels[question.user_data.level - 1].remove(question)
            self.learning_levels[question.user_data.level].append(question)

    def is_anything_to_learn(self) -> bool:
        """Check if there are any question in level other than last one. """
        return any(self.learning_levels[:-1])

    @classmethod
    def create_from_quiz_model(cls, quiz_model: QuizModel):
        """Create class instance with initial data from quiz model. """
        learning_levels = [[] for _ in range(cls.NUMBER_OF_LEVELS)]
        for question in quiz_model.questions:
            if question.user_data:
                learning_levels[question.user_data.level].append(question)
            else:
                question.user_data = QuestionUserDataModel()
                learning_levels[0].append(question.user_data)
                # TODO currently if in the quiz is a question without the user data, a exception is raised.
        return cls(learning_levels=learning_levels)

    class Config:
        """Configuration set for a model class. """
        orm_mode = True
