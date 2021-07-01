from PyQt5 import QtWidgets, uic, QtCore, QtNetwork
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

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
import ListOfDocs

class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('pyQT_client.ui', self)
        self.dbClient = DB_client.DB_client()

        self.json_data = {}

        self.urlWidget = self.findChild(QtWidgets.QLineEdit, 'urlEdit')
        self.dbClient.LoadBDschema(self.urlWidget.text())

        self.button = self.findChild(QtWidgets.QPushButton, 'selectSchema')
        self.button.clicked.connect(self.selectSchemaButtonPressed)

        self.buttonJE = self.findChild(QtWidgets.QPushButton, 'editJSON')
        self.buttonJE.clicked.connect(self.editJSONPressed)

        self.buttonnewDoc = self.findChild(QtWidgets.QPushButton, 'newDocButton')
        self.buttonnewDoc.clicked.connect(self.editJSONPressed)

        self.buttonPOST = self.findChild(QtWidgets.QPushButton, 'postJSON')
        self.buttonPOST.clicked.connect( self.buttonPOSTpressed)

        self.buttonShowJSON = self.findChild(QtWidgets.QPushButton, 'showJSON')
        self.buttonShowJSON.clicked.connect(self.ShowJSONPressed)

        self.buttonLoadJSON = self.findChild(QtWidgets.QPushButton, 'loadJSON')
        self.buttonLoadJSON.clicked.connect(self.LoadJSONPressed)

        self.buttonListOfDocs = self.findChild(QtWidgets.QPushButton, 'ListofDocs')
        self.buttonListOfDocs.clicked.connect(self.ShowListOfDocs)

        self.buttonLoadBDschema = self.findChild(QtWidgets.QPushButton, 'loadDBschema')
        self.buttonLoadBDschema.clicked.connect(lambda: self.dbClient.LoadBDschema(self.urlWidget.text()))

        self.listofDocs = ListOfDocs.ListOfDocs()
        self.layoutlistofDocs = self.findChild(QtWidgets.QVBoxLayout, 'listofDocs')
        self.layoutlistofDocs.addWidget(self.listofDocs)

        self.timer=QTimer()
        self.timer.timeout.connect(self.TimerForListOfDocs)
        self.timer.start(500)

        self.tabDocEditor = self.findChild(QtWidgets.QTabWidget, 'tabDocEdit')

        self.show()

    def TimerForListOfDocs(self):
        self.ShowListOfDocs()
        self.timer.start(5000)

    def buttonPOSTpressed(self):
        self.dbClient.postJSON(self.urlWidget.text(), self.json_data)
        self.ShowListOfDocs()

    def on_json_data_change(self,d):
        print(d)
        self.json_data = d
        #self.ShowJSON(self.json_data)

    def ShowJSONPressed(self):
        self.ShowJSON(self.json_data)

    def LoadJSONPressed(self):
        self.json_data = self.dbClient.loadJSON(self.urlWidget.text())
        self.ShowJSON(self.json_data)

    def ShowJSON(self, json_data_input):
        self.tree_widget.clear()
        self.tree_widget.setHeaderLabels(["Key", "Value"])
        self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tree_widget.addTopLevelItem(json_tree_widget.json_tree_widget(json_data_input))
        self.tree_widget.show()

    def ShowListOfDocs(self):
        self.json_list_local = self.dbClient.loadJSON(self.urlWidget.text())
        self.listofDocs.fill_table(self.json_list_local)
        self.listofDocs.cellPressed.connect(self.cell_Pressed)

    def cell_Pressed(self, row, column):
        print(row, column)
        url = self.urlWidget.text()+'/'+self.json_list_local[row]["_id"]["$oid"]
        self.json_data = self.dbClient.loadJSON(url)
        self.editJSONPressed()


    def selectSchemaButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Load JSON scheme file", "","All Files (*);;JSON schema files (*.json)", options=options)
        if fileName:
            self.jsonschemafile = self.findChild(QtWidgets.QPlainTextEdit, 'jsonschemafile')
            self.jsonschemafile.setPlainText(fileName)
        jfile = open(fileName)
        self.schema = json.load(jfile, object_pairs_hook=collections.OrderedDict)

    def editJSONPressed(self):
        builder = WidgetBuilder()
        ui_schema = {
            "buil_color": {
                "ui:widget": "colour"
            },
            "sended_file": {
                "ui:widget": "remotefilesend"
            }
        }
        form = builder.create_form(self.dbClient.schema, ui_schema, self.json_data)
        form.widget.on_changed.connect(lambda d: self.on_json_data_change(d))
        form.show()

    def buttonnewDocPressed(self):
        builder = WidgetBuilder()
        ui_schema = {
            "buil_color": {
                "ui:widget": "colour"
            },
            "sended_file": {
                "ui:widget": "remotefilesend"
            }
        }
        editDocWidget = builder.create_widget(self.dbClient.schema, ui_schema, self.json_data)
        editDocWidget.on_changed.connect(lambda d: self.on_json_data_change(d))
        current_tab = self.tabDocEditor.addTab(editDocWidget, "Doc")
        self.tabDocEditor.setCurrentIndex(current_tab)
        print("buttonnewDocPressed")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
