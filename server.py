#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, redirect
import requests, xmltodict, sr_communication, spotify_communication, json
import base64

app = Flask(__name__)
authorizedHeader = None

'''
    Hemsida, här kan man bl.a. välja radiostation och logga in med Spotify
'''
@app.route('/')
def index():
    dictionary = sr_communication.getChannels()
    if authorizedHeader:
        return render_template('index.html', channels=dictionary['channel'], loggedIn = True)
    else:
        return render_template('index.html', channels=dictionary['channel'], loggedIn = False)        
    #return render_template('index.html', channels=dictionary['channel'])

'''
    Visa specifik radiokanal och dess playlist (vad den har spelat, spelar just nu etc)
'''
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
    if authorizedHeader:
        return render_template('radiochannel.html', channels=dictionary['channel'], channel=dictionary2, previousSong = previousSong, nowPlaying=nowPlaying, nextSong=nextSong, spotifyPrevious = spotifyPrevious, spotifySong = spotifySong, spotifyNext=spotifyNext)
    else:
        return render_template('radiochannel.html', channels=dictionary['channel'], channel=dictionary2, previousSong = previousSong, nowPlaying=nowPlaying, nextSong=nextSong, spotifyPrevious = spotifyPrevious, spotifySong = spotifySong, spotifyNext=spotifyNext) 

'''
    Säkert logga ut användaren, dirigera till startsidan
'''
@app.route('/logoutSpotify')
def logoutSpotify():
    global authorizedHeader
    authorizedHeader = None
    return redirect('/')

'''
    Sök efter låt på Spotify genom API-anrop
    Om användaren är inloggad (har access token) kan sökningen göras bättre
'''
def searchSpotify(songInfo):
    global authorizedHeader
    if 'error' in songInfo:
        return {'error': 'No information available'}
    else:
        if authorizedHeader:
            track = spotify_communication.getSongExtended(songInfo['artist'], songInfo['title'], authorizedHeader)
        else:
            track = spotify_communication.getSong(songInfo['artist'], songInfo['title'])
        if not track:
            return "Kan inte hitta track"
        else:
            return track

#Spotify
'''
    Läs av kod och hämta access token
'''
@app.route('/callback/q', methods=['GET'])
def callback():
    r = request.args['code']
    getAccessToken(r)
    return redirect('/')

'''
    Hämta access token, som sedan används i server
'''
def getAccessToken(code):
    global authorizedHeader
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:5000/callback/q'
        }
    encoding = base64.b64encode("69e933979e0946a8acb19513ae0bc9c1:644e357b77d148ad81eccaabbe14ccd8")
    headers = {'Authorization': 'Basic {}'.format(encoding) }
    post_request = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
    responseData = json.loads(post_request.text)
    accessToken = responseData['access_token']
    authorizedHeader = {'Authorization': 'Bearer {}'.format(accessToken) }

    profileRequest = requests.get("http://api.spotify.com/v1/me", headers=authorizedHeader)
    profile = json.loads(profileRequest.content)

'''
    API-dokumentation
'''
app.route('/api')
def apipage():
    return render_template('api.html')

#API
'''
    Skriv ut JSON av alla kanaler
'''
@app.route('/api/v1.0/channels/', methods=['GET'])
def getChannels():
    dictionary = sr_communication.getChannels()
    return jsonify(dictionary)

'''
    Skriv ut JSON om en kanal
'''
@app.route('/api/v1.0/channels/<channelID>', methods=['GET'])
def getChannel(channelID):
    channel = sr_communication.getChannel(channelID)
    return jsonify(channel)

'''
    Skriv ut JSON om en kanals playlist
'''
@app.route('/api/v1.0/channels/<channelID>/playlist')
def getChannelPlaylist(channelID):
    channelInfo = {
        'channelID': channelID
        }
    previousSong = sr_communication.previousPlaying(channelID)
    if 'error' not in previousSong:
        channelInfo['previousSong'] = {
            'title': previousSong['title'],
            'artist': previousSong['artist']
            }
        spotifySong = searchSpotify(previousSong)
        if 'error' not in spotifySong:
            channelInfo['previousSong']['spotify'] = {
                'id': spotifySong[0]['id'],
                'uri': spotifySong[0]['uri']
                }
    
    currentSong = sr_communication.getPlaying(channelID)
    if 'error' not in currentSong:
        channelInfo['currentSong'] = {
            'title': currentSong['title'],
            'artist': currentSong['artist']
            }
        spotifySong = searchSpotify(currentSong)
        if 'error' not in spotifySong:
            channelInfo['currentSong']['spotify'] = {
                'id': spotifySong[0]['id'],
                'uri': spotifySong[0]['uri']
                }
        
    nextSong = sr_communication.nextPlaying(channelID)
    if 'error' not in nextSong:
        channelInfo['nextSong'] = {
            'title': nextSong['title'],
            'artist': nextSong['artist']
            }
        spotifySong = searchSpotify(nextSong)
        if 'error' not in spotifySong:
            channelInfo['nextSong']['spotify'] = {
                'id': spotifySong[0]['id'],
                'uri': spotifySong[0]['uri']
                }
    
    return jsonify(channelInfo)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
