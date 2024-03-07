import spotipy
import webbrowser
import json
with open("SECRETS.json", "r") as f:  # JSON
    pw = json.load(f)
    f.close()
username = pw[0]["Spotify_User"]
clientID = pw[0]["Spotify_ClientID"]
clientSecret = pw[0]["Spotify_ClientSecret"]
redirect_uri = 'http://localhost:8080/callback'

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
token_dict = oauth_object.get_cached_token()
token = token_dict['access_token']
sp = spotipy.Spotify(auth=token)
user_name = sp.current_user()

def spotify_search(prompt):
    res = sp.search(prompt, 1, 0, "track")
    tracks = res["tracks"]["items"]
    song = tracks[0]['external_urls']['spotify']
    webbrowser.open(song)
    return
