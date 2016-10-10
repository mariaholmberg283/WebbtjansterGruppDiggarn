#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests, xmltodict, sr_communication

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test/')
def testAPI():
    dictionary = sr_communication.getChannels()
    return render_template('debugsite.html', name=str(dictionary['channel']))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
<<<<<<< HEAD
=======

>>>>>>> refs/remotes/origin/master
