import os.path as path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import data_store_template

import Dm3Reader3_1
from BinResolution import BinResolution
from BinReader import BinReader


class DataStore(QDialog, data_store_template.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.files_path = None
        self.need_data = None
        self.store_data_on = 'RAM'
        self.label_need_data_store_text = "kB"
        self.set_parameters = False
        self.bin_resolution = None

        self.pushButton_select_files.clicked.connect(self.browse_folder)
        self.comboBox_data_store.activated[str].connect(self.change_data_store)
        self.buttonBox_data_store.accepted.connect(self.set_data_store)

        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def set_data_store(self):
        self.set_parameters = True

    def change_data_store(self, text):
        if text == 'Store data on RAM':
            self.store_data_on = 'RAM'
        elif text == 'Store data on HDD':
            self.store_data_on = 'HDD'

    def browse_folder(self):
        self.files_path = QFileDialog.getOpenFileNames(self, 'Select Files')
        self.files_path = self.files_path[0]
        if path.basename(self.files_path[0]).split(sep='.')[1] == 'dm3':
            tmp = Dm3Reader3_1.ReadDm3File(self.files_path[0])
            size = tmp.nbytes * len(self.files_path)/1000
            self.label_need_data_store.setText(str(size) + " " + self.label_need_data_store_text)

        elif path.basename(self.files_path[0]).split(sep='.')[1] == 'bin':
            self.bin_resolution = BinResolution()
            tmp = BinReader.read_bin_file(self.files_path, self.bin_resolution)
            size = tmp.nbytes * len(self.files_path)/1000
            self.label_need_data_store.setText(str(size)+" "+self.label_need_data_store_text)
