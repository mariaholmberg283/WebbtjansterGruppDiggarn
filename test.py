import requests
import xmltodict, json

r = requests.get("http://api.sr.se/api/v2/playlists/rightnow?channelid=2576")
x = r.content
o = xmltodict.parse(x)
print o['sr']['playlist']['song']['description']
