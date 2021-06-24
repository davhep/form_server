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

class DB_client():
    def __init__(self):
        print("DB_client activated")

    def LoadBDschema(self, url: str):
        r = requests.get(url+'/_meta', allow_redirects=True, auth=('admin', 'secret'))
        json_data_temp=json.loads(str(r.content, 'utf-8'))
        schema_id=json_data_temp["jsonSchema"]["schemaId"]
        parsed_url = urlparse(url)
        r = requests.get(parsed_url.scheme+"://"+parsed_url.netloc+"/_schemas"+"/"+schema_id , allow_redirects=True, auth=('admin', 'secret'))
        self.schema = json.loads(str(r.content, 'utf-8'))

    def postJSON(url, json_data):
        filesend_response = requests.post(url, json=json_data,  auth=('admin', 'secret'))

    def loadJSON(self, url: str):
        r = requests.get(url, allow_redirects=True, auth=('admin', 'secret'))
        json_data=json.loads(str(r.content, 'utf-8'))
        #restheart add _id and _etag, so we have to remove it (may be reusing?)
        #but remove only in document, not a collection - so, we detect class dict and remove id`s
        #dirty code ....
        if(type(json_data) == type({})):
            del json_data["_id"]
            del json_data["_etag"]
        #dirty code done
        return(json_data)
