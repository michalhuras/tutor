# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'choose_quiz.ui'
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
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 571, 41))
        self.answers_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.answers_layout.setObjectName(u"answers_layout")
        self.answers_layout.setContentsMargins(0, 0, 0, 0)
        self.question_text_lbl = QLabel(self.verticalLayoutWidget)
        self.question_text_lbl.setObjectName(u"question_text_lbl")
        self.question_text_lbl.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(20)
        self.question_text_lbl.setFont(font)
        self.question_text_lbl.setAlignment(Qt.AlignCenter)

        self.answers_layout.addWidget(self.question_text_lbl)

        self.back_btn = QPushButton(Form)
        self.back_btn.setObjectName(u"back_btn")
        self.back_btn.setGeometry(QRect(460, 360, 121, 25))
        self.verticalLayoutWidget_2 = QWidget(Form)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 70, 571, 281))
        self.quizzes_layout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.quizzes_layout.setObjectName(u"quizzes_layout")
        self.quizzes_layout.setContentsMargins(0, 0, 0, 0)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.question_text_lbl.setText(QCoreApplication.translate("Form", u"Chose quiz to start", None))
        self.back_btn.setText(QCoreApplication.translate("Form", u"back", None))
    # retranslateUi

