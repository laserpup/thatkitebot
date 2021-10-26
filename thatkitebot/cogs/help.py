# ------------------------------------------------------------------------------
#  MIT License
#
#  Copyright (c) 2021 dunnousername
#  Copyright (c) 2021 ThatRedKite

#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# ------------------------------------------------------------------------------

import discord
from discord.ext import commands
import random

info = {
    'repo': 'https://github.com/ThatRedKite/thatkitebot',
    'name': 'ThatKiteBot'
}


class BetterHelpCommand(commands.HelpCommand):
    async def send_embed(self, embed):
        embed.colour = discord.Colour.random()
        await self.get_destination().send(embed=embed)

    def blank_line(self, embed):
        embed.add_field(name='_ _', value='_ _', inline=False)

    def signature(self, command: commands.Command):
        out = [command.qualified_name]
        params = command.clean_params or {}
        for name, param in params.items():
            # slightly copied from discord.py
            greedy = isinstance(param.annotation, commands.converter._Greedy)
            if param.default is not param.empty:
                should_print = param.default if isinstance(param.default, str) else param.default is not None
                if should_print:
                    out.append(f'[{name}={param.default}]{"..." if greedy else ""}')
                else:
                    out.append(f'[{name}]')
            elif param.kind == param.VAR_POSITIONAL:
                out.append(f'<{name}...>')
            elif greedy:
                out.append(f'[{name}]...')
            else:
                out.append(f'<{name}>')
        return ' '.join(out)

    async def send_bot_help(self, mapping):
        e = discord.Embed(title=info['name'])
        e.add_field(name='Contribute at', value=info['repo'], inline=False)
        cogs = [(cog, await self.filter_commands(mapping[cog])) for cog in mapping.keys()]
        cogs = [x for x in cogs if len(x[1]) > 0]
        for i, (cog, cmds) in enumerate(cogs):
            if i % 2 == 0:
                self.blank_line(e)
            h = '\n'.join([cmd.name for cmd in cmds])
            if cog is None:
                e.add_field(name='builtin', value=h, inline=True)
            else:
                e.add_field(name=cog.qualified_name, value=h, inline=True)
        if random.random() < 0.9:
            e.set_footer(text='Made with ❤️')
        else:
            e.set_footer(text='Made with 🍆')
        await self.send_embed(e)

    async def send_cog_help(self, cog: commands.Cog):
        e = discord.Embed(title=cog.qualified_name)
        e.add_field(name='Cog', value=cog.qualified_name, inline=True)
        e.add_field(name='`in_code`', value=f'`{cog.__class__.__name__}`', inline=True)
        e.add_field(name='Commands', value='_ _', inline=False)
        for cmd in await self.filter_commands(cog.get_commands()):
            e.add_field(name=cmd, value=(cmd.help or '[no help]'), inline=False)
        await self.send_embed(e)

    async def send_group_help(self, group: commands.Group):
        e = discord.Embed(title=group.qualified_name)
        e.add_field(name='Command Group', value=group.qualified_name, inline=True)
        e.add_field(name='Help', value=(group.help or '[no help]'), inline=False)
        e.add_field(name='Subcommands', value='_ _', inline=False)
        for command in await self.filter_commands(group.commands):
            command: commands.Command
            e.add_field(name=self.signature(command), value=(command.help or '[no help]'), inline=False)
        await self.send_embed(e)

    async def send_command_help(self, command: commands.Command):
        e = discord.Embed(title=(command.qualified_name or command.name))
        e.add_field(name='Name', value=(command.qualified_name or command.name), inline=False)
        e.add_field(name='Signature', value=(self.signature(command)), inline=False)
        e.add_field(name='Help', value=(command.help or '[no help]'), inline=False)
        await self.send_embed(e)


class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        help_command = BetterHelpCommand()
        help_command.cog = self
        self.bot.help_command = help_command


def setup(bot):
    bot.add_cog(HelpCog(bot))