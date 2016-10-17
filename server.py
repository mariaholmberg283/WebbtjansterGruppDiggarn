#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify
import requests, xmltodict, sr_communication, spotify_communication, json

app = Flask(__name__)

@app.route('/')
def index():
    dictionary = sr_communication.getChannels()
    return render_template('index.html', channels=dictionary['channel'])

@app.route('/radiochannel/<channelID>')
def radiochannel(channelID):
    dictionary2 = sr_communication.getChannel(channelID)
    dictionary = sr_communication.getChannels()
    nowPlaying = sr_communication.getPlaying(channelID)
    nextSong = sr_communication.nextPlaying(channelID)
    spotifySong = searchSpotify(nowPlaying)
    return render_template('radiochannel.html', channels=dictionary['channel'], channel=dictionary2, nowPlaying=nowPlaying, nextSong=nextSong, spotifySong = spotifySong) 

def searchSpotify(songInfo):
    if 'error' in songInfo:
        return {'error': "No information"}
    else:
        response = spotify_communication.getSong(songInfo['artist'], songInfo['title'])
        return response

#API
@app.route('/api/v1.0/channels/', methods=['GET'])
def getChannels():
    dictionary = sr_communication.getChannels()
    return jsonify(dictionary)

@app.route('/api/v1.0/channels/<channelID>', methods=['GET'])
def getChannel(channelID):
    channel = sr_communication.getChannel(channelID)
    return jsonify(channel)

@app.route('/api/v1.0/channels/<channelID>/playing')
def getChannelPlaying(channelID):
    playlist = sr_communication.getPlaying(channelID)
    return jsonify(playlist)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
