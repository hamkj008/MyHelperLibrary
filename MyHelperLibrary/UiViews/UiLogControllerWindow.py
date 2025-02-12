# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LogControllerWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStackedWidget, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_LogControllerWindow(object):
    def setupUi(self, LogControllerWindow):
        if not LogControllerWindow.objectName():
            LogControllerWindow.setObjectName(u"LogControllerWindow")
        LogControllerWindow.resize(800, 600)
        self.centralwidget = QWidget(LogControllerWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout = QVBoxLayout(self.page_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stackedWidget)

        LogControllerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(LogControllerWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        LogControllerWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(LogControllerWindow)
        self.statusbar.setObjectName(u"statusbar")
        LogControllerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LogControllerWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(LogControllerWindow)
    # setupUi

    def retranslateUi(self, LogControllerWindow):
        LogControllerWindow.setWindowTitle(QCoreApplication.translate("LogControllerWindow", u"MainWindow", None))
    # retranslateUi

