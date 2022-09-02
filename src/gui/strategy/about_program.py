"""TODO """
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

from src.gui.common import PREVIOUS_STRATEGY
from src.gui.widgets import AboutWidget


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
