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
    playing: list[int]

    def __init__(self, bot: commands.Bot) -> None :
        self.bot = bot
        self.languages = load_languages()
        self.playing = []

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

    @staticmethod
    async def check_and_join_vc(i: dc.Interaction, voice_channel: Optional[dc.VoiceChannel] = None) \
            -> tuple[dc.VoiceChannel | None, Exception] :

        guild_vp: dc.VoiceProtocol = i.guild.voice_client

        # selected voice channel not in the current guild
        if voice_channel not in i.guild.voice_channels :
            return None, ChannelNotInGuildException('Unknown channel, this channel doesn\'t exist is this server.')

        # voice channel is None ?
        if voice_channel is None :
            uv: dc.VoiceState = i.user.voice
            # user voice channel is None ?
            if uv is None :
                return None, UserNotConnectedException('You are not connected to a voice channel')
            voice_channel = uv.channel

        # bot is already connected to a voice channel
        if guild_vp is not None :

            vc: dc.abc.Connectable = guild_vp.channel
            # bot is already connected to the target channel
            if vc.id == voice_channel.id :
                return None, AlreadyConnectedException(f'I\'m already connected to {voice_channel}.')

            # user hasn't permission to move the bot
            if not i.user.guild_permissions.move_members :
                return None, NotAllowedException(f'You haven\'t the permission to move me from {vc} to {voice_channel}.')

        # connect to the voice channel
        return await voice_channel.connect(self_deaf=True), NULL

    @staticmethod
    async def check_and_leave_vc(i: Optional[dc.Interaction] = None) :

        voice_channel: dc.VoiceChannel

        if i is not None :
            uc: dc.VoiceChannel = i.user.voice.channel

        for


    @dc.app_commands.command()
    async def join(self, i: dc.Interaction, channel: Optional[dc.VoiceChannel] = None) -> None :

        # IDE Warning: Cannot find reference 'defer' in '() -> InteractionResponse'
        await i.response.defer(ephemeral=True)  # type: ignore
        r: dc.InteractionMessage = await i.original_response()

        vc: dc.VoiceChannel
        err: Exception
        vc, err = self.check_and_join_vc(i, channel)
        if err != NULL :
            await r.edit(content=f'Can\'t connect to the voice channel: {err}')
            return

        await r.edit(content=f'Successfully connected to {vc}.')

    @dc.app_commands.command()
    async def leave(self, i: dc.Interaction) -> None :

        await i.response.defer(ephemeral=True)  # type: ignore
        r: dc.InteractionMessage = await i.original_response()


async def setup(bot: commands.Bot) -> None :
    await bot.add_cog(Vocal(bot))
