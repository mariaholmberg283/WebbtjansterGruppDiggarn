import requests, json

def getSong(artist, title):
    ''' This function creates a search of the artist and title. By using Spotify's API we can search through Spotify's library and return the result. If there is no match en error-message will appear. '''

    searchQuery = artist + " " + title
    searchQuery = searchQuery.replace(" ", "%20")
    searchQuery = searchQuery.replace("&", "")
    searchQuery = searchQuery.replace("'", "")
    r = requests.get("https://api.spotify.com/v1/search?q=" + searchQuery + "&type=track")
    infoSearch = json.loads(r.content)
    formatted = infoSearch['tracks']['items']
    if not formatted:
        return {'error': 'No information available'}
    else:
        return formatted

def getSongExtended(artist, title, auth):
    searchQuery = artist + " " + title
    searchQuery = searchQuery.replace(" ", "%20")
    searchQuery = searchQuery.replace("&", "")
    searchQuery = searchQuery.replace("'", "")
    r = requests.get("https://api.spotify.com/v1/search?q=" + searchQuery + "&type=track", headers=auth)
    infoSearch = json.loads(r.content)
    formatted = infoSearch['tracks']['items']
    if not formatted:
        return {'error': 'No information available'}
    else:
        return formatted

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

