# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created: Tue Jul 19 22:38:47 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(616, 583)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButtonStart = QtGui.QPushButton(self.centralwidget)
        self.pushButtonStart.setObjectName(_fromUtf8("pushButtonStart"))
        self.gridLayout_2.addWidget(self.pushButtonStart, 0, 0, 1, 1)
        self.pushButtonStop = QtGui.QPushButton(self.centralwidget)
        self.pushButtonStop.setObjectName(_fromUtf8("pushButtonStop"))
        self.gridLayout_2.addWidget(self.pushButtonStop, 0, 1, 1, 1)
        self.pushButtonStatus = QtGui.QPushButton(self.centralwidget)
        self.pushButtonStatus.setObjectName(_fromUtf8("pushButtonStatus"))
        self.gridLayout_2.addWidget(self.pushButtonStatus, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonOnline = QtGui.QPushButton(self.centralwidget)
        self.pushButtonOnline.setObjectName(_fromUtf8("pushButtonOnline"))
        self.horizontalLayout_3.addWidget(self.pushButtonOnline)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushButtonStartTimer = QtGui.QPushButton(self.centralwidget)
        self.pushButtonStartTimer.setObjectName(_fromUtf8("pushButtonStartTimer"))
        self.horizontalLayout_3.addWidget(self.pushButtonStartTimer)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.labelOnline = QtGui.QLabel(self.centralwidget)
        self.labelOnline.setObjectName(_fromUtf8("labelOnline"))
        self.verticalLayout.addWidget(self.labelOnline)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.treeWidgetChat = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidgetChat.setProperty(_fromUtf8("showDropIndicator"), False)
        self.treeWidgetChat.setAlternatingRowColors(True)
        self.treeWidgetChat.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.treeWidgetChat.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.treeWidgetChat.setIndentation(10)
        self.treeWidgetChat.setRootIsDecorated(False)
        self.treeWidgetChat.setItemsExpandable(False)
        self.treeWidgetChat.setAnimated(True)
        self.treeWidgetChat.setWordWrap(True)
        self.treeWidgetChat.setObjectName(_fromUtf8("treeWidgetChat"))
        self.verticalLayout_2.addWidget(self.treeWidgetChat)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEditMessage = QtGui.QLineEdit(self.centralwidget)
        self.lineEditMessage.setObjectName(_fromUtf8("lineEditMessage"))
        self.horizontalLayout_2.addWidget(self.lineEditMessage)
        self.pushButtonSendMessage = QtGui.QPushButton(self.centralwidget)
        self.pushButtonSendMessage.setObjectName(_fromUtf8("pushButtonSendMessage"))
        self.horizontalLayout_2.addWidget(self.pushButtonSendMessage)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_3, 3, 0, 1, 1)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.treeWidgetConsole = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidgetConsole.setAlternatingRowColors(False)
        self.treeWidgetConsole.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.treeWidgetConsole.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.treeWidgetConsole.setIndentation(10)
        self.treeWidgetConsole.setRootIsDecorated(False)
        self.treeWidgetConsole.setItemsExpandable(False)
        self.treeWidgetConsole.setWordWrap(True)
        self.treeWidgetConsole.setObjectName(_fromUtf8("treeWidgetConsole"))
        self.verticalLayout_6.addWidget(self.treeWidgetConsole)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lineEditConsole = QtGui.QLineEdit(self.centralwidget)
        self.lineEditConsole.setObjectName(_fromUtf8("lineEditConsole"))
        self.horizontalLayout_4.addWidget(self.lineEditConsole)
        self.pushButtonConsole = QtGui.QPushButton(self.centralwidget)
        self.pushButtonConsole.setObjectName(_fromUtf8("pushButtonConsole"))
        self.horizontalLayout_4.addWidget(self.pushButtonConsole)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_6, 4, 0, 1, 1)
        self.pushButtonStopStart = QtGui.QPushButton(self.centralwidget)
        self.pushButtonStopStart.setObjectName(_fromUtf8("pushButtonStopStart"))
        self.gridLayout.addWidget(self.pushButtonStopStart, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 616, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStart.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStop.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStatus.setText(QtGui.QApplication.translate("MainWindow", "Check Status", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOnline.setText(QtGui.QApplication.translate("MainWindow", "Online Players", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStartTimer.setText(QtGui.QApplication.translate("MainWindow", "Start BG Timer", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOnline.setText(QtGui.QApplication.translate("MainWindow", "Click to refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetChat.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Player Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSendMessage.setText(QtGui.QApplication.translate("MainWindow", "Refresh/Send", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetConsole.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Console", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonConsole.setText(QtGui.QApplication.translate("MainWindow", "Refresh/Send", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonStopStart.setText(QtGui.QApplication.translate("MainWindow", "Stop Server", None, QtGui.QApplication.UnicodeUTF8))

