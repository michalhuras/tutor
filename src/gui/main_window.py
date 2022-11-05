"""TODO """
from typing import Iterator

from PySide6 import QtWidgets
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QStackedWidget

from gui.common import PREVIOUS_STRATEGY
from gui.strategy.main_menu import MainMenuStrategy

MAIN_WINDOW_SIZE = (600, 400)


class MainWindow(QtWidgets.QMainWindow):
    """Main window widget. """
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
        self.last_strategy.append(self.strategy)
        self.strategy = strategy
        self.current_widget = self.strategy.widget
        self.strategy.strategy_change.connect(self.set_strategy)

        self.stack_widget.setCurrentWidget(self.current_widget)

    def set_stack_widgets(self, widgets_iterator: Iterator):
        """ Set input widgets in a stack widget. """
        for widget in widgets_iterator:
            self.stack_widget.addWidget(widget)
