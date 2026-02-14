from typing import Any, Protocol

from pydantic import BaseModel

from spotify_types import Page, json


class PaginatedEndpoint(Protocol):
    def __call__(self, limit: int = ..., offset: int = ...) -> Any: ...


def get_all[Item: BaseModel](
    model: type[Item],
    function: PaginatedEndpoint,
) -> list[Item]:
    items: list[Item] = list()

    offset = 0

    while True:
        raw_response: Any = function(offset=offset)

        response: Page[json] = Page.model_validate(raw_response)

        page_items = map(model.model_validate, response.items)

        items.extend(page_items)
        offset += len(response.items)

        if response.next is None:
            break

    return items
