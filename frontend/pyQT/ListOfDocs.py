from PyQt5 import QtWidgets, uic, QtCore, QtNetwork
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

import sys
import json
import argparse
import collections
from json import dumps
import requests
from urllib.parse import urlparse

from qt_jsonschema_form import WidgetBuilder
import DB_client
import json_tree_widget

class ListOfDocs(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(ListOfDocs, self).__init__(parent)
        #uic.loadUi('ListOfDocs.ui', self)
        self.show()

    def fill_table(self, json_list):
        keys = ["buil_color", "integerRangeSteps"]
        labels = keys + ["ID"]
        self.setRowCount(0)
        self.setColumnCount(len(keys))
        self.setHorizontalHeaderLabels(keys)
        for doc in json_list:
            try:
                row = [doc[key] for key in keys]
            except:
                row = ["invalid document"]
            row_num=self.rowCount()
            self.insertRow(row_num)
            for column_num, v in enumerate(row):
                it = QtWidgets.QTableWidgetItem(str(v))
                #it.setFlags(it.flags() and QtCore.Qt.ItemIsEditable and QtCore.Qt.ItemIsSelectable)
                self.setItem(row_num, column_num, it)



