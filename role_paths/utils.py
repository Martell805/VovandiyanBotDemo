import discord


def check_role_changing_permission(member: discord.Member) -> bool:
    for role in member.roles:
        if role.permissions.manage_roles:
            return True
    return False
