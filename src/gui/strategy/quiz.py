"""TODO """
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

from database.database_manager import DatabaseManager
from gui.common import PREVIOUS_STRATEGY
from gui.strategy.question import QuestionStrategy
from gui.widgets import ChooseQuizWidget


class QuizStrategy(QObject):
    """Menu chose a quiz strategy class. """
    strategy_change = Signal(QObject)

    def __init__(self):
        """Constructor. """
        super().__init__()

        choose_quiz_widget = ChooseQuizWidget()
        database_manager = DatabaseManager()
        choose_quiz_widget.set_quizzes_to_chose_from(database_manager.get_quizzes_names())
        choose_quiz_widget.choose_quiz.connect(self.choose_quiz)
        self.widget = choose_quiz_widget
        self.question_strategy = QuestionStrategy()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ Initiate graphic user interface signals connections. """
        self.widget.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        """Action for back button clicked signal. """
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def choose_quiz(self, quiz_name: str):
        """ TODO """
        self.question_strategy.set_quiz(quiz_name)
        self.question_strategy.start_quiz()
        self.strategy_change.emit(self.question_strategy)

    def get_widgets(self) -> QWidget:
        """ Get this strategy and sub-strategies widgets. """
        yield self.widget
        yield from self.question_strategy.get_widgets()
