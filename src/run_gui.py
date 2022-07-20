import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget

from src.gui.mainwindow_ui import Ui_MainWindow
from src.gui.not_implemented_ui import Ui_Form as Ui_NotImplemented


class NotImplementedWindow(QWidget, Ui_NotImplemented):
    """Functionality not implemented notifier widget. """

    def __init__(self):
        """Constructor. """
        super(NotImplementedWindow, self).__init__()
        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Main window widget. """

    def __init__(self):
        """Constructor. """
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.about_btn.clicked.connect(self.run_about)
        self.start_quiz_btn.clicked.connect(self.run_start_quiz)
        self.create_quiz_btn.clicked.connect(self.run_create_new_quiz)
        self.manage_quiz_btn.clicked.connect(self.run_manage_quizzes)

        self.window_not_implemented = NotImplementedWindow()

    def run_about(self):
        """Serve about application button action. """
        print('run about')
        self.window_not_implemented.show()

    def run_start_quiz(self):
        """Serve start quiz button action. """
        print('start quiz')
        self.window_not_implemented.show()

    def run_create_new_quiz(self):
        """Serve create new quiz button action. """
        print('create new quiz')
        self.window_not_implemented.show()

    def run_manage_quizzes(self):
        """Serve manage quizzes button action. """
        print('manage')
        self.window_not_implemented.show()


def run():
    """Main function for running application with a graphic user interface.
    It creates a QUI components and starts main event loop. """
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    run()
