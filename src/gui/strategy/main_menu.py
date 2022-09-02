"""TODO """
from typing import Iterator

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

from src.gui.widgets import MenuWidget


class MainMenuStrategy(QObject):
    """TODO """
    strategy_change = Signal(QObject)

    def __init__(self,
                 quiz_strategy: QObject,
                 about_program_strategy: QObject,
                 manage_quiz_strategy: QObject,
                 create_quiz_strategy: QObject):
        """TODO """
        super().__init__()

        self.widget = MenuWidget()

        self.quiz_strategy = quiz_strategy
        self.about_program_strategy = about_program_strategy
        self.manage_quiz_strategy = manage_quiz_strategy
        self.create_quiz_strategy = create_quiz_strategy

        self.init_gui_signals()

    def init_gui_signals(self):
        """ Initiate graphic user interface signals connections. """
        self.widget.about_btn.clicked.connect(self.run_about)
        self.widget.start_quiz_btn.clicked.connect(self.run_start_quiz)
        self.widget.create_quiz_btn.clicked.connect(self.run_create_new_quiz)
        self.widget.manage_quiz_btn.clicked.connect(self.run_manage_quizzes)

    def run_about(self):
        """Serve about application button action. """
        self.strategy_change.emit(self.about_program_strategy)

    def run_start_quiz(self):
        """Serve start quiz button action. """
        self.strategy_change.emit(self.quiz_strategy)

    def run_create_new_quiz(self):
        """Serve create new quiz button action. """
        self.strategy_change.emit(self.create_quiz_strategy)

    def run_manage_quizzes(self):
        """Serve manage quizzes button action. """
        self.strategy_change.emit(self.manage_quiz_strategy)

    def get_widgets(self) -> Iterator[QWidget]:
        """ Get this strategy and sub-strategies widgets. """
        yield self.widget
        yield from self.quiz_strategy.get_widgets()
        yield from self.about_program_strategy.get_widgets()
        yield from self.manage_quiz_strategy.get_widgets()
        yield from self.create_quiz_strategy.get_widgets()
