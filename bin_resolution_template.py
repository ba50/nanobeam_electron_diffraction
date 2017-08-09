# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bin_resolution_template.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(175, 195)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(175, 195))
        self.buttonBox_set_resolution = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_set_resolution.setGeometry(QtCore.QRect(60, 160, 101, 31))
        self.buttonBox_set_resolution.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_set_resolution.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_set_resolution.setObjectName("buttonBox_set_resolution")
        self.lineEdit_width = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_width.setGeometry(QtCore.QRect(130, 10, 31, 20))
        self.lineEdit_width.setProperty("tabletTracking", False)
        self.lineEdit_width.setObjectName("lineEdit_width")
        self.lineEdit_height = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_height.setGeometry(QtCore.QRect(130, 40, 31, 20))
        self.lineEdit_height.setObjectName("lineEdit_height")
        self.lineEdit_offset = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_offset.setGeometry(QtCore.QRect(130, 100, 31, 20))
        self.lineEdit_offset.setObjectName("lineEdit_offset")
        self.comboBox_type = QtWidgets.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(90, 130, 69, 22))
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 10, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 100, 47, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 130, 47, 13))
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 70, 47, 13))
        self.label_3.setObjectName("label_3")
        self.lineEdit_z = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_z.setGeometry(QtCore.QRect(130, 70, 31, 20))
        self.lineEdit_z.setObjectName("lineEdit_z")

        self.retranslateUi(Dialog)
        self.buttonBox_set_resolution.accepted.connect(Dialog.accept)
        self.buttonBox_set_resolution.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEdit_width, self.lineEdit_height)
        Dialog.setTabOrder(self.lineEdit_height, self.lineEdit_z)
        Dialog.setTabOrder(self.lineEdit_z, self.lineEdit_offset)
        Dialog.setTabOrder(self.lineEdit_offset, self.comboBox_type)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.comboBox_type.setItemText(0, _translate("Dialog", "int16"))
        self.comboBox_type.setItemText(1, _translate("Dialog", "int32"))
        self.comboBox_type.setItemText(2, _translate("Dialog", "float32"))
        self.label.setText(_translate("Dialog", "X"))
        self.label_2.setText(_translate("Dialog", "Y"))
        self.label_4.setText(_translate("Dialog", "offset"))
        self.label_5.setText(_translate("Dialog", "type"))
        self.label_3.setText(_translate("Dialog", "Z"))

