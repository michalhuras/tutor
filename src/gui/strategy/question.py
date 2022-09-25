"""TODO """
from enum import auto, Enum
from functools import partial
from typing import List

from PySide6.QtCharts import QBarSet, QChart, QChartView, QHorizontalPercentBarSeries
from PySide6.QtCore import QObject, Signal, QMargins
from PySide6.QtGui import QPainter, QColor, QColorConstants
from PySide6.QtWidgets import QVBoxLayout, QCheckBox, QWidget, QSizePolicy

from src.database.database_manager import DatabaseManager
from src.gui.common import PREVIOUS_STRATEGY
from src.gui.widgets import QuestionWidget
from src.question_model import QuestionModel, LearningModel


def blend_colors(first_color: QColor, second_color: QColor, number_of_steps: int) -> QColor:
    """Create gradient colors between two edges with defined number of steps. """
    rgba_first, rgba_last = first_color.getRgb(), second_color.getRgb()
    rgb_first, rgb_last = rgba_first[:-1], rgba_last[:-1]
    delta = [(second_element - first_element) / (number_of_steps - 1) for
             first_element, second_element in zip(rgb_first, rgb_last)]

    for index in range(number_of_steps):
        rgb_color = [int(first_element + (second_element * index)) for
                     first_element, second_element in zip(rgb_first, delta)]
        yield QColor(*rgb_color)


def create_progress_chart(levels_questions: List[int]) -> QWidget:
    """Create progress chart from the input data. """
    data_sets = [QBarSet(str(index)) for index, _ in enumerate(levels_questions)]
    [single_Set.append([value]) for single_Set, value in zip(data_sets, levels_questions)]
    [single_Set.setColor(color) for single_Set, color in
     zip(data_sets, blend_colors(QColorConstants.Red, QColorConstants.Green, len(levels_questions)))]

    series = QHorizontalPercentBarSeries()

    [series.append(single_Set) for single_Set in data_sets]

    chart = QChart()
    chart.addSeries(series)
    chart.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    chart.legend().setVisible(False)
    margins = QMargins(0, 0, 0, 0)
    chart.setMargins(margins)
    chart.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)
    chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
        progress_chart = create_progress_chart(self.question_iterator.get_number_of_questions_on_levels())
        self.widget.findChild(QVBoxLayout, 'chart_layout').addWidget(progress_chart)

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
