#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, xmltodict

def getChannels():
    ''' This function gets all the channels and saves them in a dictionairy and returns the channels '''

    r = requests.get("http://api.sr.se/api/v2/channels/") 
    channelsDict = xmltodict.parse(r.content)
    formattedDict = channelsDict['sr']['channels'] 
    return formattedDict

def getChannel(channelID):
    ''' This function get the channels' id so that we can choose channel and get current info '''

    urlLink = "http://api.sr.se/api/v2/channels/" + str(channelID)
    r = requests.get(urlLink)

    #SR lämnar tillbaka channelID 0 om kanalen inte finns
    if r.status_code == 404:
        return {'error': "Channel does not exist"}
    
    channelDict = xmltodict.parse(r.content)
    formattedDict = channelDict['sr']['channel']
    return formattedDict


def previousPlaying(channelID):
    ''' This function gets the channels' playlist which includes information about the previous song and artist.
        If there is no information available an error-message will appear  '''

    urlLink = "http://api.sr.se/api/v2/playlists/rightnow?channelid=" + str(channelID)
    r = requests.get(urlLink)
    playlistDict = xmltodict.parse(r.content)
    formattedDict = playlistDict['sr']['playlist']
    if 'previoussong' in formattedDict:
        return formattedDict['previoussong']
    else:
        return {'error': 'No information available'}

def getPlaying(channelID):
    ''' This function gets the channels' playlist which includes information about the current song and artist. 
    If there is no information available an error-message will appear '''

    urlLink = "http://api.sr.se/api/v2/playlists/rightnow?channelid=" + str(channelID)
    r = requests.get(urlLink)
    playlistDict = xmltodict.parse(r.content)
    formattedDict = playlistDict['sr']['playlist']
    if 'song' in formattedDict:
        return formattedDict['song']
    else:
        return {'error': 'No information available'}

def nextPlaying(channelID):
    ''' This function gets the channels' playlist which includes information about the next song and artist.
        If there is no information available an error-message will appear '''

    urlLink = "http://api.sr.se/api/v2/playlists/rightnow?channelid=" + str(channelID)
    r = requests.get(urlLink)
    playlistDict = xmltodict.parse(r.content)
    formattedDict = playlistDict['sr']['playlist']
    if 'nextsong' in formattedDict:
        return formattedDict['nextsong']
    else:
        return {'error': 'No information available'}

