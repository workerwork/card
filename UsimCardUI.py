# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UsimCardUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 720)
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser_Command = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_Command.setAutoFillBackground(False)
        self.textBrowser_Command.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textBrowser_Command.setObjectName("textBrowser_Command")
        self.horizontalLayout.addWidget(self.textBrowser_Command)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_KEY = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_KEY.setMaxLength(32)
        self.lineEdit_KEY.setObjectName("lineEdit_KEY")
        self.gridLayout.addWidget(self.lineEdit_KEY, 2, 1, 1, 1)
        self.lineEdit_SPN = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_SPN.setMaxLength(16)
        self.lineEdit_SPN.setObjectName("lineEdit_SPN")
        self.gridLayout.addWidget(self.lineEdit_SPN, 6, 1, 1, 1)
        self.lineEdit_IMSI_start = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_IMSI_start.setMaxLength(15)
        self.lineEdit_IMSI_start.setObjectName("lineEdit_IMSI_start")
        self.gridLayout.addWidget(self.lineEdit_IMSI_start, 0, 1, 1, 1)
        self.lineEdit_IMSI_done = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_IMSI_done.setReadOnly(True)
        self.lineEdit_IMSI_done.setObjectName("lineEdit_IMSI_done")
        self.gridLayout.addWidget(self.lineEdit_IMSI_done, 1, 1, 1, 1)
        self.label_SPN = QtWidgets.QLabel(self.widget)
        self.label_SPN.setObjectName("label_SPN")
        self.gridLayout.addWidget(self.label_SPN, 6, 0, 1, 1)
        self.label_FPLMN = QtWidgets.QLabel(self.widget)
        self.label_FPLMN.setObjectName("label_FPLMN")
        self.gridLayout.addWidget(self.label_FPLMN, 5, 0, 1, 1)
        self.label_IMSI_start = QtWidgets.QLabel(self.widget)
        self.label_IMSI_start.setObjectName("label_IMSI_start")
        self.gridLayout.addWidget(self.label_IMSI_start, 0, 0, 1, 1)
        self.lineEdit_OPC = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_OPC.setMaxLength(32)
        self.lineEdit_OPC.setObjectName("lineEdit_OPC")
        self.gridLayout.addWidget(self.lineEdit_OPC, 3, 1, 1, 1)
        self.lineEdit_FPLMN = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_FPLMN.setMaxLength(27)
        self.lineEdit_FPLMN.setObjectName("lineEdit_FPLMN")
        self.gridLayout.addWidget(self.lineEdit_FPLMN, 5, 1, 1, 1)
        self.lineEdit_HPLMN = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_HPLMN.setText("")
        self.lineEdit_HPLMN.setMaxLength(6)
        self.lineEdit_HPLMN.setObjectName("lineEdit_HPLMN")
        self.gridLayout.addWidget(self.lineEdit_HPLMN, 4, 1, 1, 1)
        self.label_IMSI_done = QtWidgets.QLabel(self.widget)
        self.label_IMSI_done.setObjectName("label_IMSI_done")
        self.gridLayout.addWidget(self.label_IMSI_done, 1, 0, 1, 1)
        self.label_KEY = QtWidgets.QLabel(self.widget)
        self.label_KEY.setObjectName("label_KEY")
        self.gridLayout.addWidget(self.label_KEY, 2, 0, 1, 1)
        self.label_OPC = QtWidgets.QLabel(self.widget)
        self.label_OPC.setObjectName("label_OPC")
        self.gridLayout.addWidget(self.label_OPC, 3, 0, 1, 1)
        self.label_HPLMN = QtWidgets.QLabel(self.widget)
        self.label_HPLMN.setObjectName("label_HPLMN")
        self.gridLayout.addWidget(self.label_HPLMN, 4, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser_IMSI = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_IMSI.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textBrowser_IMSI.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textBrowser_IMSI.setObjectName("textBrowser_IMSI")
        self.verticalLayout_2.addWidget(self.textBrowser_IMSI)
        self.textBrowser_Log = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_Log.setMinimumSize(QtCore.QSize(256, 192))
        self.textBrowser_Log.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textBrowser_Log.setObjectName("textBrowser_Log")
        self.verticalLayout_2.addWidget(self.textBrowser_Log)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1200, 23))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuChooseMode = QtWidgets.QMenu(self.menuBar)
        self.menuChooseMode.setObjectName("menuChooseMode")
        self.menuReadCard = QtWidgets.QMenu(self.menuBar)
        self.menuReadCard.setObjectName("menuReadCard")
        self.menuWriteCard = QtWidgets.QMenu(self.menuBar)
        self.menuWriteCard.setObjectName("menuWriteCard")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLoadCommandFile = QtWidgets.QAction(MainWindow)
        self.actionLoadCommandFile.setObjectName("actionLoadCommandFile")
        self.actionLoadIMSIFile = QtWidgets.QAction(MainWindow)
        self.actionLoadIMSIFile.setObjectName("actionLoadIMSIFile")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSingle_IMSI = QtWidgets.QAction(MainWindow)
        self.actionSingle_IMSI.setCheckable(False)
        self.actionSingle_IMSI.setChecked(False)
        self.actionSingle_IMSI.setObjectName("actionSingle_IMSI")
        self.actionBatch_IMSI = QtWidgets.QAction(MainWindow)
        self.actionBatch_IMSI.setCheckable(False)
        self.actionBatch_IMSI.setObjectName("actionBatch_IMSI")
        self.actionReadCard = QtWidgets.QAction(MainWindow)
        self.actionReadCard.setObjectName("actionReadCard")
        self.actionWriteCard = QtWidgets.QAction(MainWindow)
        self.actionWriteCard.setObjectName("actionWriteCard")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionLoadCommandFile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLoadIMSIFile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuChooseMode.addAction(self.actionSingle_IMSI)
        self.menuChooseMode.addSeparator()
        self.menuChooseMode.addAction(self.actionBatch_IMSI)
        self.menuReadCard.addAction(self.actionReadCard)
        self.menuWriteCard.addAction(self.actionWriteCard)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuChooseMode.menuAction())
        self.menuBar.addAction(self.menuReadCard.menuAction())
        self.menuBar.addAction(self.menuWriteCard.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UsimWriter"))
        self.label_SPN.setText(_translate("MainWindow", "SPN(ascii)"))
        self.label_FPLMN.setText(_translate("MainWindow", "FPLMNs"))
        self.label_IMSI_start.setText(_translate("MainWindow", "IMSI_start"))
        self.label_IMSI_done.setText(_translate("MainWindow", "IMSI_done"))
        self.label_KEY.setText(_translate("MainWindow", "KEY(hex)"))
        self.label_OPC.setText(_translate("MainWindow", "OPC(hex)"))
        self.label_HPLMN.setText(_translate("MainWindow", "HPLMN"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuChooseMode.setTitle(_translate("MainWindow", "ChooseMode"))
        self.menuReadCard.setTitle(_translate("MainWindow", "ReadCard"))
        self.menuWriteCard.setTitle(_translate("MainWindow", "WriteCard"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionLoadCommandFile.setText(_translate("MainWindow", "LoadCommandFile"))
        self.actionLoadIMSIFile.setText(_translate("MainWindow", "LoadIMSIFile"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionSingle_IMSI.setText(_translate("MainWindow", "Single IMSI"))
        self.actionBatch_IMSI.setText(_translate("MainWindow", "Batch IMSI"))
        self.actionReadCard.setText(_translate("MainWindow", "ReadCard"))
        self.actionWriteCard.setText(_translate("MainWindow", "WriteCard"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
