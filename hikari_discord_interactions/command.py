import dataclasses
import typing

from hikari_discord_interactions import types


__all__: list[str] = [
    "Command",
]


@dataclasses.dataclass
class Command:
    name: str
    description: str
    callback: types.Callback
