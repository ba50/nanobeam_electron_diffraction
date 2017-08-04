# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'virtual_image_resolution_template.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(175, 125)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(175, 125))
        self.buttonBox_set_resolution = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_set_resolution.setGeometry(QtCore.QRect(60, 90, 101, 31))
        self.buttonBox_set_resolution.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_set_resolution.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_set_resolution.setObjectName("buttonBox_set_resolution")
        self.lineEdit_width = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_width.setGeometry(QtCore.QRect(130, 10, 31, 20))
        self.lineEdit_width.setObjectName("lineEdit_width")
        self.lineEdit_height = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_height.setGeometry(QtCore.QRect(130, 40, 31, 20))
        self.lineEdit_height.setObjectName("lineEdit_height")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 10, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 47, 13))
        self.label_2.setObjectName("label_2")
        self.lineEdit_threads = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_threads.setGeometry(QtCore.QRect(130, 70, 31, 20))
        self.lineEdit_threads.setObjectName("lineEdit_threads")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 70, 47, 13))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        self.buttonBox_set_resolution.accepted.connect(Dialog.accept)
        self.buttonBox_set_resolution.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "X"))
        self.label_2.setText(_translate("Dialog", "Y"))
        self.label_3.setText(_translate("Dialog", "Threads"))

