import discord

from .users import User


class Saver:
    users: dict[int: User] = {}
    client: discord.Client = None

    def __init__(self, client: discord.Client, score_channel_id: int):
        self.client = client
        self.score_channel_id = score_channel_id

    async def __get_score_message(self) -> discord.Message | None:
        info_channel = self.client.get_channel(self.score_channel_id)
        async for message in info_channel.history(limit=10):
            if message.author == self.client.user:
                return message
        return None

    async def reset_message(self):
        score_message = await self.__get_score_message()
        await score_message.edit(content='<SCORE>')

    async def update_saver(self):
        score_message = await self.__get_score_message()
        score_message_user_list = score_message.content.split('\n')[1:]

        for user_info in score_message_user_list:
            user_info = user_info.split()[1:]
            id = int(user_info[0])
            name = ' '.join(user_info[1:-2])
            score = int(user_info[-2])
            last_change = int(user_info[-1])
            self.users[id] = User(id, name, score, last_change)

    async def update_message(self):
        new_text = '<SCORE>\n'
        for user_id in self.users:
            new_text += str(self.users[user_id]) + '\n'

        score_message = await self.__get_score_message()
        await score_message.edit(content=new_text)

    def __getitem__(self, item: discord.Member) -> User:
        if item.id not in self.users:
            self.users[item.id] = User(item.id, item.name)
        return self.users[item.id]

    def on_member_enter(self, member: discord.Member):
        self[member].on_enter()

    def on_member_exit(self, member: discord.Member):
        self[member].on_exit()

    def get_all_users(self) -> dict[int: User]:
        return self.users
