import tomllib

from pydantic import BaseModel, ValidationError

import log
from new_api import Spotify
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
        for track in self.liked.resolve(spotify):
            print(track.id())
