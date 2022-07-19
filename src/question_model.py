from typing import List, Optional, Any

from pydantic import conlist, BaseModel, Field


class AnswerModel(BaseModel):
    """Answer to a question model class. """
    text: str
    is_correct: bool

    class Config:
        orm_mode = True


class QuestionModel(BaseModel):
    """Single question model class. """
    text: str
    answers: List[AnswerModel]
    progress: List[Any] = Field(default_factory=list)
    image_path: Optional[str] = Field(default=None)
    comment: Optional[str] = Field(default=None)
    user_comment: Optional[str] = Field(default=None)

    class Config:
        orm_mode = True


class QuizModel(BaseModel):
    """Class for keeping track of an item in inventory."""
    name: str
    questions: List[QuestionModel]
    description: Optional[str]
    date: Optional[str]

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


NUMBER_OF_LEVELS = 5


class LearningModel(BaseModel):
    """ There are 5 levels. At the beginning every question starts in first level.
    After defined number of tries with positive answers it is promoted to next level.
    The higher the question is, the lower probability should be that it is going to be asked. """
    # NUMBER_OF_LEVELS = 5

    learning_levels: conlist(List[LearningQuestion], min_items=NUMBER_OF_LEVELS, max_items=NUMBER_OF_LEVELS)

    def get_number_of_questions_on_levels(self) -> List[int]:
        """Get number of questions on every level """
        return [len(list_of_questions) for list_of_questions in self.learning_levels]

    def move_to_next_level(self, current_level, index) -> None:
        """Erase question from current level and add it to the next level.
        If the question is already on the highest level nothing will happen.
        """
        if current_level == NUMBER_OF_LEVELS - 1:
            return

        question = self.learning_levels[current_level].pop(index)
        self.learning_levels[current_level + 1].append(question)

    def move_to_lower_level(self, current_level, index) -> None:
        """Erase question from current level and add it to the previous level.
        If the question is already on the lowest level nothing will happen.
        """
        _lowest_level = 0
        if current_level == _lowest_level:
            return

        question = self.learning_levels[current_level].pop(index)
        self.learning_levels[current_level - 1].append(question)

    def is_anything_to_learn(self) -> bool:
        """Check if there are any question in level other than last one. """
        return any(self.learning_levels[:-1])

    @classmethod
    def create_from_quiz_model(cls, quiz_model: QuizModel): # TODO co tu dopisać zamiast LearningModel?
        """ TODO """
        return cls(learning_levels=[quiz_model.questions, [], [], [], []])

    class Config:
        orm_mode = True
