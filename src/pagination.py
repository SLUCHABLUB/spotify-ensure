from typing import Protocol

from spotify_types import Page


class PaginatedEndpoint(Protocol):
    def __call__(self, limit: int = ..., offset: int = ...) -> dict[str, str]: ...


def get_all[Item](function: PaginatedEndpoint) -> list[Item]:
    items = list()

    offset = 0

    while True:
        response = function(offset=offset)

        response = Page.model_validate(response)

        items.extend(response.items)
        offset += len(response.items)

        if response.next is None:
            break

    return items
