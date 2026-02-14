from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def main():
    load_dotenv()

    scope: list[str] = ["playlist-read-private"]

    spotify: Spotify = Spotify(auth_manager=SpotifyOAuth(scope=scope))

    result: dict[str, str] = spotify.current_user_playlists()

    for playlist in result["items"]:
        print(playlist["name"])


if __name__ == "__main__":
    main()
