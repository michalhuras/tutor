"""TODO"""
from functools import partial
from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from gui.forms.main_menu_ui import Ui_MainMenu
from gui.forms.not_implemented_ui import Ui_Form as Ui_NotImplemented
from gui.forms.question_ui import Ui_Form as Ui_Question
from gui.forms.about_ui import Ui_Form as Ui_About
from gui.forms.choose_quiz import Ui_Form as Ui_ChooseQuiz


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

    @staticmethod
    def delete_subwidgets(owner: QVBoxLayout):
        """Delete owner subwidgets. Used especially to delete a layout checkboxes. """
        [owner.itemAt(index).widget().deleteLater() for index in reversed(range(owner.count()))]

    @staticmethod
    def disable_subwidgets(owner: QVBoxLayout):
        """Disable owner subwidgets. Used especially to disable a layout checkboxes. """
        [owner.itemAt(index).widget().setEnabled(False) for index in range(owner.count())]

    @staticmethod
    def red_subwidgets_at(owner: QVBoxLayout, positions: List[int]):
        """Set red color for subwidgets at a specified positions. """
        [owner.itemAt(index).widget().setStyleSheet("color: red; font-weight: bold;") for index in positions]

    @staticmethod
    def green_subwidgets_at(owner: QVBoxLayout, positions: List[int]):
        """Set green color for subwidgets at a specified positions. """
        [owner.itemAt(index).widget().setStyleSheet("color: green") for index in positions]


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
        """Action for choosing one of quizzes. It emits a signal that changes main widget. """
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
