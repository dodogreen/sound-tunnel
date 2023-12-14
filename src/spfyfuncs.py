import sys
import re
import spotipy
from src.mainfuncs import message, what_to_move, compare
from math import ceil
from time import sleep
from config.config import CLIENT_SECRET, CLIENT_ID, REDIRECT_URI, SCOPE
import requests

def spotify_auth():
# Attempt to authenticate Spotify
   try:
      # print(f"CLIENT_ID: {CLIENT_ID}")
      # print(f"CLIENT_SECRET: {CLIENT_SECRET}")
      spotify = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))
      message("s+","Successfully Authenticated")
      return spotify
   except Exception:
      message("s+","Authentication failed")
      sys.exit(0)
   # had to add print(auth_url) to line 435 of /usr/local/lib/python3.10/dist-packages/spotipy/oauth2.py so that the script would print the link
   # why? because wsl2 sucks
   
def spotify_user_playlists(headers):
   url = "https://api.spotify.com/v1/me/playlists"
   r = requests.get(url, headers=headers)
   if r.status_code == 200:
      return r.json()

def get_spotify_playlists(spotify):
   # Gets user spotify playlists
   user_playlists = spotify.current_user_playlists(limit=50)

   # for i in user_playlists['items']:
   #    print(f"user_playlists: {i['name']}")
   print(f"user_playlists['items'] len: {len(user_playlists['items'])}")

   albums = spotify.current_user_saved_albums(limit=20, offset=0)
   # for i in albums['items']:
   #    print(f"albums: {i['album']['name']}")
   print(f"albums['items'] len: {len(albums['items'])}")
   # print(f"albums: {albums['items']}")

   shows = spotify.current_user_saved_shows(limit=50, offset=0)
   # for i in shows['items']:
      # print(f"shows: {i['show']['name']}")
   print(f"shows['items'] len: {len(shows['items'])}")

   tracks = spotify.current_user_saved_tracks(limit=20, offset=0)
   # for i in tracks['items']:
      # print(f"tracks: {i['track']['name']}")
   print(f"tracks['items'] len: {len(tracks['items'])}")

   
   # user_playlists_func = spotify_user_playlists(spotify)
   # print(f"user_playlists_func: {user_playlists_func}")


   spfy_lists = {}
   # try:
   for i in user_playlists['items']:
      # print(f"i: {i}")
      playlist_name = i['name']
      playlist_id = i['id']
      # Add playlist name and ids to dictionary
      spfy_lists[playlist_name] = playlist_id
   print(f"after list {len(spfy_lists)}")

   for i in albums['items']:
      # print(f"i: {i['album']['name']}")
      # print(f"i: {i['album']['id']}")

      playlist_name = i['album']['name']
      playlist_id = i['album']['id']
      # Add playlist name and ids to dictionary
      spfy_lists[playlist_name] = playlist_id
   print(f"after album {len(spfy_lists)}")

   for i in shows['items']:
      playlist_name = i['show']['name']
      playlist_id = i['show']['id']
      # Add playlist name and ids to dictionary
      spfy_lists[playlist_name] = playlist_id
   print(f"after show {len(spfy_lists)}")

   for i in tracks['items']:
      playlist_name = i['track']['name']
      playlist_id = i['track']['id']
      # Add playlist name and ids to dictionary
      spfy_lists[playlist_name] = playlist_id
   print(f"after track {len(spfy_lists)}")


   # except:
   #    # Triggered for non-songs
   #    pass



   print(f"final len: {len(spfy_lists)}")
   print(f"spfy_lists: {spfy_lists}")

   return spfy_lists

def get_spfy_likes(spotify):
   # Gets track on spotify liked list
   test_likes = spotify.current_user_saved_tracks(limit=50)
   no_of_liked_songs = test_likes['total']
   total_requests = ceil(no_of_liked_songs/50)
   result = []
   for i in range(total_requests):
      like = spotify.current_user_saved_tracks(limit=50, offset=50*i)
      for song in like['items']:
         song_name = song['track']['name']
         album_name = song['track']['album']['name']
         artist_name = []
         for i in song['track']['artists']:
            artist = i['name']
            artist_name.append(artist)
         artist = ' '.join(artist_name)
         result.append(album_name+"&@#72"+song_name+"&@#72"+artist)
   return result

def get_spfy_playlist_content(spotify, source_id):
   # Gets track on spotify playlist
   playlist_content = spotify.playlist_items('spotify:playlist:{}'.format(source_id))
   result = []
   for song in playlist_content['items']:
      try:
         song_name = song['track']['name']
         album_name = song['track']['album']['name']
         artist_name = []
         for i in song['track']['artists']:
            artist = i['name']
            artist_name.append(artist)
         artist = ' '.join(artist_name)
         result.append(album_name+"&@#72"+song_name+"&@#72"+artist)
      except:
         pass
   
   # test_likes = spotify.playlist_items(limit=50, playlist_id='spotify:playlist:{}'.format(source_id))
   # no_of_liked_songs = test_likes['total']
   # total_requests = ceil(no_of_liked_songs/50)
   # result = []
   # for i in range(total_requests):
   #    like = spotify.current_user_saved_tracks(limit=50, offset=50*i)
   #    for song in like['items']:
   #       song_name = song['track']['name']
   #       album_name = song['track']['album']['name']
   #       artist_name = []
   #       for i in song['track']['artists']:
   #          artist = i['name']
   #          artist_name.append(artist)
   #       artist = ' '.join(artist_name)
   #       result.append(album_name+"&@#72"+song_name+"&@#72"+artist)
   # return result
      # song_name = song['track']['name']
      # album_name = song['track']['album']['name']
      # artist_name = []
      # for i in song['track']['artists']:
      #    artist = i['name']
      #    artist_name.append(artist)
      # artist = ' '.join(artist_name)
      # result.append(album_name+"&@#72"+song_name+"&@#72"+artist)
   return result

def spfy_dest_check(spfy_lists, spotify, spfy_id, dest_playlist_name):
   if dest_playlist_name in spfy_lists:
      dest_playlist_id = spfy_lists[dest_playlist_name]
      message("s+","Playlist exists, adding missing songs")
   else:
      create_playlist = spotify.user_playlist_create(spfy_id, dest_playlist_name, public=False, collaborative=False, description='Sound Tunnel Playlist')
      dest_playlist_id = create_playlist['id']
      message("s+","Playlist created")
   return dest_playlist_id

def move_to_spfy(spotify, playlist_info, dest_id):
   not_found = []
   present_song = get_spfy_playlist_content(spotify, dest_id)
   playlist_info = what_to_move(present_song, playlist_info)

   # try:
   for i in playlist_info:
      try:
         # print(f" music {i}")
         i = i.replace("&@#72", " ")
         try:
            search = spotify.search(i, limit=5, type="track")
         except:
            bk = i
            i = re.sub("\(.*?\)","",i)
            try:
               search = spotify.search(i, limit=5, type="track")
            except:
               not_found.append(bk)
               continue
         for song in search['tracks']['items']:
            album_name = song['album']['name']
            song_name = song['name']
            artist_name = []
            for j in song['artists']:
               artist = j['name']
               artist_name.append(artist)
            artist = ' '.join(artist_name)
            found = album_name+" "+song_name+" "+artist
            songid = [song['id']]
            if compare(found, i):
               sleep(0.5)
               spotify.playlist_add_items(dest_id, songid)
               break
         else:
            not_found.append(i)
      # print exception information and continue
      except Exception as e:
         print(f"Exception song: {i}")
         print(e)
         not_found.append(i)

         continue
   return not_found
   # except:
   #    return not_found