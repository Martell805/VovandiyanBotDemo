import discord

from saver import Saver
from .duel_users import DuelUser


class DuelHandler(Saver):
    def __init__(self, client: discord.Client, score_channel_id: int, allowed_channels_id=None):
        super().__init__(client, score_channel_id)
        super().set_prefix("<DUELSCORE>")
        super().set_user_class(DuelUser)

        self.__allowed_channels = allowed_channels_id

    def add_allowed_channel_id(self, channel_id: int) -> None:
        self.__allowed_channels.append(channel_id)

    def get_allowed_channels_id(self) -> list[int]:
        return self.__allowed_channels

    async def duel(self, channel: discord.TextChannel, duelist1: discord.Member, duelist2: discord.Member) -> None:
        if not (self.get_allowed_channels_id() is None) and channel.id not in self.get_allowed_channels_id():
            return

        if duelist1 == duelist2:
            await channel.send(f"{duelist1.mention}, вы не можете провести дуэль с самим собой")
            return

        if duelist1.bot or duelist2.bot:
            await channel.send(f"Боты не могут участвовать в дуэлях")
            return

        duel_user1 = self[duelist1]
        duel_user2 = self[duelist2]

        duelist1_roll = duel_user1.roll()
        duelist2_roll = duel_user2.roll()

        text = f"{duelist1.mention} выбрасывает {duelist1_roll} из 100\n" \
               f"{duelist2.mention} выбрасывает {duelist2_roll} из 100\n"

        if duelist1_roll > duelist2_roll:
            winner = duel_user1
            text += f"{duelist1.mention} побеждает!"
        elif duelist1_roll < duelist2_roll:
            winner = duel_user2
            text += f"{duelist2.mention} побеждает!"
        else:
            winner = None
            text += f"Ничья!"

        duel_user1.duel_result(duel_user2, winner)
        duel_user2.duel_result(duel_user1, winner)

        await self.update_message()

        await channel.send(text)
