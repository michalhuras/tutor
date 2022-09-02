"""TODO """
import sys

from PySide6 import QtWidgets

from src.database.database_manager import DatabaseManager
from src.gui.main_window import MainWindow
from src.gui.strategy.about_program import AboutProgramStrategy
from src.gui.strategy.create_quiz import CreateQuizStrategy
from src.gui.strategy.main_menu import MainMenuStrategy
from src.gui.strategy.manage_quiz import ManageQuizStrategy
from src.gui.strategy.quiz import QuizStrategy

QUIZ_DB_PATH = './data/quiz.db'


def run():
    """Main function for running application with a graphic user interface.
    It creates a QUI components and starts main event loop. """
    app = QtWidgets.QApplication(sys.argv)
    # initiate database manager object
    DatabaseManager(QUIZ_DB_PATH)

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
