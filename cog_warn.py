import json
import discord
from discord.ext import commands
import os

class WarnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns = self.load_warns()

    def load_warns(self):
        if not os.path.exists('Fonction-ipt'):
            os.makedirs('Fonction-ipt')

        try:
            with open('Fonction-ipt/warn.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_warns(self):
        with open('Fonction-ipt/warn.json', 'w') as file:
            json.dump(self.warns, file, indent=4)

    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        if ctx.author.guild_permissions.kick_members:
            if member.bot:
                await ctx.send(embed=discord.Embed(
                    title="Avertissement",
                    description="Vous ne pouvez pas avertir un bot.",
                    color=0x660066
                ))
            else:
                if str(ctx.guild.id) not in self.warns:
                    self.warns[str(ctx.guild.id)] = {}

                if str(member.id) not in self.warns[str(ctx.guild.id)]:
                    self.warns[str(ctx.guild.id)][str(member.id)] = []

                self.warns[str(ctx.guild.id)][str(member.id)].append(reason)
                self.save_warns()
                await ctx.send(embed=discord.Embed(
                    title="Avertissement",
                    description=f"{member.mention} a été averti pour la raison suivante:\n\n{reason}",
                    color=0x660066
                ))

                # Envoie un message privé au membre averti
                warn_count = len(self.warns[str(ctx.guild.id)][str(member.id)])
                warn_message = f"Vous avez été averti {warn_count} fois sur le serveur {ctx.guild.name}. Dernier avertissement:\n\n{reason}"
                await member.send(embed=discord.Embed(
                    title="Avertissement",
                    description=warn_message,
                    color=0x660066
                ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Avertissement",
                description="Vous n'avez pas la permission d'avertir des membres.",
                color=0x660066
            ))

    @commands.command()
    async def unwarn(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.kick_members:
            if str(ctx.guild.id) in self.warns and str(member.id) in self.warns[str(ctx.guild.id)]:
                if len(self.warns[str(ctx.guild.id)][str(member.id)]) > 0:
                    self.warns[str(ctx.guild.id)][str(member.id)].pop()
                    self.save_warns()
                    await ctx.send(embed=discord.Embed(
                        title="Retrait d'avertissement",
                        description=f"Le dernier avertissement de {member.mention} a été retiré.",
                        color=0x660066
                    ))
                else:
                    await ctx.send(embed=discord.Embed(
                        title="Retrait d'avertissement",
                        description=f"{member.mention} n'a pas d'avertissements à retirer.",
                        color=0x660066
                    ))
            else:
                await ctx.send(embed=discord.Embed(
                    title="Retrait d'avertissement",
                    description=f"{member.mention} n'a pas d'avertissements sur ce serveur.",
                    color=0x660066
                ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Retrait d'avertissement",
                description="Vous n'avez pas la permission de retirer des avertissements.",
                color=0x660066
            ))

    @commands.command()
    async def warnlist(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.kick_members:
            if str(ctx.guild.id) in self.warns and str(member.id) in self.warns[str(ctx.guild.id)]:
                warns = self.warns[str(ctx.guild.id)][str(member.id)]
                if len(warns) > 0:
                    warn_list = "\n".join([f"{i + 1}. {warn}" for i, warn in enumerate(warns)])
                    await ctx.send(embed=discord.Embed(
                        title=f"Avertissements pour {member.display_name} sur {ctx.guild.name}",
                        description=warn_list,
                        color=0x660066
                    ))
                else:
                    await ctx.send(embed=discord.Embed(
                        title=f"Avertissements pour {member.display_name} sur {ctx.guild.name}",
                        description=f"{member.display_name} n'a pas d'avertissements sur ce serveur.",
                        color=0x660066
                    ))
            else:
                await ctx.send(embed=discord.Embed(
                    title=f"Avertissements pour {member.display_name} sur {ctx.guild.name}",
                    description=f"{member.display_name} n'a pas d'avertissements sur ce serveur.",
                    color=0x660066
                ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Liste des avertissements",
                description="Vous n'avez pas la permission de voir la liste des avertissements.",
                color=0x660066
            ))

def setup(bot):
    bot.add_cog(WarnCog(bot))
