# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_template.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(1029, 662)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMouseTracking(False)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.curr_image_name = QtWidgets.QTextBrowser(self.centralwidget)
        self.curr_image_name.setMaximumSize(QtCore.QSize(100, 35))
        self.curr_image_name.setObjectName("curr_image_name")
        self.verticalLayout.addWidget(self.curr_image_name)
        self.slider_image_id = QtWidgets.QSlider(self.centralwidget)
        self.slider_image_id.setMaximum(0)
        self.slider_image_id.setOrientation(QtCore.Qt.Horizontal)
        self.slider_image_id.setObjectName("slider_image_id")
        self.verticalLayout.addWidget(self.slider_image_id)
        self.move_roi = QtWidgets.QCheckBox(self.centralwidget)
        self.move_roi.setEnabled(True)
        self.move_roi.setObjectName("move_roi")
        self.verticalLayout.addWidget(self.move_roi)
        self.label_template = QtWidgets.QLabel(self.centralwidget)
        self.label_template.setMaximumSize(QtCore.QSize(100, 100))
        self.label_template.setObjectName("label_template")
        self.verticalLayout.addWidget(self.label_template)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.image_layout = QtWidgets.QHBoxLayout()
        self.image_layout.setObjectName("image_layout")
        self.horizontalLayout.addLayout(self.image_layout)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1029, 21))
        self.menubar.setMouseTracking(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuFilters = QtWidgets.QMenu(self.menubar)
        self.menuFilters.setObjectName("menuFilters")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionLoad_template = QtWidgets.QAction(MainWindow)
        self.actionLoad_template.setObjectName("actionLoad_template")
        self.actionCenter_series = QtWidgets.QAction(MainWindow)
        self.actionCenter_series.setObjectName("actionCenter_series")
        self.actionSobel = QtWidgets.QAction(MainWindow)
        self.actionSobel.setObjectName("actionSobel")
        self.actionCanny = QtWidgets.QAction(MainWindow)
        self.actionCanny.setObjectName("actionCanny")
        self.actionTesting = QtWidgets.QAction(MainWindow)
        self.actionTesting.setObjectName("actionTesting")
        self.actionLog = QtWidgets.QAction(MainWindow)
        self.actionLog.setObjectName("actionLog")
        self.actionWiener = QtWidgets.QAction(MainWindow)
        self.actionWiener.setObjectName("actionWiener")
        self.actionTesting_2 = QtWidgets.QAction(MainWindow)
        self.actionTesting_2.setObjectName("actionTesting_2")
        self.actionVirtual_image = QtWidgets.QAction(MainWindow)
        self.actionVirtual_image.setObjectName("actionVirtual_image")
        self.menuFile.addAction(self.actionOpen)
        self.menuTools.addAction(self.actionCenter_series)
        self.menuTools.addAction(self.actionVirtual_image)
        self.menuTools.addAction(self.actionTesting)
        self.menuFilters.addAction(self.actionLog)
        self.menuFilters.addAction(self.actionSobel)
        self.menuFilters.addAction(self.actionCanny)
        self.menuFilters.addAction(self.actionWiener)
        self.menuFilters.addAction(self.actionTesting_2)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuFilters.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Nanobeam electron diffraction"))
        self.move_roi.setText(_translate("MainWindow", "Move"))
        self.label_template.setText(_translate("MainWindow", "Template image"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuFilters.setTitle(_translate("MainWindow", "Filters"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionLoad_template.setText(_translate("MainWindow", "Load template"))
        self.actionCenter_series.setText(_translate("MainWindow", "Center series"))
        self.actionSobel.setText(_translate("MainWindow", "Sobel"))
        self.actionCanny.setText(_translate("MainWindow", "Canny"))
        self.actionTesting.setText(_translate("MainWindow", "Testing"))
        self.actionLog.setText(_translate("MainWindow", "Log"))
        self.actionWiener.setText(_translate("MainWindow", "Wiener"))
        self.actionTesting_2.setText(_translate("MainWindow", "Testing"))
        self.actionVirtual_image.setText(_translate("MainWindow", "Virtual image"))

