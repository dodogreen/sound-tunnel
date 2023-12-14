# Client_ID and Client_secret from Spotify Developers Dashboard
CLIENT_ID = "6a360d2dff414cca9e6a5e9fc9a7c611"
CLIENT_SECRET = "e3e68924e0bd45f89cec35206fa18c27"

# Option 1
# REDIRECT_URI can be set to localhost
# the spotipy module should automatically get the access code by setting up a simple server at specified port
#
# Option 2
# REDIRECT_URI can be set to a random website (make sure it's a nonexistent website else the website's owner
# will probably see your access code in their logs, not a smart move)
# 
# MAKE SURE THE SAME REDIRECT URI SET HERE IS ALSO SET ON YOUR SPOTIPY DASHBOARD
REDIRECT_URI = "http://localhost:4321/callback/"

# The permissions needed to access all your spotify playlists
SCOPE = "playlist-read-collaborative playlist-read-private user-library-read playlist-modify-private"

# File containing your youtubemusic cookies
ytfile = ".creds/headers_auth.json"

# File containing your tidal cookies
tidalfile = ".creds/creds_auth.txt"

# File containing your applemusic cookies
applefile = ".creds/i_auth.txt"
