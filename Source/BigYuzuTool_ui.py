# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BigYuzuTool.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(431, 640)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.NightlyButton = QPushButton(self.centralwidget)
        self.NightlyButton.setObjectName(u"NightlyButton")
        self.NightlyButton.setGeometry(QRect(20, 120, 391, 41))
        self.BetaButton = QPushButton(self.centralwidget)
        self.BetaButton.setObjectName(u"BetaButton")
        self.BetaButton.setGeometry(QRect(20, 170, 391, 41))
        self.WifiFixButton = QPushButton(self.centralwidget)
        self.WifiFixButton.setObjectName(u"WifiFixButton")
        self.WifiFixButton.setGeometry(QRect(20, 340, 391, 41))
        self.UninstallWifiButton = QPushButton(self.centralwidget)
        self.UninstallWifiButton.setObjectName(u"UninstallWifiButton")
        self.UninstallWifiButton.setGeometry(QRect(20, 390, 391, 41))
        self.FolderButton = QPushButton(self.centralwidget)
        self.FolderButton.setObjectName(u"FolderButton")
        self.FolderButton.setGeometry(QRect(20, 10, 381, 51))
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 90, 441, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(0, 270, 441, 20))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.BetaPatch = QPushButton(self.centralwidget)
        self.BetaPatch.setObjectName(u"BetaPatch")
        self.BetaPatch.setGeometry(QRect(20, 520, 391, 41))
        self.NightlyPatch = QPushButton(self.centralwidget)
        self.NightlyPatch.setObjectName(u"NightlyPatch")
        self.NightlyPatch.setGeometry(QRect(20, 470, 391, 41))
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(0, 440, 441, 20))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.Legacy = QPushButton(self.centralwidget)
        self.Legacy.setObjectName(u"Legacy")
        self.Legacy.setGeometry(QRect(20, 220, 391, 41))
        self.Legacy_2 = QPushButton(self.centralwidget)
        self.Legacy_2.setObjectName(u"Legacy_2")
        self.Legacy_2.setGeometry(QRect(20, 290, 391, 41))
        self.HDRVersion = QLabel(self.centralwidget)
        self.HDRVersion.setObjectName(u"HDRVersion")
        self.HDRVersion.setGeometry(QRect(20, 70, 381, 20))
        self.HDRVersion.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.FolderButton, self.NightlyButton)
        QWidget.setTabOrder(self.NightlyButton, self.BetaButton)
        QWidget.setTabOrder(self.BetaButton, self.Legacy)
        QWidget.setTabOrder(self.Legacy, self.Legacy_2)
        QWidget.setTabOrder(self.Legacy_2, self.WifiFixButton)
        QWidget.setTabOrder(self.WifiFixButton, self.UninstallWifiButton)
        QWidget.setTabOrder(self.UninstallWifiButton, self.NightlyPatch)
        QWidget.setTabOrder(self.NightlyPatch, self.BetaPatch)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.NightlyButton.setText(QCoreApplication.translate("MainWindow", u"Download Latest Nightly", None))
        self.BetaButton.setText(QCoreApplication.translate("MainWindow", u"Download Latest Beta", None))
        self.WifiFixButton.setText(QCoreApplication.translate("MainWindow", u"Install Wifi Fix", None))
        self.UninstallWifiButton.setText(QCoreApplication.translate("MainWindow", u"Uninstall Wifi Fix", None))
        self.FolderButton.setText(QCoreApplication.translate("MainWindow", u"Select Your yuzu/sdmc/ Folder", None))
        self.BetaPatch.setText(QCoreApplication.translate("MainWindow", u"Patch In Beta", None))
        self.NightlyPatch.setText(QCoreApplication.translate("MainWindow", u"Patch In Nightly", None))
        self.Legacy.setText(QCoreApplication.translate("MainWindow", u"Download Legacy Discovery", None))
        self.Legacy_2.setText(QCoreApplication.translate("MainWindow", u"Install Legacy Discovery", None))
        self.HDRVersion.setText(QCoreApplication.translate("MainWindow", u"Current HDR Version: NOT SELECTED", None))
    # retranslateUi

