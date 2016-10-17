import requests, xmltodict

def getChannels():
    r = requests.get("http://api.sr.se/api/v2/channels/")
    channelsDict = xmltodict.parse(r.content)
    formattedDict = channelsDict['sr']['channels']
    return formattedDict

def getChannel(channelID):
    urlLink = "http://api.sr.se/api/v2/channels/" + str(channelID)
    r = requests.get(urlLink)
    channelDict = xmltodict.parse(r.content)
    formattedDict = channelDict['sr']['channel']
    return formattedDict

def getPlaying(channelID):
    urlLink = "http://api.sr.se/api/v2/playlists/rightnow?channelid=" + str(channelID)
    r = requests.get(urlLink)
    playlistDict = xmltodict.parse(r.content)
    formattedDict = playlistDict['sr']['playlist']
    if 'song' in formattedDict:
        return formattedDict['song']
    else:
        return {'error': 'No information available'}

try:
    print getPlaying(223)['description']
except:
    print "N/A"

    
def nextPlaying(channelID):
    urlLink = "http://api.sr.se/api/v2/playlists/rightnow?channelid=" + str(channelID)
    r = requests.get(urlLink)
    playlistDict = xmltodict.parse(r.content)
    formattedDict = playlistDict['sr']['playlist']
    if 'nextsong' in formattedDict:
        return formattedDict['nextsong']
    else:
        return {'error': 'No information available'}