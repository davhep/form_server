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

    def postJSON(self, url, json_data):
        filesend_response = requests.post(url, json=json_data,  auth=('admin', 'secret'))

    def loadJSON(self, url: str):
        r = requests.get(url, allow_redirects=True, auth=('admin', 'secret'))
        json_data=json.loads(str(r.content, 'utf-8'))
        #restheart add _id and _etag, so we have to remove it (may be reusing?)
        #but remove only in document, not a collection - so, we detect class dict and remove id`s
        #dirty code ....
        if(type(json_data) == type({})):
            if '_id' in json_data:
                del json_data['_id']
            if '_etag' in json_data:
                del json_data['_etag']
        #dirty code done
        return(json_data)

    def send_file(self, url, file):
        url = url + '.files'
        filesend_response = requests.post(url, files = {"file_upload":  file },  auth=('admin', 'secret'))
        return(filesend_response.headers['Location'])

    def get_file(self, url):
        fileget_reponse = requests.get(url+'/binary', stream=True, auth=('admin', 'secret'))
        if fileget_reponse.status_code == 200:
            fileget_reponse.raw.decode_content = True
            return(fileget_reponse.raw.data)
        else:
            return(None)
