from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from pagination import get_all
from spotify_types import SimplifiedPlaylist


def main():
    load_dotenv()

    scope = ["playlist-read-private"]

    spotify = Spotify(auth_manager=SpotifyOAuth(scope=scope))

    playlists = get_all(SimplifiedPlaylist, spotify.current_user_playlists)

    for playlist in playlists:
        print(playlist.name)


if __name__ == "__main__":
    main()
