import discord


class Role:
    def __init__(self, id: int, time_to_up: int):
        self.__id = id
        self.__time_to_up = time_to_up

    def __repr__(self):
        return f"<ROLE> {self.get_id()}: {self.get_time_to_up()} очков необходимо"

    def __str__(self):
        return f"<ROLE> {self.get_id()} {self.get_time_to_up()}"

    def get_id(self) -> int:
        return self.__id

    def get_time_to_up(self) -> int:
        return self.__time_to_up

    async def get_role(self, member: discord.Member) -> discord.Role:
        guild = member.guild
        role = guild.get_role(self.__id)
        return role
