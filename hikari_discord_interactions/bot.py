from __future__ import annotations

import inspect
import typing

import hikari
from hikari import api
from hikari.impl import special_endpoints

from hikari_discord_interactions import command, context, types, return_types

__all__: list[str] = [
    "Bot",
]


class Bot:
    def __init__(self, token: str, guild_id: int) -> None:
        self._rest_bot: hikari.RESTBot = hikari.RESTBot(token, hikari.TokenType.BOT)
        self._rest: api.RESTClient = self._rest_bot.rest
        self._guild_id = guild_id

        self._commands: [command.Command] = []

        self._rest_bot.set_listener(hikari.CommandInteraction, self._on_application_command)
        self._rest_bot.add_startup_callback(self._on_start)

    def _hikari_type_to_option_type(self, item: typing.Any) -> hikari.OptionType:
        return {
            int: hikari.OptionType.INTEGER,
            bool: hikari.OptionType.BOOLEAN,
            str: hikari.OptionType.STRING,
        }[item]

    def _parse_options(self, callback: types.Callback) -> list[hikari.CommandOption] | None:
        signature = inspect.signature(callback)
        options: list[hikari.CommandOption] = []
        parameters = signature.parameters

        for parameter in parameters:
            parameter = parameters[parameter]
            print(parameter.annotation)

            if parameter.annotation != context.Context:
                options.append(
                    hikari.CommandOption(name=parameter.name, description="none", type=self._hikari_type_to_option_type(parameter.annotation), is_required=True)
                )

        return options

    async def _on_start(self, _: hikari.RESTBot) -> None:
        application: hikari.Application = await self._rest.fetch_application()

        for cmd in self._commands:
            options = self._parse_options(cmd.callback)
            await self._rest.create_slash_command(application, cmd.name, cmd.description, guild=self._guild_id, options=options)

    async def _handle_response(self, interaction: hikari.CommandInteraction, response: types.InteractionResponse) -> special_endpoints.InteractionMessageBuilder:
        interaction_response = interaction.build_response()

        if isinstance(response, str):
            interaction_response.set_content(response)
        elif isinstance(response, return_types.Image):
            interaction_response.add_attachment(response.url)
        elif isinstance(response, hikari.Embed):
            interaction_response.add_embed(response)
        elif isinstance(response, special_endpoints.InteractionMessageBuilder):
            return response

        return interaction_response

    async def _on_application_command(self, interaction: hikari.CommandInteraction) -> special_endpoints.InteractionMessageBuilder | None:
        if interaction.command_type == hikari.CommandType.SLASH:
            for cmd in self._commands:
                if cmd.name == interaction.command_name:
                    if interaction.options != None:
                        options = {option.name: option.value for option in interaction.options}
                        response = await cmd.callback(context.Context(interaction, self._rest), **options)
                    else:
                        response = await cmd.callback(context.Context(interaction, self._rest))

                    return await self._handle_response(interaction, response)

        return None

    def command(self, name: str, description: str) -> typing.Callable[[], None]:
        def inner(callback: typing.Callable[[context.Context, ...], typing.Awaitable[typing.Any]]) -> None:
            self. _commands.append(command.Command(name, description, callback))

        return inner

    def run(self):
        self._rest_bot.run()
