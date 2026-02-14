from pydantic import BaseModel

type json = dict[str, str]


class Page[Item](BaseModel):
    next: str | None
    items: list[Item]


class SimplifiedPlaylist(BaseModel):
    name: str
    id: str
