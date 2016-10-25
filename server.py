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

def getArtist(artist):

    searchQuery = artist
    searchQuery = searchQuery.replace(" ", "%20")
    r = requests.get("https://api.spotify.com/v1/search?q=" + searchQuery + "&type=track")
    infoSearch = json.loads(r.content)
    formatted = infoSearch['tracks']['items']
    if not formatted:
        return {'error': 'No information available'}
    else:
        return formatted

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
    return jsonify(channel)

@app.route('/api/v1.0/channels/<channelID>/playing')
def getChannelPlaying(channelID):
    playlist = sr_communication.getPlaying(channelID)
    return jsonify(playlist)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
