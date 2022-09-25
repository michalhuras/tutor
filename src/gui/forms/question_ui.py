# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'question.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 400)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 50, 571, 291))
        self.main_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.correct_answer_lbl = QLabel(self.verticalLayoutWidget)
        self.correct_answer_lbl.setObjectName(u"correct_answer_lbl")
        self.correct_answer_lbl.setEnabled(True)
        self.correct_answer_lbl.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.correct_answer_lbl.setFont(font)
        self.correct_answer_lbl.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.correct_answer_lbl)

        self.incorrect_answer_lbl = QLabel(self.verticalLayoutWidget)
        self.incorrect_answer_lbl.setObjectName(u"incorrect_answer_lbl")
        self.incorrect_answer_lbl.setEnabled(True)
        self.incorrect_answer_lbl.setMaximumSize(QSize(16777215, 40))
        self.incorrect_answer_lbl.setFont(font)
        self.incorrect_answer_lbl.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.incorrect_answer_lbl)

        self.question_text_lbl = QLabel(self.verticalLayoutWidget)
        self.question_text_lbl.setObjectName(u"question_text_lbl")
        self.question_text_lbl.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setPointSize(20)
        self.question_text_lbl.setFont(font1)
        self.question_text_lbl.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.question_text_lbl)

        self.answers_layout = QVBoxLayout()
        self.answers_layout.setObjectName(u"answers_layout")

        self.main_layout.addLayout(self.answers_layout)

        self.back_btn = QPushButton(Form)
        self.back_btn.setObjectName(u"back_btn")
        self.back_btn.setGeometry(QRect(10, 360, 121, 25))
        self.check_next_btn = QPushButton(Form)
        self.check_next_btn.setObjectName(u"check_next_btn")
        self.check_next_btn.setGeometry(QRect(460, 360, 121, 25))
        self.verticalLayoutWidget_2 = QWidget(Form)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(9, 9, 571, 31))
        self.chart_layout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.chart_layout.setObjectName(u"chart_layout")
        self.chart_layout.setContentsMargins(0, 0, 0, 0)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.correct_answer_lbl.setText(QCoreApplication.translate("Form", u"Correct answer!", None))
        self.incorrect_answer_lbl.setText(QCoreApplication.translate("Form", u"Incorrect answer!", None))
        self.question_text_lbl.setText(QCoreApplication.translate("Form", u"Question text", None))
        self.back_btn.setText(QCoreApplication.translate("Form", u"back", None))
        self.check_next_btn.setText(QCoreApplication.translate("Form", u"check/next", None))
    # retranslateUi

