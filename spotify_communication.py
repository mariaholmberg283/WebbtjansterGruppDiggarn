import requests, json

def getSong(artist, title):
    ''' This function creates a search of the artist and title. By using Spotify's API we can search through Spotify's library and return the result. If there is no match en error-message will appear. '''

    searchQuery = artist + "%20" + title
    searchQuery = searchQuery.replace(" ", "%20")
    print searchQuery
    r = requests.get("https://api.spotify.com/v1/search?q=" + searchQuery + "&type=track")
    infoSearch = json.loads(r.content)
    formatted = infoSearch['tracks']['items']
    if not formatted:
        return {'error': 'No information available'}
    else:
        return formatted


def authorize():
    ''' This function '''

    r = requests.get("https://accounts.spotify.com/authorize?client_id=69e933979e0946a8acb19513ae0bc9c1&response_type=code&redirect_uri=localhost:5000/spotifyResponse&scope=user-read-private")
    print r.content

authorize()
    
