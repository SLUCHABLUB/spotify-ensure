from itertools import batched
from typing import Iterable, Protocol


class ParallellEndpoint[Input, Output](Protocol):
    def __call__(self, input: Iterable[Input], /) -> Iterable[Output]: ...


def process_all[Input, Output](
    endpoint: ParallellEndpoint[Input, Output],
    input: Iterable[Input],
    *,
    batch_size: int,
) -> list[Output]:
    output = list()

    for batch in batched(input, n=batch_size):
        output.extend(endpoint(batch))

    return output
