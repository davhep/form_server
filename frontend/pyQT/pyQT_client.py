from PyQt5 import QtWidgets, uic, QtCore, QtNetwork
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

import sys
import json
import argparse
import collections
from json import dumps

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

class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('pyQT_client.ui', self)

        self.json_data = {}

        self.button = self.findChild(QtWidgets.QPushButton, 'selectSchema')
        self.button.clicked.connect(self.selectSchemaButtonPressed)

        self.buttonJE = self.findChild(QtWidgets.QPushButton, 'editJSON')
        self.buttonJE.clicked.connect(self.editJSONPressed)

        self.buttonPOST = self.findChild(QtWidgets.QPushButton, 'postJSON')
        self.buttonPOST.clicked.connect(self.postJSONPressed)

        self.buttonShowJSON = self.findChild(QtWidgets.QPushButton, 'showJSON')
        self.buttonShowJSON.clicked.connect(self.ShowJSONPressed)

        self.buttonLoadJSON = self.findChild(QtWidgets.QPushButton, 'loadJSON')
        self.buttonLoadJSON.clicked.connect(self.LoadJSONPressed)

        self.show()

    def on_json_data_change(self,d):
        print(d)
        self.json_data = d
        self.ShowJSONPressed()

    def getJetsonfinished(self, reply):
        print("Get complete")
        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()
            print(str(bytes_string, 'utf-8'))
            json_data_temp=json.loads(str(bytes_string, 'utf-8'))
            #restheart add _id and _etag, so we have to remove it (may be reusing?)
            del json_data_temp["_id"]
            del json_data_temp["_etag"]
            print(json_data_temp)
            self.json_data = json_data_temp
            self.ShowJSON(self.json_data)


        else:
            print("Error occured: ", er)
            print(reply.errorString())


    def LoadJSONPressed(self):
        url = self.findChild(QtWidgets.QLineEdit, 'urlEdit').text()
        self.request_qt = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        self.manager = QtNetwork.QNetworkAccessManager()
        self.manager.authenticationRequired.connect(self.auth_req)
        self.manager.finished.connect(self.getJetsonfinished)
        self.request = self.manager.get(self.request_qt)

    def ShowJSONPressed(self):
        self.ShowJSON(self.json_data)

    def ShowJSON(self, json_data_input):
        self.text_to_titem = TextToTreeItem()
        self.tree_widget= self.findChild(QtWidgets.QTreeWidget, 'JSONtreeWidget')
        self.tree_widget.clear()
        self.tree_widget.setHeaderLabels(["Key", "Value"])
        self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        root_item = QtWidgets.QTreeWidgetItem(["Root"])
        self.recurse_jdata(json_data_input, root_item)
        self.tree_widget.addTopLevelItem(root_item)
        self.tree_widget.show()



    def recurse_jdata(self, jdata, tree_widget):
        if isinstance(jdata, dict):
            for key, val in jdata.items():
                self.tree_add_row(key, val, tree_widget)
        elif isinstance(jdata, list):
            for i, val in enumerate(jdata):
                key = str(i)
                self.tree_add_row(key, val, tree_widget)
        else:
            print("This should never be reached!")

    def tree_add_row(self, key, val, tree_widget):
        text_list = []

        if isinstance(val, dict) or isinstance(val, list):
            text_list.append(key)
            row_item = QtWidgets.QTreeWidgetItem([key])
            self.recurse_jdata(val, row_item)
        else:
            text_list.append(key)
            text_list.append(str(val))
            row_item = QtWidgets.QTreeWidgetItem([key, str(val)])

        tree_widget.addChild(row_item)
        self.text_to_titem.append(text_list, row_item)


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
            "buil_color": {
                "ui:widget": "colour"
            },
            "sended_file": {
                "ui:widget": "remotefilesend"
            }

        }
        form = builder.create_form(self.schema, ui_schema, self.json_data)
        form.show()
        form.widget.on_changed.connect(lambda d: self.on_json_data_change(d))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
