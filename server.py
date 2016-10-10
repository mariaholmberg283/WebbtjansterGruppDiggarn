#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests, xmltodict
from xml.etree import ElementTree

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def testAPI():
    r = requests.get("http://api.sr.se/api/v2/playlists/rightnow?channelid=2576")
    newDict = xmltodict.parse(r.content)
    return newDict['sr']['playlist']['song']['description']


if __name__ == "__main__":
    app.run(debug=True, port=5000)

