import discord

from .users import User


class Saver:
    def __init__(self, client: discord.Client, score_channel_id: int):
        self.__users: dict[int] = {}
        self.__client = client
        self.__score_channel_id = score_channel_id
        self.__prefix = "<SAVER>"
        self.__user_class = User

    def get_prefix(self) -> str:
        return self.__prefix

    def set_prefix(self, prefix: str) -> None:
        self.__prefix = prefix

    def get_user_class(self) -> type:
        return self.__user_class

    def set_user_class(self, user_class) -> None:
        self.__user_class = user_class

    def get_score_channel_id(self) -> int:
        return self.__score_channel_id

    def get_client(self) -> discord.Client:
        return self.__client

    async def __get_score_message(self) -> discord.Message:
        info_channel = self.get_client().get_channel(self.get_score_channel_id())

        while True:
            async for message in info_channel.history(limit=10):
                if message.author == self.get_client().user and message.content.startswith(self.get_prefix()):
                    return message

            await info_channel.send(self.get_prefix())

    async def reset_message(self) -> None:
        score_message = await self.__get_score_message()
        await score_message.edit(content=self.get_prefix())

    async def update_saver(self) -> None:
        score_message = await self.__get_score_message()
        score_message_user_list = score_message.content.split('\n')[1:]

        for user_info in score_message_user_list:
            new_user = self.__user_class.parse_user(user_info)
            self.__users[new_user.get_id()] = new_user

    async def update_message(self) -> None:
        new_text = self.get_prefix() + '\n'
        for user_id in self.__users:
            new_text += str(self.__users[user_id]) + '\n'

        score_message = await self.__get_score_message()
        await score_message.edit(content=new_text)

    def __getitem__(self, item: discord.Member):
        if item.id not in self.__users:
            self.__users[item.id] = self.get_user_class()(item.id, item.name)
        return self.__users[item.id]

    def get_all_users(self) -> dict[int]:
        return self.__users
