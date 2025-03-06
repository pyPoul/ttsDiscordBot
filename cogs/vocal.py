from typing import Optional
import json
import os

import discord as dc
import discord.utils as dutils
from discord.ext import commands

from utils.error import *


def load_languages() -> list[dict] :

    with open('src/lang/lang.json', 'r', encoding='UTF-8') as f :
        return json.load(f)


class Vocal(commands.Cog) :

    bot: commands.Bot
    languages: list[dict]

    def __init__(self, bot: commands.Bot) -> None :
        self.bot = bot
        self.languages = load_languages()

    @commands.Cog.listener()
    async def on_ready(self) -> None :
        await self.bot.wait_until_ready()
        print('Vocal Cog is ready !')

    @dc.app_commands.command()
    async def update_languages(self, i: dc.Interaction) -> None :
        """
        update languages
        """

        if i.user.id not in [''] :
            return

        self.languages = load_languages()

    async def check_and_join_vc(self, i: dc.Interaction, voice_channel: Optional[dc.VoiceChannel] = None) \
            -> tuple[Optional[dc.VoiceChannel], Optional[Exception]] :

        guild_vc: dc.VoiceProtocol = i.guild.voice_client

        if i.user.id not in [''] :

            if guild_vc is not None :
                return None, AlreadyConnectedException('I\'m already connected to')

            if voice_channel is None :

                uc: dc.VoiceChannel = i.user.voice.channel
                if uc is None :
                    return None, UserNotConnectedException('You are not connected to a voice channel')

                voice_channel = uc

            if self.bot.voice_clients :
                return None, AlreadyConnectedException('You are not allowed to move the bot from')

                # TODO: check if user auth, and bot not already in a channel

        if

        # connect to the voice channel
        return await voice_channel.connect(self_deaf=True)

    @dc.app_commands.command()
    async def join(self, i: dc.Interaction, channel: Optional[dc.VoiceChannel] = None) -> None :

        # IDE Warning: Cannot find reference 'defer' in '() -> InteractionResponse'
        await i.response.defer(ephemeral=True)  # type: ignore
        r: dc.InteractionMessage = await i.original_response()

        vc, err = self.check_and_join_vc(i, channel)

        await r.edit(content=f'Successfully connected to {}.')

    @dc.app_commands.command()
    async def leave(self, i: dc.Interaction) :

async def setup(bot: commands.Bot) -> None :
    await bot.add_cog(Vocal(bot))
