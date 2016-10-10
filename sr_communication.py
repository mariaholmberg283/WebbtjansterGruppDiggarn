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
    elif 'nextsong' in formattedDict:
        return formattedDict['nextsong']
    return "No info available"

try:
    print getPlaying(223)['description']
except:
    print "N/A"
