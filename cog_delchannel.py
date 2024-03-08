import discord
from discord.ext import commands
import json
import os

class AntiDeleteChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists("Fonction-ipt/delete.json"):
            with open("Fonction-ipt/delete.json", "r") as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open("Fonction-ipt/delete.json", "w") as f:
            json.dump(self.config, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild_id = str(channel.guild.id)
        if self.config.get(guild_id, False):
            await channel.clone()
            embed = discord.Embed(
                title="Protection des salons activée",
                description="Ce salon ne peut pas être supprimé.",
                color=0x660066
            )
            await channel.send(embed=embed)

    @commands.command()
    async def deletechannel(self, ctx, action: str):
        guild_id = str(ctx.guild.id)

        if action.lower() == "on":
            self.config[guild_id] = True
            self.save_config()
            embed = discord.Embed(
                title="Protection des salons activée",
                description="La protection des salons est activée. Les salons ne peuvent pas être supprimés.",
                color=0x660066
            )
            await ctx.send(embed=embed)
        elif action.lower() == "off":
            self.config[guild_id] = False
            self.save_config()
            embed = discord.Embed(
                title="Protection des salons désactivée",
                description="La protection des salons est désactivée. Les salons peuvent être supprimés.",
                color=0x660066
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Utilisation incorrecte de la commande",
                description="Utilisez !deletechannel on ou !deletechannel off.",
                color=0x660066
            )
            await ctx.send(embed=embed)


def setup(bot):
  bot.add_cog(AntiDeleteChannel(bot))