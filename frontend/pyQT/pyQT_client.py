from PyQt5 import QtWidgets, uic, QtCore, QtNetwork
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

import sys
import json
import argparse
import collections
from json import dumps

from qt_jsonschema_form import WidgetBuilder

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('pyQT_client.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'selectSchema')
        self.button.clicked.connect(self.selectSchemaButtonPressed)

        self.buttonJE = self.findChild(QtWidgets.QPushButton, 'editJSON')
        self.buttonJE.clicked.connect(self.editJSONPressed)

        self.buttonPOST = self.findChild(QtWidgets.QPushButton, 'postJSON')
        self.buttonPOST.clicked.connect(self.postJSONPressed)

        self.show()

    def on_json_data_change(self,d):
        print(d)
        self.json_data = d

    def selectSchemaButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Load JSON scheme file", "","All Files (*);;JSON schema files (*.json)", options=options)
        if fileName:
            self.jsonschemafile = self.findChild(QtWidgets.QPlainTextEdit, 'jsonschemafile')
            self.jsonschemafile.setPlainText(fileName)
            print(fileName)

        jfile = open(fileName)
        self.schema = json.load(jfile, object_pairs_hook=collections.OrderedDict)

    def auth_req(self, req, auth):
      print("Auth req")
      auth.setUser("admin")
      auth.setPassword("secret")

    def postJSONPressed(self):
        url = self.findChild(QtWidgets.QLineEdit, 'urlEdit').text()
        self.request_qt = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        self.request_qt.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 'application/json')
        self.manager = QtNetwork.QNetworkAccessManager()
        self.manager.authenticationRequired.connect(self.auth_req)
        self.request = self.manager.post(self.request_qt, json.dumps(self.json_data).encode("utf-8"))

    def editJSONPressed(self):
        builder = WidgetBuilder()
        ui_schema = {
            "schema_path": {
                "ui:widget": "filepath"
            },
            "buil_color": {
                "ui:widget": "colour"
            }

        }
        form = builder.create_form(self.schema, ui_schema)
        form.show()
        form.widget.on_changed.connect(lambda d: self.on_json_data_change(d))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
