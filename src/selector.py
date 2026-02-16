from functools import partial
from typing import Iterable

from pydantic import BaseModel, RootModel

import log
from new_api import Spotify
from pagination import get_all
from spotify_types import PlaylistTrack, Track


class TrackWithId(BaseModel):
    id: str

    def get_id(self) -> str:
        return self.id


class PlaylistWithUri(BaseModel):
    uri: str

    def get_id(self) -> str:
        return self.uri.removeprefix("spotify:playlist:")


class SingleTrack(RootModel[TrackWithId]):
    def resolve(self, spotify: Spotify) -> Iterable[SingleTrack]:
        return [self]

    def id(self) -> str:
        return self.root.get_id()


class AllInPlaylist(BaseModel):
    all_in: SinglePlaylist

    def resolve(self, spotify: Spotify) -> Iterable[SingleTrack]:
        tracks = get_all(
            PlaylistTrack,
            partial(spotify.playlist_items, playlist_id=self.all_in.id()),
        )

        def parser(track: PlaylistTrack) -> SingleTrack | None:
            if not isinstance(track.item, Track):
                log.warn(
                    f"{track.item.type} track found in playlist {self.all_in}, ignoring it"
                )
                return

            return SingleTrack(TrackWithId(id=track.item.id))

        parsed = map(parser, tracks)

        return (track for track in parsed if track is not None)


class TrackSelector(RootModel[AllInPlaylist | SingleTrack]):
    def resolve(self, spotify: Spotify) -> Iterable[SingleTrack]:
        return self.root.resolve(spotify)


class SinglePlaylist(RootModel[PlaylistWithUri]):
    def resolve(self, spotify: Spotify) -> Iterable[PlaylistWithUri]:
        return [self.root]

    def id(self) -> str:
        return self.root.get_id()
