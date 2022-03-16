from discord import Embed, Member, Color
from score import get_fine_current_time_msk

BLUE = Color.blue()
RED = Color.red()
GREEN = Color.green()


def make_embed(member: Member, body: str,  color: Color) -> Embed:
    embed = Embed(
        description=body,
        color=color
    )
    embed.set_footer(text=get_fine_current_time_msk())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=str(member), icon_url=member.avatar_url)

    return embed


def neutral_embed(member: Member, body: str) -> Embed:
    embed = Embed(
        description=body,
        color=BLUE,
    )
    embed.set_footer(text=get_fine_current_time_msk())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=str(member), icon_url=member.avatar_url)

    return embed


def positive_embed(member: Member, body: str) -> Embed:
    embed = Embed(
        description=body,
        color=GREEN,
    )
    embed.set_footer(text=get_fine_current_time_msk())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=str(member), icon_url=member.avatar_url)

    return embed


def negative_embed(member: Member, body: str) -> Embed:
    embed = Embed(
        description=body,
        color=RED,
    )
    embed.set_footer(text=get_fine_current_time_msk())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=str(member), icon_url=member.avatar_url)

    return embed
