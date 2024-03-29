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

        self.urlWidget = self.findChild(QtWidgets.QLineEdit, 'urlEdit')
        self.dbClient.LoadBDschema(self.urlWidget.text())

        self.buttonnewDoc = self.findChild(QtWidgets.QPushButton, 'newDocButton')
        self.buttonnewDoc.setEnabled(False)
        self.buttonnewDoc.clicked.connect(self.editJSON)

        self.buttonPOST = self.findChild(QtWidgets.QPushButton, 'postJSON')
        self.buttonPOST.setEnabled(False)
        self.buttonPOST.clicked.connect( self.buttonPOSTpressed)

        self.ConnecttoDB = self.findChild(QtWidgets.QPushButton, 'ConnecttoDB')
        self.ConnecttoDB.clicked.connect(self.ConnecttoDBpressed)

        self.listofDocs = ListOfDocs.ListOfDocs()
        self.layoutlistofDocs = self.findChild(QtWidgets.QVBoxLayout, 'listofDocs')
        self.layoutlistofDocs.addWidget(self.listofDocs)

        self. DocEditLayout = self.findChild(QtWidgets.QGridLayout, 'DocEditLayout')

        self.show()

    def ConnecttoDBpressed(self):
        try:
            self.dbClient.LoadBDschema(self.urlWidget.text())
        except:
            print("AAAA")
        else:
            print("OK")
            self.timer=QTimer()
            self.timer.timeout.connect(self.TimerForListOfDocs)
            self.timer.start(500)
            self.buttonnewDoc.setEnabled(True)
            self.buttonPOST.setEnabled(True)



    def TimerForListOfDocs(self):
        self.ShowListOfDocs()
        self.timer.start(5000)

    def buttonPOSTpressed(self):
        self.dbClient.postJSON(self.urlWidget.text(), self.DocEditWidget.state)
        self.ShowListOfDocs()

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
        url = self.urlWidget.text()+'/'+self.json_list_local[row]["_id"]["$oid"]
        self.editJSON(self.dbClient.loadJSON(url))


    def selectSchemaButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Load JSON scheme file", "","All Files (*);;JSON schema files (*.json)", options=options)
        if fileName:
            self.jsonschemafile = self.findChild(QtWidgets.QPlainTextEdit, 'jsonschemafile')
            self.jsonschemafile.setPlainText(fileName)
        jfile = open(fileName)
        self.schema = json.load(jfile, object_pairs_hook=collections.OrderedDict)

    def editJSON(self, json_data = None):
        put_file_helper = lambda file: self.dbClient.send_file(self.urlWidget.text(), file)
        get_file_helper = lambda url: self.dbClient.get_file(url)
        get_file_props_helper = lambda url: self.dbClient.loadJSON(url)
        builder = WidgetBuilder(put_file_helper, get_file_helper, get_file_props_helper)
        ui_schema = {
            "buil_color": {
                "ui:widget": "colour"
            },
            "sended_file": {
                "ui:widget": "remotefilesend"
            }
        }
        if (self.DocEditLayout.count()>0):
            self.DocEditWidget.deleteLater()

        if json_data:
             self.DocEditWidget = builder.create_widget(self.dbClient.schema, ui_schema, json_data)
        else:
             self.DocEditWidget = builder.create_widget(self.dbClient.schema, ui_schema)
        self.DocEditLayout.addWidget(self.DocEditWidget)
        self.DocEditWidget.show()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
