from pydantic import BaseModel


class Page[Item](BaseModel):
    href: str
    limit: int
    next: str | None
    offset: int
    previous: str | None
    total: int
    items: list[Item]
