# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_store_template.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(240, 100))
        self.buttonBox_data_store = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_data_store.setGeometry(QtCore.QRect(10, 60, 221, 41))
        self.buttonBox_data_store.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_data_store.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_data_store.setObjectName("buttonBox_data_store")
        self.comboBox_data_store = QtWidgets.QComboBox(Dialog)
        self.comboBox_data_store.setGeometry(QtCore.QRect(108, 10, 121, 22))
        self.comboBox_data_store.setObjectName("comboBox_data_store")
        self.comboBox_data_store.addItem("")
        self.comboBox_data_store.addItem("")
        self.label_need_data_store = QtWidgets.QLabel(Dialog)
        self.label_need_data_store.setGeometry(QtCore.QRect(140, 40, 91, 21))
        self.label_need_data_store.setText("")
        self.label_need_data_store.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_need_data_store.setObjectName("label_need_data_store")
        self.pushButton_select_files = QtWidgets.QPushButton(Dialog)
        self.pushButton_select_files.setGeometry(QtCore.QRect(20, 10, 71, 23))
        self.pushButton_select_files.setObjectName("pushButton_select_files")

        self.retranslateUi(Dialog)
        self.buttonBox_data_store.accepted.connect(Dialog.accept)
        self.buttonBox_data_store.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.comboBox_data_store.setItemText(0, _translate("Dialog", "Store data on RAM"))
        self.comboBox_data_store.setItemText(1, _translate("Dialog", "Store data on HDD"))
        self.pushButton_select_files.setText(_translate("Dialog", "Select files"))

