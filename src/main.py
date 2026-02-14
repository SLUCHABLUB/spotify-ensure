from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from pagination import get_all


def main():
    load_dotenv()

    scope: list[str] = ["playlist-read-private"]

    spotify: Spotify = Spotify(auth_manager=SpotifyOAuth(scope=scope))

    playlists = get_all(spotify.current_user_playlists)

    for playlist in playlists:
        print(playlist["name"])


if __name__ == "__main__":
    main()
