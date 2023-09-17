import dataclasses

import hikari
from hikari import api


__all__: list[str] = [
    "Context"
]


@dataclasses.dataclass
class Context:
    interaction: hikari.CommandInteraction
    rest: api.RESTClient
