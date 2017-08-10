# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'virtual_image_plot_template.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_virtual_image_plot(object):
    def setupUi(self, Dialog_virtual_image_plot):
        Dialog_virtual_image_plot.setObjectName("Dialog_virtual_image_plot")
        Dialog_virtual_image_plot.resize(615, 561)
        self.gridLayout = QtWidgets.QGridLayout(Dialog_virtual_image_plot)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_update_plot = QtWidgets.QPushButton(Dialog_virtual_image_plot)
        self.pushButton_update_plot.setObjectName("pushButton_update_plot")
        self.gridLayout.addWidget(self.pushButton_update_plot, 0, 0, 1, 1)
        self.image_layout = QtWidgets.QGridLayout()
        self.image_layout.setObjectName("image_layout")
        self.gridLayout.addLayout(self.image_layout, 1, 0, 1, 2)

        self.retranslateUi(Dialog_virtual_image_plot)
        QtCore.QMetaObject.connectSlotsByName(Dialog_virtual_image_plot)

    def retranslateUi(self, Dialog_virtual_image_plot):
        _translate = QtCore.QCoreApplication.translate
        Dialog_virtual_image_plot.setWindowTitle(_translate("Dialog_virtual_image_plot", "Virtual Image Plot"))
        self.pushButton_update_plot.setText(_translate("Dialog_virtual_image_plot", "Update plot"))

