from typing import Any, Iterable, override

import spotipy


class Spotify(spotipy.Spotify):
    def check_users_saved_items(self, uris: list[str]) -> list[bool]:
        # pyrefly: ignore[bad-return]
        return self._get("/me/library/contains?uris=" + ",".join(uris))

    @override
    def playlist_items(
        self,
        playlist_id: str,
        fields: None = None,
        limit: int = 100,
        offset: int = 0,
        market: str | None = None,
        additional_types: Iterable[str] = ("track", "episode"),
    ) -> dict[str, Any]:

        id = self._get_id("playlist", playlist_id)
        # pyrefly: ignore[bad-return]
        return self._get(
            f"playlists/{id}/items",
            limit=limit,
            offset=offset,
            fields=fields,
            market=market,
            additional_types=",".join(additional_types),
        )
