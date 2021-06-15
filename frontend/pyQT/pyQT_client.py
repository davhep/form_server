from PyQt5 import QtWidgets, uic, QtCore
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

        self.button = self.findChild(QtWidgets.QPushButton, 'printButton') # Find the button
        self.button.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!

        self.show()

    def printButtonPressed(self):
        # This is executed when the button is pressed
        print('printButtonPressed')
        print(type(100))
        a = 3
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Load JSON scheme file", "","All Files (*);;JSON schema files (*.json)", options=options)
        if fileName:
            self.jsonschemafile = self.findChild(QtWidgets.QPlainTextEdit, 'jsonschemafile') # Find the button
            self.jsonschemafile.setPlainText(fileName)
            print(fileName)
        jfile = open(fileName)
        schema = json.load(jfile, object_pairs_hook=collections.OrderedDict)
        builder = WidgetBuilder()
        ui_schema = {
            "schema_path": {
                "ui:widget": "filepath"
            },
            "buil_color": {
                "ui:widget": "colour"
            }

        }
        form = builder.create_form(schema, ui_schema)
        form.show()
        form.widget.on_changed.connect(lambda d: print(dumps(d, indent=4)))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

