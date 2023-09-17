import typing

from hikari.impl import special_endpoints

from hikari_discord_interactions import context
from hikari_discord_interactions import return_types

import hikari

InteractionResponse: typing.TypeAlias = str | return_types.Image | hikari.Embed | special_endpoints.InteractionMessageBuilder
Callback: typing.TypeAlias = typing.Callable[[context.Context, ...], typing.Awaitable[InteractionResponse]]
