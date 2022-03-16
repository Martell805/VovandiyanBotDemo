import discord

from saver import Saver
from .score_users import ScoreUser


class ScoreSaver(Saver):
    def __init__(self, client: discord.Client, score_channel_id: int):
        super().__init__(client, score_channel_id)
        super().set_prefix("<SCORE>")
        super().set_user_class(ScoreUser)

    async def on_member_enter(self, member: discord.Member) -> None:
        self[member].on_enter()
        await self.update_message()

    async def on_member_exit(self, member: discord.Member) -> None:
        self[member].on_exit()
        await self.update_message()
