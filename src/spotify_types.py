from typing import Literal

from pydantic import BaseModel, Field

type json = dict[str, str]


class Page[Item](BaseModel):
    next: str | None
    items: list[Item]


class SimplifiedPlaylist(BaseModel):
    name: str
    id: str


class PlaylistTrack(BaseModel):
    # TODO: Make this non-exhaustive.
    item: Track | Episode = Field(discriminator="type")


class Track(BaseModel):
    type: Literal["track"]
    name: str
    id: str


class Episode(BaseModel):
    type: Literal["episode"]
    name: str
