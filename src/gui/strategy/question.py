"""TODO """
from enum import auto, Enum
from functools import partial
from typing import List

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QVBoxLayout, QCheckBox, QWidget

from src.database.database_manager import DatabaseManager
from src.gui.common import PREVIOUS_STRATEGY
from src.gui.widgets import QuestionWidget
from src.question_model import QuestionModel, LearningModel

from PySide6.QtGui import QPainter
from PySide6.QtCharts import QBarSet, QChart, QChartView, QHorizontalPercentBarSeries


def get_me_chart() -> QWidget:

    set0 = QBarSet("Jane")
    set1 = QBarSet("Jane")
    set2 = QBarSet("Jane")
    set3 = QBarSet("Jane")
    set4 = QBarSet("Jane")

    set0.append([4])
    set1.append([5])
    set2.append([7])
    set3.append([3])
    set4.append([5])

    series = QHorizontalPercentBarSeries()
    series.append(set0)
    series.append(set1)
    series.append(set2)
    series.append(set3)
    series.append(set4)



    chart = QChart()
    chart.addSeries(series)

    # chart.setTitle("Simple percentbarchart example")
    # chart.setAnimationOptions(QChart.SeriesAnimations)

    # categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    # axis = QBarCategoryAxis()
    # axis.append(categories)
    # chart.createDefaultAxes()
    # chart.setAxisX(axis, series)
    #
    # chart.legend().setVisible(True)
    # chart.legend().setAlignment(Qt.AlignBottom)
    #
    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)

    # self.setCentralWidget()
    return chart_view


class QuestionStrategy(QObject):
    """Single question form strategy. It defines the logic behind question widget. """
    strategy_change = Signal(QObject)

    NEXT_QUESTION_LABEL = 'Next question'
    CHECK_QUESTION_LABEL = 'Check question'

    class QuestionWidgetState(Enum):
        """State of a question widget. """
        NEXT_QUESTION = auto()
        CHECK_QUESTION = auto()

    class ManageAnswer:
        def __init__(self):
            """Constructor. """
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
                    zip(range(len(self.answer_model)), self.answer_model, self.correct_answer_model)
                    if answer != correct_answer]

    def __init__(self):
        """Constructor. """
        super().__init__()

        self.quiz_name = None
        self.current_question = None
        self.widget_state = self.QuestionWidgetState.CHECK_QUESTION

        self.widget = QuestionWidget()
        self.manage_answer = self.ManageAnswer()

        self.question_iterator = None
        self.database_manager = DatabaseManager()

        self.init_gui_signals()

    def init_gui_signals(self):
        """ Initiate graphic user interface signals connections. """
        self.widget.back_btn.clicked.connect(self.back_button)
        self.widget.check_next_btn.clicked.connect(self.next_or_check_question)

    def back_button(self):
        """Action for back button clicked signal. """
        self.strategy_change.emit(PREVIOUS_STRATEGY)

    def get_widgets(self) -> QWidget:
        """ Get this strategy and sub-strategies widgets. """
        yield self.widget

    def set_quiz(self, quiz_name):
        """Set current quiz. """
        self.quiz_name = quiz_name

    def start_quiz(self):
        """TODO"""
        quiz_model = self.database_manager.get_quiz(self.quiz_name)
        self.question_iterator = LearningModel.create_from_quiz_model(quiz_model)
        self.draw_next_question()

    def draw_next_question(self):
        """Draw in widget information about next question. """
        try:
            question_model = next(self.question_iterator, None)
        except StopIteration:
            print('stop iteration!')
            # TODO write finish screen
            return

        self.widget.correct_answer_lbl.hide()
        self.widget.incorrect_answer_lbl.hide()

        self.manage_answer.new_question()
        self.current_question: QuestionModel = question_model

        self.widget.question_text_lbl.setText(question_model.text)

        self.widget.delete_subwidgets(self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout'))

        for index, answer in enumerate(question_model.answers):
            self.manage_answer.add_answer(answer.is_correct)
            answer_check_box = QCheckBox(answer.text)
            answer_check_box.clicked.connect(partial(self.manage_answer.update_answer, index))
            self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout').addWidget(answer_check_box)
        self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout').addWidget(get_me_chart())

        self.widget.check_next_btn.setText(self.CHECK_QUESTION_LABEL)
        self.widget_state = self.QuestionWidgetState.CHECK_QUESTION

    def next_or_check_question(self):
        """Action for button next or checked clicked signal.
        It runs the checking question procedure or draws next question, depending on the state in which strategy is.
        """
        if self.widget_state == self.QuestionWidgetState.CHECK_QUESTION:
            self.widget.check_next_btn.setText(self.NEXT_QUESTION_LABEL)
            self.widget_state = self.QuestionWidgetState.NEXT_QUESTION
            self.widget.disable_subwidgets(self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout'))

            self.widget.green_subwidgets_at(
                self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout'),
                [i for i in range(self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout').count())])

            if self.manage_answer.is_correct():
                self.widget.correct_answer_lbl.show()
                self.current_question.correct_answer()
                self.question_iterator.update_question(self.current_question)
            else:
                self.widget.incorrect_answer_lbl.show()
                self.widget.red_subwidgets_at(
                    self.widget.main_layout.findChild(QVBoxLayout, 'answers_layout'),
                    self.manage_answer.get_differences())
                self.current_question.incorrect_answer()
            self.database_manager.update_question_user_data(user_data_model=self.current_question.user_data,
                                                            question_id=self.current_question.id)
        elif self.widget_state == self.QuestionWidgetState.NEXT_QUESTION:
            self.widget.check_next_btn.setText(self.CHECK_QUESTION_LABEL)
            self.widget_state = self.QuestionWidgetState.CHECK_QUESTION
            self.draw_next_question()
