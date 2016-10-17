import requests, json

def getSong(artist, title):
    searchQuery = artist + "%20" + title
    searchQuery = searchQuery.replace(" ", "%20")
    print searchQuery
    r = requests.get("https://api.spotify.com/v1/search?q=" + searchQuery + "&type=track")
    infoSearch = json.loads(r.content)
    formatted = infoSearch['tracks']['items']
    if not formatted:
        return {'error': "No information"}
    else:
        return formatted


