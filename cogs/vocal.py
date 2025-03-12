from typing import Optional
import json

import discord as dc
from discord.ext import commands

from utils.constants import AUTH_USERS
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

        if i.user.id not in AUTH_USERS :
            return

        self.languages = load_languages()

    @staticmethod
    async def check_and_join_vc(i: dc.Interaction, voice_channel: Optional[dc.VoiceChannel] = None) \
            -> tuple[dc.VoiceChannel | None, Exception] :

        # get current user voice (channel)
        uv: dc.VoiceState = i.user.voice
        # get current guild voice channels
        gvc: list[voice_channel] = i.guild.voice_channels

        # selected voice channel not in the current guild
        if uv is not None :
            if voice_channel not in gvc and i.user.voice.channel not in gvc :
                # should not happen
                return None, ChannelNotInGuildException('Unknown channel, this channel doesn\'t exist is this server.')

        # voice channel is None ?
        if voice_channel is None :
            # user voice channel is None ?
            if uv is None :
                return None, UserNotConnectedException('You are not connected to a voice channel.')
            voice_channel = uv.channel

        gvp: dc.VoiceProtocol = i.guild.voice_client
        # bot is already connected to a voice channel
        if gvp is not None :

            vc: dc.abc.Connectable = gvp.channel
            # is the bot already connected to the target channel ?
            if vc.id == voice_channel.id :
                return None, AlreadyConnectedException(f'I\'m already connected to {voice_channel}.')

            # user hasn't permission to move the bot
            if not i.user.guild_permissions.move_members :
                return None, NotAllowedException(f'You haven\'t the permission to move me from {vc} to {voice_channel}.')
            # disconnect the bot from the current channel
            await gvp.disconnect(force=False)

        # connect to the voice channel (deaf for more confidence, the goal of the bot isn't to record voice chats)
        await voice_channel.connect(self_deaf=True)
        return voice_channel, NULL

    @staticmethod
    async def check_and_leave_vc(g: dc.Guild, i: Optional[dc.Interaction] = None) \
            -> Exception :

        # bot not connected
        gvp: dc.VoiceProtocol = g.voice_client
        print(i.guild.voice_client)
        if gvp is None :
            return ClientNotConnectedException('I\'m not connected to a voice channel.')

        # auto disconnect
        if i is None :
            await gvp.disconnect(force=True)
            return NULL

        uv: dc.VoiceState = i.user.voice
        # user has permissions ?
        if not i.user.guild_permissions.move_members :
            # is the user connected to a voice channel ?
            if uv is None :
                return UserNotConnectedException('You are not connected to a voice channel.')

            cvc: dc.abc.Connectable = gvp.channel
            # user not in the same voice channel than
            if uv.channel.id != cvc.id :
                if len(cvc.members) != 1 :
                    return NotAllowedException('You can\'t disconnect me from a channel you are not in.')

        await gvp.disconnect(force=True)
        return NULL

    @dc.app_commands.command()
    async def join(self, i: dc.Interaction, channel: Optional[dc.VoiceChannel] = None) -> None :
        """
        join a voice channel
        """

        # IDE Warning: Cannot find reference 'defer' in '() -> InteractionResponse'
        await i.response.defer(ephemeral=True)  # type: ignore
        r: dc.InteractionMessage = await i.original_response()

        vc: dc.VoiceChannel
        err: Exception
        vc, err = await self.check_and_join_vc(i, channel)
        if err != NULL :
            await r.edit(content=f'Can\'t connect to the voice channel: {err}')
            return

        await r.edit(content=f'Successfully connected to <#{vc.id}>.')

    @dc.app_commands.command()
    async def leave(self, i: dc.Interaction) -> None :
        """
        leave a voice channel
        """

        await i.response.defer(ephemeral=True)  # type: ignore
        r: dc.InteractionMessage = await i.original_response()

        if (err := await self.check_and_leave_vc(i.guild, i)) != NULL :
            await r.edit(content=f'Can\'t disconnect from the voice channel: {err}')
            return

        await r.edit(content='Successfully disconnected from the voice channel.')


async def setup(bot: commands.Bot) -> None :
    await bot.add_cog(Vocal(bot))
