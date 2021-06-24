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

class TextToTreeItem:

    def __init__(self):
        self.text_list = []
        self.titem_list = []

    def append(self, text_list, titem):
        for text in text_list:
            self.text_list.append(text)
            self.titem_list.append(titem)

    # Return model indices that match string
    def find(self, find_str):

        titem_list = []
        for i, s in enumerate(self.text_list):
            if find_str in s:
                titem_list.append(self.titem_list[i])

        return titem_list


def json_tree_widget(json_data_input):
    root_item = QtWidgets.QTreeWidgetItem(["Root"])
    recurse_jdata(json_data_input, root_item)
    return(root_item)

def recurse_jdata(jdata, tree_widget):
    if isinstance(jdata, dict):
        for key, val in jdata.items():
            tree_add_row(key, val, tree_widget)
    elif isinstance(jdata, list):
        for i, val in enumerate(jdata):
            key = str(i)
            tree_add_row(key, val, tree_widget)
    else:
        print("This should never be reached!")

def tree_add_row(key, val, tree_widget):
    text_list = []

    if isinstance(val, dict) or isinstance(val, list):
        text_list.append(key)
        row_item = QtWidgets.QTreeWidgetItem([key])
        recurse_jdata(val, row_item)
    else:
        text_list.append(key)
        text_list.append(str(val))
        row_item = QtWidgets.QTreeWidgetItem([key, str(val)])

    tree_widget.addChild(row_item)
    #self.text_to_titem.append(text_list, row_item)
