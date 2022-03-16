import discord

import role_paths
from config import CHANNELS_ID, CATEGORIES


async def up_role(client, message: discord.Message, member_id, *args):
    guild = message.guild
    member = guild.get_member(int(member_id[3:-1]))

    role_path = client.role_path_handler
    role, role_number = role_path.get_highest_role(member)

    initiator = message.author
    initiator_role, initiator_role_number = role_path.get_highest_role(initiator)

    if not role_paths.check_role_changing_permission(initiator):
        await message.channel.send(f"{initiator.mention}, у вас недостаточно прав для использования этой команды")
        return

    if initiator_role_number <= role_number:
        await message.channel.send(f"{initiator.mention}, вы не можете выдавать роли выше своей")
        return

    if role_path.is_max_role(role.get_id()):
        await message.channel.send(f"{initiator.mention}, {member.name} уже получил максимальную роль")
        return

    user = client.saver[member]
    user.set_score(role_path[role_number + 1].get_time_to_up())
    await client.saver.update_message()

    await role_path.update_role(member)

    role, role_number = role_path.get_highest_role(member)
    role = await role.get_role(member)
    print(f"{member.name} был повышен {message.author.name} до {role.name}")
    await message.channel.send(f"{member.name} был успешно повышен до {role.name}")


async def down_role(client, message: discord.Message, member_id, *args):
    guild = message.guild
    member = guild.get_member(int(member_id[3:-1]))

    role_path = client.role_path_handler
    role, role_number = role_path.get_highest_role(member)

    initiator = message.author
    initiator_role, initiator_role_number = role_path.get_highest_role(initiator)

    if not role_paths.check_role_changing_permission(initiator):
        await message.channel.send(f"{initiator.mention}, у вас недостаточно прав для использования этой команды")
        return

    if initiator_role_number <= role_number:
        await message.channel.send(f"{initiator.mention}, вы не можете понижать роли выше своей")
        return

    if role_number == 0 or role_number is None:
        await message.channel.send(f"{initiator.mention}, {member.name} некуда понижать")
        return

    user = client.saver[member]
    user.set_score(role_path[role_number - 1].get_time_to_up())
    await client.saver.update_message()

    await role_path.update_role(member)

    role, role_number = role_path.get_highest_role(member)
    role = await role.get_role(member)
    print(f"{member.name} был понижен {message.author.name} до {role.name}")
    await message.channel.send(f"{member.name} был успешно понижен до {role.name}")


async def edit_channel_name(client, message: discord.Message, *name):
    if message.channel.id != CHANNELS_ID['custom']:
        return

    initiator = message.author
    channel = initiator.voice.channel

    reason = f"Вызван командой {initiator.name}"

    category = client.category_handler[channel.category_id]

    if channel.category.id == CATEGORIES['custom']['id'] and channel.id in category.get_temp_channels_id():
        await channel.edit(name=' '.join(name), reason=reason)


async def edit_channel_ul(client, message: discord.Message, user_limit, *args):
    if message.channel.id != CHANNELS_ID['custom']:
        return

    initiator = message.author
    channel = initiator.voice.channel

    reason = f"Вызван командой {initiator.name}"

    if channel.category_id == CATEGORIES['custom']['id']:
        await channel.edit(user_limit=int(user_limit), reason=reason)


async def edit_channel_br(client, message: discord.Message, bitrate, *args):
    if message.channel.id != CHANNELS_ID['custom']:
        return

    initiator = message.author
    channel = initiator.voice.channel

    reason = f"Вызван командой {initiator.name}"

    if channel.category_id == CATEGORIES['custom']['id']:
        await channel.edit(bitrate=int(bitrate), reason=reason)


async def edit_channel(client, message: discord.Message, user_limit, *name):
    if message.channel.id != CHANNELS_ID['custom']:
        return

    initiator = message.author
    channel = initiator.voice.channel

    reason = f"Вызван командой {initiator.name}"

    if channel.category.id == CATEGORIES['custom']['id']:
        await channel.edit(name=' '.join(name), user_limit=int(user_limit), reason=reason)


async def print_score(client, message: discord.Message, *args):
    other_member = len(args) != 0
    if other_member:
        id = int(args[0][3:-1])
        guild = message.guild
        target = guild.get_member(id)
    else:
        target = message.author

    current_role, current_role_number = client.role_path_handler.get_highest_role(target)
    member_score = client.saver[target].get_score()
    current_role_ds = await current_role.get_role(target)

    if client.role_path_handler.is_max_role(current_role.get_id()):
        if other_member:
            text = f'У {target.name} сейчас {member_score} очков. Он уже достиг максимальной роли ' \
                   f'{current_role_ds.name}'
        else:
            text = f'{target.mention}, сейчас у вас {member_score} очков. Вы уже достигли максимальной роли ' \
                   f'{current_role_ds.name}, поздравляем!'

    else:
        next_role = client.role_path_handler[current_role_number + 1]
        next_role_ds = await next_role.get_role(target)

        if other_member:
            text = f'У {target.name} сейчас {member_score} очков. До следующей роли - ' \
                   f'{next_role_ds.name} - ' \
                   f'осталось {next_role.get_time_to_up() - member_score} очков'
        else:
            text = f'{target.mention}, сейчас у вас {member_score} очков. До следующей роли - ' \
                   f'{next_role_ds.name} - ' \
                   f'вам осталось {next_role.get_time_to_up() - member_score} очков'

    await message.channel.send(text)


async def roll_dice(client, message: discord.Message, *args):
    initiator = message.author
    channel = message.channel

    roll = client.duel_handler[initiator].roll()

    text = f"{initiator.mention}, вы выбросили {roll} из 100"

    await channel.send(text)


async def dice_duel(client, message: discord.Message, opponent, *args):
    initiator = message.author
    channel = message.channel
    guild = message.guild

    opponent_id = int(opponent[3:-1])
    opponent = guild.get_member(opponent_id)

    await client.duel_handler.duel(channel, initiator, opponent)


async def duel_stats(client, message: discord.Message, *args):
    other_member = len(args) != 0

    if other_member:
        id = int(args[0][3:-1])
        guild = message.guild
        target = guild.get_member(id)
    else:
        target = message.author

    duel_user = client.duel_handler[target]

    if other_member:
        text = f'{target.name} сыграл {duel_user.get_games()} игр, ' \
               f'из которых выиграл {duel_user.get_wins()}. ' \
               f'Его процент побед - {duel_user.get_winrate()}.'
    else:
        text = f'{target.mention}, вы сыграли {duel_user.get_games()} игр, ' \
               f'из которых выиграли {duel_user.get_wins()}. ' \
               f'Ваш процент побед - {duel_user.get_winrate()}. '

    await message.channel.send(text)


async def help(client, message: discord.Message, *args):
    text = f"Доступные команды:\n" \
           f"1. !roll_dice - выбросить случайное значение от 0 до 100\n" \
           f"2. !dice_duel <@пользователь> - каждый выбросит случайное число от 0 до 100 и будет выбран победитель\n" \
           f"3. !duel_stats  <@пользователь (если не указывать - покажет для вас)> - покажет вашу статистику дуэлей\n" \
           f"4. !print_stats <@пользователь (если не указывать - покажет для вас)> - покажет, сколько очков " \
           f"вам осталось получить до следующего звания\n" \

    await message.channel.send(text)
