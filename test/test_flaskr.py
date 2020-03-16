#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import requests



from flask import Flask, jsonify, request

from flask_cors import CORS

from routes import *

app = Flask(__name__)
app.register_blueprint(routes)

CORS(app)


print('1111111111')
print('2222222222')
print('3333333333')
print(os.environ['_url_update_gonsa3'])

url = 'http://127.0.0.1:8081'

def test_get_balance_in_transacations():
    print('---------------------------')
    print('---------------------------')
    print('---------------------------')
    print('---------------------------')
    print("TEEEEEEEEST")
    print(os.environ['_url_update_gonsa3'])
    r = requests.get(os.environ['_url_update_gonsa3'])
    print(r.status_code)
    print('***************************')
    assert r.status_code == 200
print('4444444444')