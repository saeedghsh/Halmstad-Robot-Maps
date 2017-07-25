# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_keypoint.ui'
#
# Created: Tue Jul 25 19:15:40 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1569, 1084)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_load_map = QtGui.QPushButton(self.centralwidget)
        self.pushButton_load_map.setGeometry(QtCore.QRect(10, 1000, 70, 27))
        self.pushButton_load_map.setObjectName("pushButton_load_map")
        self.textEdit_file_path = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_file_path.setGeometry(QtCore.QRect(90, 1000, 660, 30))
        self.textEdit_file_path.setReadOnly(False)
        self.textEdit_file_path.setObjectName("textEdit_file_path")
        self.pushButton_next = QtGui.QPushButton(self.centralwidget)
        self.pushButton_next.setGeometry(QtCore.QRect(830, 1000, 70, 27))
        self.pushButton_next.setObjectName("pushButton_next")
        self.pushButton_previous = QtGui.QPushButton(self.centralwidget)
        self.pushButton_previous.setGeometry(QtCore.QRect(760, 1000, 70, 27))
        self.pushButton_previous.setObjectName("pushButton_previous")
        self.graphicsView_map = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView_map.setGeometry(QtCore.QRect(10, 10, 1551, 981))
        self.graphicsView_map.setObjectName("graphicsView_map")
        self.pushButton_save = QtGui.QPushButton(self.centralwidget)
        self.pushButton_save.setEnabled(True)
        self.pushButton_save.setGeometry(QtCore.QRect(1490, 1000, 70, 27))
        self.pushButton_save.setObjectName("pushButton_save")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(960, 1010, 250, 14))
        self.label.setText("")
        self.label.setObjectName("label")
        self.checkBox_save_with_nxt_prv = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_save_with_nxt_prv.setGeometry(QtCore.QRect(910, 1000, 271, 21))
        self.checkBox_save_with_nxt_prv.setChecked(True)
        self.checkBox_save_with_nxt_prv.setObjectName("checkBox_save_with_nxt_prv")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1569, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_load_map.setText(QtGui.QApplication.translate("MainWindow", "Load Map", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_next.setText(QtGui.QApplication.translate("MainWindow", "Next>>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_previous.setText(QtGui.QApplication.translate("MainWindow", "<< Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_save.setText(QtGui.QApplication.translate("MainWindow", "save", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_save_with_nxt_prv.setText(QtGui.QApplication.translate("MainWindow", "Save results with \"Next\" and \"Previous\" buttons", None, QtGui.QApplication.UnicodeUTF8))

