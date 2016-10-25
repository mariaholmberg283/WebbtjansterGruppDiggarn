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
    previousSong = sr_communication.previousPlaying(channelID)
    nowPlaying = sr_communication.getPlaying(channelID)
    nextSong = sr_communication.nextPlaying(channelID)
    spotifyPrevious = searchSpotify(previousSong)
    spotifySong = searchSpotify(nowPlaying)
    spotifyNext = searchSpotify(nextSong)
    return render_template('radiochannel.html', channels=dictionary['channel'], channel=dictionary2, previousSong = previousSong, nowPlaying=nowPlaying, nextSong=nextSong, spotifyPrevious = spotifyPrevious, spotifySong = spotifySong, spotifyNext=spotifyNext) 

def searchSpotify(songInfo):
    if 'error' in songInfo:
        return {'error': 'No information available'}
    else:
        track = spotify_communication.getSong(songInfo['artist'], songInfo['title'])
        if not track:
            return "Kan inte hitta track"
        else:
            return track

#Spotify
@app.route('/callback', methods=['GET'])
def callAuthorization():
    return "Authorization complete"

@app.route('/api')
def apipage():
    return render_template('api.html')

#API
@app.route('/api/v1.0/channels/', methods=['GET'])
def getChannels():
    dictionary = sr_communication.getChannels()
    return jsonify(dictionary)

@app.route('/api/v1.0/channels/<channelID>', methods=['GET'])
def getChannel(channelID):
    channel = sr_communication.getChannel(channelID)
    channelInfo = {
        'id': channelID,
        'name': channel['@name'],
        'image': channel['image']
        }
    previousSong = sr_communication.previousPlaying(channelID)
    if 'error' not in previousSong:
        channelInfo['previousSong'] = {
            'title': previousSong['title'],
            'artist': previousSong['artist']
            }
    currentSong = sr_communication.getPlaying(channelID)
    if 'error' not in currentSong:
        channelInfo['currentSong'] = {
            'title': currentSong['title'],
            'artist': currentSong['artist']
            }
    nextSong = sr_communication.nextPlaying(channelID)
    if 'error' not in nextSong:
        channelInfo['nextSong'] = {
            'title': nextSong['title'],
            'artist': nextSong['artist']
            }
    
    return jsonify(channelInfo)

@app.route('/api/v1.0/channels/<channelID>/playlist')
def getChannelPlaylist(channelID):
    channelInfo = {
        'id': channelID
        }
    previousSong = sr_communication.previousPlaying(channelID)
    if 'error' not in previousSong:
        channelInfo['previousSong'] = {
            'title': previousSong['title'],
            'artist': previousSong['artist']
            }
        spotifySong = searchSpotify(previousSong)
        if 'error' not in spotifySong:
            channelInfo['previousSong']['spotify'] = spotifySong[0]['uri']
    
    currentSong = sr_communication.getPlaying(channelID)
    if 'error' not in currentSong:
        channelInfo['currentSong'] = {
            'title': currentSong['title'],
            'artist': currentSong['artist']
            }
        spotifySong = searchSpotify(currentSong)
        if 'error' not in spotifySong:
            channelInfo['currentSong']['spotify'] = spotifySong[0]['uri']
        
    nextSong = sr_communication.nextPlaying(channelID)
    if 'error' not in nextSong:
        channelInfo['nextSong'] = {
            'title': nextSong['title'],
            'artist': nextSong['artist']
            }
        spotifySong = searchSpotify(nextSong)
        if 'error' not in spotifySong:
            channelInfo['nextSong']['spotify'] = spotifySong[0]['uri']
    
    return jsonify(channelInfo)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
