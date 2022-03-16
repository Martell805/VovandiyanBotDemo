import discord
import score

from .role import Role


class RolePathHandler:
    def __init__(self, client, saver: score.ScoreSaver, roles_info: dict[int: int]):
        self.__client = client
        self.__saver = saver
        self.__roles = [Role(role_id, roles_info[role_id]) for role_id in roles_info]

    async def give_starter_role(self, member: discord.Member):
        start_role = await self.__roles[0].get_role(member)

        reason = f'Пользователь {member.name} получил роль {start_role.name} за присоединение к серверу!'
        await member.add_roles(start_role, reason=reason)

    def __getitem__(self, number: int) -> Role | None:
        return self.__roles[number]

    def get_role(self, id: int) -> Role | None:
        for role in self.__roles:
            if role.get_id() == id:
                return role
        return None

    def is_max_role(self, id) -> bool:
        return self.get_role_number(id) == len(self.__roles) - 1

    def get_role_number(self, id: int) -> int:
        if self.get_role(id) in self.__roles:
            return self.__roles.index(self.get_role(id))
        return -1

    def get_highest_role(self, member: discord.Member) -> (Role, int):
        highest_role_number = -1
        for role in member.roles:
            n_cur_role = self.get_role_number(role.id)
            if n_cur_role == -1:
                continue
            if n_cur_role > highest_role_number:
                highest_role_number = n_cur_role

        return self[highest_role_number], highest_role_number

    def choose_role(self, member: discord.Member) -> (Role, int):
        user = self.__saver[member]
        prev_role = self.__roles[0]
        for role in self.__roles:
            if user.get_score() < role.get_time_to_up():
                break
            prev_role = role
        return prev_role, self.get_role_number(prev_role.get_id())

    async def update_role(self, member: discord.Member) -> None:
        if member.bot:
            return

        current_role, current_role_number = self.get_highest_role(member)
        current_role_ds = await current_role.get_role(member)
        new_role, new_role_number = self.choose_role(member)

        if new_role is None:
            return

        new_role_ds = await new_role.get_role(member)

        if current_role_number == new_role_number:
            return

        if current_role_number > new_role_number:
            self.__saver[member].set_score(current_role.get_time_to_up())
            await self.__saver.update_message()
            return

        if current_role_number < new_role_number:
            reason = f'{member.name} получил достаточно опыта для повышения с {current_role_ds} до {new_role_ds}'
        else:
            reason = f'{member.name} потерял достаточно опыта для понижения с {current_role_ds} до {new_role_ds}'

        await member.remove_roles(current_role_ds, reason=reason)
        await member.add_roles(new_role_ds, reason=reason)
