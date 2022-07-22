import sys
from typing import Any, Iterator

from PySide6 import QtWidgets
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QStackedWidget

from src.gui.main_menu_ui import Ui_MainMenu
from src.gui.not_implemented_ui import Ui_Form as Ui_NotImplemented
from src.gui.question_ui import Ui_Form as Ui_Question
from src.gui.about_ui import Ui_Form as Ui_About

MAIN_WINDOW_SIZE = (600, 400)
PREVIOUS_STRATEGY = None


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
        """TODO"""
        self.widget.about_btn.clicked.connect(self.run_about)
        self.widget.start_quiz_btn.clicked.connect(self.run_start_quiz)
        self.widget.create_quiz_btn.clicked.connect(self.run_create_new_quiz)
        self.widget.manage_quiz_btn.clicked.connect(self.run_manage_quizzes)

    def run_about(self):
        """Serve about application button action. """
        print('run about')
        self.strategy_change.emit(self.about_program_strategy)

    def run_start_quiz(self):
        """Serve start quiz button action. """
        print('start quiz')
        self.strategy_change.emit(self.quiz_strategy)

    def run_create_new_quiz(self):
        """Serve create new quiz button action. """
        print('create new quiz')
        self.strategy_change.emit(self.create_quiz_strategy)

    def run_manage_quizzes(self):
        """Serve manage quizzes button action. """
        print('manage')
        self.strategy_change.emit(self.manage_quiz_strategy)

    def get_widgets(self) -> Iterator[QWidget]:
        """ TODO """
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
        """ TODO """
        self.widget.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ TODO """
        yield self.widget


class ManageQuizStrategy(QObject):
    """Menu chose a quiz strategy class. """
    strategy_change = Signal(QObject)

    def __init__(self):
        super().__init__()

        self.widget = NotImplementedWindow()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ TODO """
        self.widget.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ TODO """
        yield self.widget


class CreateQuizStrategy(QObject):
    """Menu chose a quiz strategy class. """
    strategy_change = Signal(QObject)

    def __init__(self):
        super().__init__()

        self.widget = NotImplementedWindow()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ TODO """
        self.widget.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ TODO """
        yield self.widget


class QuizStrategy(QObject):
    """Menu chose a quiz strategy class. """
    strategy_change = Signal(QObject)

    def __init__(self):
        super().__init__()

        self.widget = NotImplementedWindow()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ TODO """
        self.widget.back_btn.clicked.connect(self.back_button)

    def back_button(self):
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ TODO """
        yield self.widget


class QuestionStrategy(QObject):
    """ TODO """
    strategy_change = Signal(QObject)

    def __init__(self):
        super().__init__()

        self.widget = NotImplementedWindow()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ TODO """
        self.widget.about_btn.clicked.connect(self.back_button)

    def back_button(self):
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ TODO """
        print('QuestionStrategy get_widgets')
        yield self.widget


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
        """TODO"""
        if strategy == PREVIOUS_STRATEGY:
            strategy = self.last_strategy.pop()
        else:
            self.last_strategy.append(self.strategy)

        self.strategy = strategy
        self.current_widget = self.strategy.widget
        self.strategy.strategy_change.connect(self.set_strategy)

        self.stack_widget.setCurrentWidget(self.current_widget)
        # self.current_widget.show()
        # self.setCentralWidget(self.current_widget)

    def set_stack_widgets(self, widgets_iterator: Iterator):
        """ TODO """
        print('set_stack_widgets')
        for widget in widgets_iterator:
            print(widget)
            self.stack_widget.addWidget(widget)


def run():
    """Main function for running application with a graphic user interface.
    It creates a QUI components and starts main event loop. """
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    main_menu_strategies = {
        'quiz_strategy': QuizStrategy(),
        'about_program_strategy': AboutProgramStrategy(),
        'manage_quiz_strategy': ManageQuizStrategy(),
        'create_quiz_strategy': CreateQuizStrategy()
    }
    main_menu_strategy = MainMenuStrategy(**main_menu_strategies)
    window.set_stack_widgets(main_menu_strategy.get_widgets())
    window.set_strategy(main_menu_strategy)
    window.show()
    app.exec()


if __name__ == '__main__':
    run()
