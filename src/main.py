from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from arguments import get_ensure_file_path
from ensurance import Ensurance
from new_api import Spotify


def main():
    file_path = get_ensure_file_path()

    ensurance = Ensurance.read_from_file(file_path)

    if ensurance is None:
        return

    load_dotenv()

    scope = ["playlist-read-private", "user-library-read"]

    spotify = Spotify(auth_manager=SpotifyOAuth(scope=scope))

    ensurance.ensure_with(spotify)


if __name__ == "__main__":
    main()
