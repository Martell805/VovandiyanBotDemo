import discord


class Category:
    def __init__(self, client: discord.Client, category_id: int,
                 info_channel_id: int, creation_channels_info: dict[int: dict] = None):

        if creation_channels_info is not None:
            self.__creation_channels_info = creation_channels_info
        else:
            self.__creation_channels_info: dict[int: dict] = {}

        self.__temp_channels_id: set[int] = set()

        self.client = client

        self.info_channel_id = info_channel_id
        self.category_id = category_id

    def get_temp_channels_id(self) -> set[int]:
        return self.__temp_channels_id.copy()

    def add_temp_channel(self, id: int) -> None:
        self.__temp_channels_id.add(id)

    def remove_temp_channel(self, id: int) -> None:
        self.__temp_channels_id.remove(id)

    def reset_temp_channels(self) -> None:
        self.__temp_channels_id = set()

    def get_creation_channels_info(self) -> dict[int: dict]:
        return self.__creation_channels_info.copy()

    def add_creation_channel_info(self, creation_channel_id: int, creation_channel_info: dict) -> None:
        self.__creation_channels_info[creation_channel_id] = creation_channel_info

    def remove_creation_channel_info(self, creation_channel_id: int) -> None:
        del self.__creation_channels_info[creation_channel_id]

    def reset_creation_channels_info(self) -> None:
        self.__creation_channels_info = {}

    async def __get_info_message(self) -> tuple[discord.TextChannel, discord.Message | None]:
        info_channel = self.client.get_channel(self.info_channel_id)
        async for message in info_channel.history(limit=10):
            if message.author == self.client.user:
                return info_channel, message
        return info_channel, None

    async def update_handler(self) -> None:
        info_channel, info_message = await self.__get_info_message()
        while not info_message:
            await info_channel.send('<TEMP_CHANNELS> ')
            info_channel, info_message = await self.__get_info_message()
        info_message_text = info_message.content

        for channel_id in info_message_text.split()[1:]:
            self.add_temp_channel(int(channel_id))

    async def update_message(self) -> None:
        info_channel, info_message = await self.__get_info_message()
        while not info_message:
            await info_channel.send('<TEMP_CHANNELS> ')
            info_channel, info_message = await self.__get_info_message()

        new_text = '<TEMP_CHANNELS> '
        for channel_id in self.__temp_channels_id:
            new_text += str(channel_id) + ' '

        await info_message.edit(content=new_text)

    @staticmethod
    def __is_empty_channel(channel: discord.VoiceChannel) -> bool:
        return len(channel.members) == 0

    async def on_enter(self, channel: discord.VoiceChannel, member: discord.Member) -> None:
        channel_info = self.__creation_channels_info.get(channel.id, None)

        if channel_info is None:
            return

        guild = channel.guild
        category = channel.category

        reason = f"{member.name} зашёл в {channel.name}"

        overwrites = {
            member: discord.PermissionOverwrite(manage_channels=True, manage_permissions=True, move_members=True)
        }

        new_channel = await guild.create_voice_channel(name=channel_info['name_pattern'].format(member.name),
                                                       user_limit=channel_info['user_limit'],
                                                       category=category, reason=reason, overwrites=overwrites)

        await member.move_to(new_channel)

        self.add_temp_channel(new_channel.id)
        await self.update_message()

    async def on_exit(self, channel: discord.VoiceChannel, member: discord.Member) -> None:
        if channel is None:
            return

        if channel.category_id != self.category_id:
            return

        if channel.id not in self.__temp_channels_id:
            return

        if not self.__is_empty_channel(channel):
            return

        reason = f"С канала {channel.mention} все вышли"
        await channel.delete(reason=reason)
        self.__temp_channels_id.remove(channel.id)
        await self.update_message()

    async def create_temp_channel(self, name: str, reason: str = "Просто так"):
        info_channel, info_message = await self.__get_info_message()
        guild = info_channel.guild
        category = info_channel.category

        new_channel = await guild.create_voice_channel(name, category=category, reason=reason)
        self.add_temp_channel(new_channel.id)
        await self.update_message()
