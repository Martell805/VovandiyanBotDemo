VERSION = "1.6.5.3"


import discord

from config import CHANNELS_ID, TOKEN, PREFIX, REACTION_POSTS, CATEGORIES, ROLES_INFO
import answers

from role_posts import RolePostHandler
from categories import CategoryHandler
from score import ScoreSaver
from commands import CommandHandler
from role_paths import RolePathHandler
from duels import DuelHandler

from utils.embeds import neutral_embed, positive_embed, negative_embed


class VovandiyanBot(discord.Client):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True
        intents.guild_reactions = True

        super().__init__(*args, **kwargs, intents=intents)

        self.saver = ScoreSaver(self, CHANNELS_ID['score'])
        self.duel_handler = DuelHandler(self, CHANNELS_ID['score'], [CHANNELS_ID['duels']])
        self.command_handler = CommandHandler(self, PREFIX)

        self.category_handler = CategoryHandler(self)
        self.role_post_handler = RolePostHandler(self)
        self.role_path_handler = RolePathHandler(self, self.saver, ROLES_INFO)

    async def on_ready(self):
        print(f'Залогинился как {self.user}, версия {VERSION}')

        await self.saver.update_saver()
        await self.duel_handler.update_saver()

        self.category_handler.add_category(CATEGORIES['custom'])
        self.category_handler.add_category(CATEGORIES['apex'])
        self.category_handler.add_category(CATEGORIES['csgo'])

        await self.category_handler.update_handler_full()

        self.role_post_handler.add_post(REACTION_POSTS['main'])

        self.command_handler.add_command('up_role', answers.up_role)
        self.command_handler.add_command('down_role', answers.down_role)
        self.command_handler.add_command('edit_channel_name', answers.edit_channel_name)
        self.command_handler.add_command('edit_channel_ul', answers.edit_channel_ul)
        self.command_handler.add_command('edit_channel_br', answers.edit_channel_br)
        self.command_handler.add_command('edit_channel', answers.edit_channel)
        self.command_handler.add_command('print_score', answers.print_score)
        self.command_handler.add_command('roll_dice', answers.roll_dice)
        self.command_handler.add_command('dice_duel', answers.dice_duel)
        self.command_handler.add_command('duel_stats', answers.duel_stats)
        self.command_handler.add_command('help', answers.help)

    async def on_member_join(self, member):
        await self.role_path_handler.give_starter_role(member)

        channel = self.get_channel(CHANNELS_ID['new_members'])
        await channel.send(embed=positive_embed(member, f'{member.mention} пришёл на сервер!'))

    async def on_member_remove(self, member):
        channel = self.get_channel(CHANNELS_ID['new_members'])
        await channel.send(embed=negative_embed(member, f'{member.mention} ушёл с сервера!'))

    async def on_raw_reaction_add(self, payload):
        await self.role_post_handler.on_add(payload)

    async def on_raw_reaction_remove(self, payload):
        await self.role_post_handler.on_remove(payload)

    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:
            if not before.self_mute and after.self_mute:
                await self.saver.on_member_exit(member)
            elif before.self_mute and not after.self_mute:
                await self.saver.on_member_enter(member)
            return

        if before.channel != after.channel:
            if before.channel is None:
                await self.saver.on_member_enter(member)
                embed_body = f'{member.mention} вошёл в канал {after.channel.name}'
                await self.role_path_handler.update_role(member)
                await self.category_handler.on_enter_full(after.channel, member)

            elif after.channel is None:
                embed_body = f'{member.mention} вышел с канала {before.channel.name}'
                if not before.afk:
                    await self.saver.on_member_exit(member)
                    await self.role_path_handler.update_role(member)

                await self.category_handler.on_exit_full(before.channel, member)
            else:
                embed_body = f'{member.mention} сменил канал с {before.channel.name} на {after.channel.name}'

                await self.category_handler.on_exit_full(before.channel, member)
                await self.category_handler.on_enter_full(after.channel, member)

            raports_channel = self.get_channel(CHANNELS_ID['raports'])
            await raports_channel.send(embed=neutral_embed(member, embed_body))

    async def on_message(self, message):
        await self.command_handler.answer(message)


def main():
    bot = VovandiyanBot()
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
