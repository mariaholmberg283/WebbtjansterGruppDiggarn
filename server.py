#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests, xmltodict, sr_communication

app = Flask(__name__)

@app.route('/')
def index():
    dictionary = sr_communication.getChannels()
    return render_template('index.html', channels=dictionary['channel'])

@app.route('/channels/')
def getChannels():
    dictionary = sr_communication.getChannels()
    return render_template('debugsite.html', name=str(dictionary['channel']))

@app.route('/channels/<channelID>')
def getChannel(channelID):
    channel = sr_communication.getChannel(channelID)
    return render_template('debugsite.html', name=str(channel))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
