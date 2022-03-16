import discord

from .category import Category


class CategoryHandler:
    def __init__(self, client: discord.Client):
        self.client = client
        self.__categories: dict[int: Category] = {}

    def __getitem__(self, id: int):
        return self.__categories.get(id, None)

    def get_category(self, id: int):
        return self[id]

    def get_all_categories(self):
        return self.__categories.copy()

    def get_all_categories_id(self):
        return self.__categories.keys()

    def add_category(self, category_info) -> None:
        self.__categories[category_info['id']] = Category(self.client, category_info['id'],
                                                          category_info['info_channel_id'],
                                                          category_info['create_channels'])

    async def update_handler(self, category_id: int) -> None:
        category = self.__categories[category_id]
        await category.update_handler()

    async def update_handler_full(self) -> None:
        for category_id, category in self.__categories.items():
            await category.update_handler()

    async def update_message(self, category_id: int) -> None:
        category = self.__categories[category_id]
        await category.update_message()

    async def update_message_full(self) -> None:
        for category_id, category in self.__categories.items():
            await category.update_message()

    def add_temp_channel(self, category_id: int, channel_id: int) -> None:
        category = self.__categories[category_id]
        category.__temp_channels_id.add(channel_id)

    def reset_temp_channels(self, category_id: int) -> None:
        category = self.__categories[category_id]
        category.__temp_channels_id = set()

    async def on_enter(self, category_id: int, channel: discord.VoiceChannel, member: discord.Member) -> None:
        category = self.__categories[category_id]
        await category.on_enter(channel, member)

    async def on_enter_full(self, channel: discord.VoiceChannel, member: discord.Member) -> None:
        for category_id, category in self.__categories.items():
            await category.on_enter(channel, member)

    async def on_exit(self, category_id: int, channel: discord.VoiceChannel, member: discord.Member) -> None:
        category = self.__categories[category_id]
        await category.on_exit(channel, member)

    async def on_exit_full(self, channel: discord.VoiceChannel, member: discord.Member) -> None:
        for category_id, category in self.__categories.items():
            await category.on_exit(channel, member)

    async def create_temp_channel(self, category_id: int, name: str, reason: str = "Просто так") -> None:
        category = self.__categories[category_id]
        await category.create_temp_channel(name, reason)
