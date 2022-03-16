import discord


class RolePost:
    def __init__(self, client: discord.Client, post_id: int, reactions: dict[str: int] = None):
        self.client = client
        self.__post_id = post_id

        if reactions is None:
            self.__reactions = {}
        else:
            self.__reactions = reactions

    def add_reaction(self, reaction: str, role_id: int) -> None:
        self.__reactions[reaction] = role_id

    def remove_reaction(self, reaction: str) -> None:
        del self.__reactions[reaction]

    def get_post_id(self) -> int:
        return self.__post_id

    def get_reaction_role_id(self, reaction: str) -> int:
        return self.__reactions[reaction]

    def __getitem__(self, reaction: str) -> int:
        return self.__reactions[reaction]

    def get_all_reaction_roles_id(self) -> dict[str: int]:
        return self.__reactions.copy()

    def reset_reactions(self) -> None:
        self.__reactions = {}

    async def on_add(self, payload) -> None:
        if payload.message_id != self.get_post_id():
            return

        emoji = str(payload.emoji)

        if emoji not in self.__reactions:
            return

        guild = self.client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        role = guild.get_role(self.__reactions[emoji])

        reason = f'Пользователь {member.name} получил роль {role.name} за реакцию {emoji}!'
        await member.add_roles(role, reason=reason)
        print(reason)

    async def on_remove(self, payload) -> None:
        if payload.message_id != self.__post_id:
            return

        emoji = str(payload.emoji)

        if emoji not in self.__reactions:
            return

        guild = self.client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        role = guild.get_role(self.__reactions[emoji])

        reason = f'Пользователь {member.name} потерял роль {role.name} за реакцию {emoji}!'
        await member.remove_roles(role, reason=reason)
        print(reason)
