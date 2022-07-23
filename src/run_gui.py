import sys
from enum import Enum, auto
from functools import partial
from typing import Any, Iterator, List

from PySide6 import QtWidgets
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QStackedWidget, QPushButton, QCheckBox, QVBoxLayout

from src.database.database_manager import get_quizzes_names, get_quiz
from src.gui.main_menu_ui import Ui_MainMenu
from src.gui.not_implemented_ui import Ui_Form as Ui_NotImplemented
from src.gui.question_ui import Ui_Form as Ui_Question
from src.gui.about_ui import Ui_Form as Ui_About
from src.gui.choose_quiz import Ui_Form as Ui_ChooseQuiz
from src.question_model import LearningModel, QuestionModel

MAIN_WINDOW_SIZE = (600, 400)
PREVIOUS_STRATEGY = None
QUIZ_DB_PATH = './data/quiz.db'


class NotImplementedWindow(QWidget, Ui_NotImplemented):
    """Functionality not implemented notifier widget. """

    def __init__(self):
        """Constructor. """
        super(NotImplementedWindow, self).__init__()
        self.setupUi(self)


class MenuWidget(QWidget, Ui_MainMenu):
    """Main menu widget. """

    def __init__(self, *args, **kwargs):
        """Constructor. """
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # self.window_not_implemented = NotImplementedWindow()


class QuestionWidget(QWidget, Ui_Question):
    """Main menu widget. """

    def __init__(self, *args, **kwargs):
        """Constructor. """
        super().__init__(*args, **kwargs)
        self.setupUi(self)


class ChooseQuizWidget(QWidget, Ui_ChooseQuiz):
    """Main menu widget. """
    choose_quiz = Signal(str)

    def __init__(self, *args, **kwargs):
        """Constructor. """
        super().__init__(*args, **kwargs)
        self.setupUi(self)

    def set_quizzes_to_chose_from(self, quiz_names: List[str]):
        """ Create button for every quiz name. After clicking a button signal to change widget needs to be emitted. """
        for quiz in quiz_names:
            new_button = QPushButton(quiz)
            new_button.clicked.connect(partial(self.choose_quiz_btn, quiz))
            self.quizzes_layout.addWidget(new_button)

    def choose_quiz_btn(self, quiz):
        """ TODO """
        self.choose_quiz.emit(quiz)


class AboutWidget(QWidget, Ui_About):
    """About program widget. """

    def __init__(self, *args, **kwargs):
        """Constructor. """
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.about_txt.setMarkdown(self.get_readme())

    @staticmethod
    def get_readme() -> str:
        """ Get text from readme file and put in widget's text browser.
        TODO Extract from this class.
        """
        with open('README.md') as readme_file:
            return readme_file.read()


class MainMenuStrategy(QObject):
    strategy_change = Signal(QObject)

    def __init__(self,
                 quiz_strategy: QObject,
                 about_program_strategy: QObject,
                 manage_quiz_strategy: QObject,
                 create_quiz_strategy: QObject):
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


class AboutProgramStrategy(QObject):
    """Menu chose a quiz strategy class. """
    strategy_change = Signal(QObject)

    def __init__(self):
        super().__init__()

        self.widget = AboutWidget()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ Initiate graphic user interface signals connections. """
        self.widget.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        """ Emit signal to change strategy to previous, after back button was clicked. """
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ Get this strategy and sub-strategies widgets. """
        yield self.widget


class ManageQuizStrategy(QObject):
    """Menu chose a quiz strategy class. """
    strategy_change = Signal(QObject)

    def __init__(self):
        super().__init__()

        self.widget = NotImplementedWindow()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ Initiate graphic user interface signals connections. """
        self.widget.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ Get this strategy and sub-strategies widgets. """
        yield self.widget


class CreateQuizStrategy(QObject):
    """Menu chose a quiz strategy class. """
    strategy_change = Signal(QObject)

    def __init__(self):
        """ TODO """
        super().__init__()

        self.widget = NotImplementedWindow()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ Initiate graphic user interface signals connections. """
        self.widget.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ Get this strategy and sub-strategies widgets. """
        yield self.widget


class QuestionStrategy(QObject):
    """ TODO """
    strategy_change = Signal(QObject)

    NEXT_QUESTION_LABEL = 'Next question'
    CHECK_QUESTION_LABEL = 'Check question'

    class QuestionWidgetState(Enum):
        NEXT_QUESTION = auto()
        CHECK_QUESTION = auto()

    class ManageAnswer:
        def __init__(self):
            self.answer_model = []
            self.correct_answer_model = []

        def add_answer(self, is_correct):
            self.answer_model.append(False)
            self.correct_answer_model.append(is_correct)

        def update_answer(self, index):
            self.answer_model[index] = not self.answer_model[index]

        def new_question(self):
            self.answer_model = []
            self.correct_answer_model = []

        def is_correct(self) -> bool:
            return self.answer_model == self.correct_answer_model

        def get_differences(self) -> List[int]:
            return [index for index, answer, correct_answer in
                    zip(enumerate(self.answer_model), self.answer_model, self.correct_answer_model)
                    if answer != correct_answer]

    def __init__(self):
        super().__init__()

        self.quiz_name = None
        self.current_question = None
        self.widget_state = self.QuestionWidgetState.CHECK_QUESTION

        self.widget = QuestionWidget()
        self.manage_answer = self.ManageAnswer()

        self.question_iterator = None

        self.init_gui_signals()

    def init_gui_signals(self):
        """ Initiate graphic user interface signals connections. """
        self.widget.back_btn.clicked.connect(self.back_button)
        self.widget.check_next_btn.clicked.connect(self.next_or_check_question)

    def back_button(self):
        """ TODO """
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ Get this strategy and sub-strategies widgets. """
        yield self.widget

    def set_quiz(self, quiz_name):
        """ TODO """
        self.quiz_name = quiz_name

    def start_quiz(self):
        quiz_model = get_quiz(QUIZ_DB_PATH, self.quiz_name)
        self.question_iterator = iter(quiz_model.questions)
        # TODO algorytm przechodzenia po kolejnych pytaniach
        # (iterator uwzględniający częstość to iż częście powinny pojawiać się pytania z levelu 1 niż 4)

        learning_model = LearningModel.create_from_quiz_model(quiz_model)
        # TODO learning_model - refaktoryzacja.
        self.draw_next_question()

    def draw_next_question(self):
        """ TODO """
        question_model = None
        try:
            question_model = next(self.question_iterator)
        except StopIteration:
            print('stop iteration!')
            # TODO dopisać stop iteration

        self.widget.correct_answer_lbl.hide()
        self.widget.incorrect_answer_lbl.hide()

        self.manage_answer.new_question()
        self.current_question = question_model

        self.widget.question_text_lbl.setText(question_model.text)
        for index in reversed(range(self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout').count())):
            self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout').itemAt(index).widget().deleteLater()

        for index, answer in enumerate(question_model.answers):
            self.manage_answer.add_answer(answer.is_correct)
            answer_check_box = QCheckBox(answer.text)
            answer_check_box.clicked.connect(partial(self.manage_answer.update_answer, index))
            self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout').addWidget(answer_check_box)

        self.widget.check_next_btn.setText(self.CHECK_QUESTION_LABEL)
        self.widget_state = self.QuestionWidgetState.CHECK_QUESTION

    def next_or_check_question(self):
        """ TODO """
        print('Tutaj?')
        if self.widget_state == self.QuestionWidgetState.CHECK_QUESTION:
            print('Checking question!')
            self.widget.check_next_btn.setText(self.NEXT_QUESTION_LABEL)
            self.widget_state = self.QuestionWidgetState.NEXT_QUESTION
            if self.manage_answer.is_correct():
                self.widget.correct_answer_lbl.show()
            else:
                self.widget.incorrect_answer_lbl.show()
        elif self.widget_state == self.QuestionWidgetState.NEXT_QUESTION:
            print('Next question!')
            self.widget.check_next_btn.setText(self.CHECK_QUESTION_LABEL)
            self.widget_state = self.QuestionWidgetState.CHECK_QUESTION
            self.draw_next_question()

    # TODO aktualizacja stanu nauki pytań
    # TODO odczyt z bazy danych stanu aktualnej nauki


class QuizStrategy(QObject):
    """Menu chose a quiz strategy class. """
    strategy_change = Signal(QObject)

    def __init__(self):
        super().__init__()

        choose_quiz_widget = ChooseQuizWidget()
        choose_quiz_widget.set_quizzes_to_chose_from(get_quizzes_names(QUIZ_DB_PATH))
        choose_quiz_widget.choose_quiz.connect(self.choose_quiz)
        self.widget = choose_quiz_widget
        self.question_strategy = QuestionStrategy()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ Initiate graphic user interface signals connections. """
        self.widget.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        """ TODO """
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


class MainWindow(QtWidgets.QMainWindow):
    """Main window widget. """
    # strategies = {MainMenuStrategy.widget: MainMenuStrategy}
    INITIAL_STRATEGY = MainMenuStrategy

    def __init__(self):
        """Constructor. """
        super().__init__()

        self.strategy = None
        self.current_widget = None

        self.setFixedSize(*MAIN_WINDOW_SIZE)
        self.stack_widget = QStackedWidget()
        self.setCentralWidget(self.stack_widget)

        self.last_strategy = []

    def set_strategy(self, strategy: QObject):
        """ Set current strategy. """
        if strategy == PREVIOUS_STRATEGY:
            strategy = self.last_strategy.pop()
        else:
            self.last_strategy.append(self.strategy)

        self.strategy = strategy
        self.current_widget = self.strategy.widget
        self.strategy.strategy_change.connect(self.set_strategy)

        self.stack_widget.setCurrentWidget(self.current_widget)

    def set_stack_widgets(self, widgets_iterator: Iterator):
        """ Set input widgets in a stack widget. """
        for widget in widgets_iterator:
            self.stack_widget.addWidget(widget)


def run():
    """Main function for running application with a graphic user interface.
    It creates a QUI components and starts main event loop. """
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    main_menu_strategy = MainMenuStrategy(quiz_strategy=QuizStrategy(),
                                          about_program_strategy=AboutProgramStrategy(),
                                          manage_quiz_strategy=ManageQuizStrategy(),
                                          create_quiz_strategy=CreateQuizStrategy()
                                          )
    window.set_stack_widgets(main_menu_strategy.get_widgets())
    window.set_strategy(main_menu_strategy)
    window.show()
    app.exec()


if __name__ == '__main__':
    run()
