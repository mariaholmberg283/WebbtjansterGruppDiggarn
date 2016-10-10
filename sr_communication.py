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
