import tomllib
from typing import Iterable

from pydantic import BaseModel, ValidationError

import log
from new_api import Spotify
from parallell import process_all
from selector import TrackSelector


class Ensurance(BaseModel):
    liked: TrackSelector

    @staticmethod
    def read_from_file(path: str) -> Ensurance | None:
        with open(path, "r") as file:
            content = file.read()

        toml = tomllib.loads(content)

        try:
            return Ensurance.model_validate(toml)
        except ValidationError as error:
            log.error(str(error))
            return None

    def ensure_with(self, spotify: Spotify) -> None:
        self.ensure_liked(spotify)

    def ensure_liked(self, spotify: Spotify) -> None:
        tracks = list(self.liked.resolve(spotify))

        uris: Iterable[str] = map(lambda track: track.uri(), tracks)

        is_liked_mask = process_all(
            spotify.check_users_saved_items, uris, batch_size=40
        )

        for track, is_liked in zip(tracks, is_liked_mask):
            if not is_liked:
                log.error(f"{track.display()} is not liked")
