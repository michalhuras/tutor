# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu.ui'
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

class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        if not MainMenu.objectName():
            MainMenu.setObjectName(u"MainMenu")
        MainMenu.resize(600, 400)
        self.verticalLayoutWidget = QWidget(MainMenu)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setEnabled(True)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 601, 401))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalLayoutWidget.sizePolicy().hasHeightForWidth())
        self.verticalLayoutWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tutor_label = QLabel(self.verticalLayoutWidget)
        self.tutor_label.setObjectName(u"tutor_label")
        self.tutor_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(20)
        self.tutor_label.setFont(font)
        self.tutor_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.tutor_label)

        self.about_btn = QPushButton(self.verticalLayoutWidget)
        self.about_btn.setObjectName(u"about_btn")
        self.about_btn.setEnabled(True)
        sizePolicy.setHeightForWidth(self.about_btn.sizePolicy().hasHeightForWidth())
        self.about_btn.setSizePolicy(sizePolicy)
        self.about_btn.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.about_btn)

        self.start_quiz_btn = QPushButton(self.verticalLayoutWidget)
        self.start_quiz_btn.setObjectName(u"start_quiz_btn")
        sizePolicy.setHeightForWidth(self.start_quiz_btn.sizePolicy().hasHeightForWidth())
        self.start_quiz_btn.setSizePolicy(sizePolicy)
        self.start_quiz_btn.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.start_quiz_btn)

        self.create_quiz_btn = QPushButton(self.verticalLayoutWidget)
        self.create_quiz_btn.setObjectName(u"create_quiz_btn")
        sizePolicy.setHeightForWidth(self.create_quiz_btn.sizePolicy().hasHeightForWidth())
        self.create_quiz_btn.setSizePolicy(sizePolicy)
        self.create_quiz_btn.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.create_quiz_btn)

        self.manage_quiz_btn = QPushButton(self.verticalLayoutWidget)
        self.manage_quiz_btn.setObjectName(u"manage_quiz_btn")
        sizePolicy.setHeightForWidth(self.manage_quiz_btn.sizePolicy().hasHeightForWidth())
        self.manage_quiz_btn.setSizePolicy(sizePolicy)
        self.manage_quiz_btn.setMaximumSize(QSize(16777215, 40))

        self.verticalLayout.addWidget(self.manage_quiz_btn)


        self.retranslateUi(MainMenu)

        QMetaObject.connectSlotsByName(MainMenu)
    # setupUi

    def retranslateUi(self, MainMenu):
        MainMenu.setWindowTitle(QCoreApplication.translate("MainMenu", u"Form", None))
        self.tutor_label.setText(QCoreApplication.translate("MainMenu", u"Tutor", None))
        self.about_btn.setText(QCoreApplication.translate("MainMenu", u"About application", None))
        self.start_quiz_btn.setText(QCoreApplication.translate("MainMenu", u"Start quiz", None))
        self.create_quiz_btn.setText(QCoreApplication.translate("MainMenu", u"Create new quiz", None))
        self.manage_quiz_btn.setText(QCoreApplication.translate("MainMenu", u"Manage quizes", None))
    # retranslateUi

