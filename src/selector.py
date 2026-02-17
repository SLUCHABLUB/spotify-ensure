from functools import partial
from typing import Iterable

from pydantic import BaseModel

import api_types as api
import log
from new_api import Spotify
from pagination import get_all


class Track(BaseModel):
    name: str
    id: str
    playlist: Playlist | None

    def uri(self) -> str:
        return f"spotify:track:{self.id}"

    def display(self) -> str:
        if self.playlist is not None:
            return f"{self.name} (id: {self.id}) in {self.playlist.display()}"
        else:
            return f"{self.name} (id: {self.id})"


class Playlist(BaseModel):
    name: str
    id: str

    def display(self) -> str:
        return f"{self.name} (id: {self.id})"

    @staticmethod
    def from_id(spotify: Spotify, id: str) -> Playlist:
        playlist = api.Playlist.model_validate(spotify.playlist(id, fields="name"))

        return Playlist(name=playlist.name, id=id)


# Types for config use.


class NamedTrack(BaseModel):
    name: str

    def resolve(self, spotify: Spotify) -> Iterable[Track]:
        # TODO: Resolve track from name.
        log.error("cannot resolve a track from just a name yet")
        return []


class TrackWithId(BaseModel):
    id: str

    def resolve(self, spotify: Spotify) -> Iterable[Track]:
        # TODO: Find the name.
        return []


class TrackWithUri(BaseModel):
    uri: str

    def resolve(self, spotify: Spotify) -> Iterable[Track]:
        # TODO: Find the name.
        return []


type SingleTrack = NamedTrack | TrackWithId | TrackWithUri


class NamedPlaylist(BaseModel):
    """A playlist identified by name. Assumed to be a playlist of the user."""

    name: str

    def resolve(self, spotify: Spotify) -> Iterable[Playlist]:
        # TODO: Resolve track from name.
        log.error("cannot resolve a playlist from just a name yet")
        return []


class PlaylistWithId(BaseModel):
    id: str

    def resolve(self, spotify: Spotify) -> Iterable[Playlist]:
        return [Playlist.from_id(spotify, self.id)]


class PlaylistWithUri(BaseModel):
    uri: str

    def resolve(self, spotify: Spotify) -> Iterable[Playlist]:
        return [Playlist.from_id(spotify, self.id())]

    def id(self) -> str:
        return self.uri.lstrip("spotify:playlist:")


type SinglePlaylist = NamedPlaylist | PlaylistWithId | PlaylistWithUri


class AllInPlaylist(BaseModel):
    all_in: SinglePlaylist

    def resolve(self, spotify: Spotify) -> Iterable[Track]:
        playlist = next(iter(self.all_in.resolve(spotify)))

        tracks = get_all(
            api.PlaylistTrack,
            partial(spotify.playlist_items, playlist_id=playlist.id),
        )

        def parser(track: api.PlaylistTrack) -> Track | None:
            if not isinstance(track.item, api.Track):
                log.warn(
                    f"{track.item.type} track found in playlist {self.all_in}, ignoring it"
                )
                return None

            return Track(name=track.item.name, id=track.item.id, playlist=playlist)

        parsed = map(parser, tracks)

        return (track for track in parsed if track is not None)


type TrackSelector = AllInPlaylist | SingleTrack
