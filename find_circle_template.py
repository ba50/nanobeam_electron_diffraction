# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'find_circle_template.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(175, 190)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(175, 190))
        self.buttonBox_set_resolution = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_set_resolution.setGeometry(QtCore.QRect(60, 160, 101, 31))
        self.buttonBox_set_resolution.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_set_resolution.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_set_resolution.setObjectName("buttonBox_set_resolution")
        self.lineEdit_minDist = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_minDist.setGeometry(QtCore.QRect(130, 10, 31, 20))
        self.lineEdit_minDist.setObjectName("lineEdit_minDist")
        self.lineEdit_param1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_param1.setGeometry(QtCore.QRect(130, 40, 31, 20))
        self.lineEdit_param1.setObjectName("lineEdit_param1")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 10, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 47, 13))
        self.label_2.setObjectName("label_2")
        self.lineEdit_param2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_param2.setGeometry(QtCore.QRect(130, 70, 31, 20))
        self.lineEdit_param2.setObjectName("lineEdit_param2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 70, 71, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 100, 71, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_minRadius = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_minRadius.setGeometry(QtCore.QRect(130, 100, 31, 20))
        self.lineEdit_minRadius.setObjectName("lineEdit_minRadius")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 130, 71, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit_maxRadius = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_maxRadius.setGeometry(QtCore.QRect(130, 130, 31, 20))
        self.lineEdit_maxRadius.setObjectName("lineEdit_maxRadius")

        self.retranslateUi(Dialog)
        self.buttonBox_set_resolution.accepted.connect(Dialog.accept)
        self.buttonBox_set_resolution.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Image Resolution"))
        self.label.setText(_translate("Dialog", "minDist"))
        self.label_2.setText(_translate("Dialog", "param1"))
        self.label_3.setText(_translate("Dialog", "param2"))
        self.label_4.setText(_translate("Dialog", "minRadius"))
        self.label_5.setText(_translate("Dialog", "maxRadius"))

