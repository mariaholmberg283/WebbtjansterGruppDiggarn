#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests, xmltodict, sr_communication, json

app = Flask(__name__)

@app.route('/')
def index():
    dictionary = sr_communication.getChannels()
    return render_template('index.html', channels=dictionary['channel'])

@app.route('/radiochannel')
def radiochannel():
    dictionary = sr_communication.getChannels()
    desc = sr_communication.getPlaying(223)
    return render_template('radiochannel.html', channels=dictionary['channel'], playing=desc['description']) 



#API
@app.route('/api/v1.0/channels/', methods=['GET'])
def getChannels():
    dictionary = sr_communication.getChannels()
    return json.dumps(dictionary)

@app.route('/api/v1.0/channels/<channelID>', methods=['GET'])
def getChannel(channelID):
    channel = sr_communication.getChannel(channelID)
    return json.dumps(channel)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
