import discord
from discord.ext import commands

class Utill(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        roles_info = []
        for role in member.roles:
            if role.name != "@everyone":
                roles_info.append(f"{role.mention} ({role.name})")

        permissions = member.guild_permissions
        permission_list = [perm for perm, value in permissions if value]

        embed = discord.Embed(title=f"Informations sur {member.display_name}", color=0x660066)
        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="Nom d'utilisateur", value=member.name, inline=True)
        embed.add_field(name="Surnom", value=member.display_name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Compte créé le", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="A rejoint le serveur le", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="Rôles", value='\n'.join(roles_info) if roles_info else "Aucun rôle", inline=False)

        await ctx.send(embed=embed)


    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        guild = ctx.guild

        embed = discord.Embed(title=f"Informations sur le serveur {guild.name}", color=0x660066)
        embed.set_thumbnail(url=guild.icon_url)

        embed.add_field(name="Nom du serveur", value=guild.name, inline=True)
        embed.add_field(name="ID du serveur", value=guild.id, inline=True)

        if guild.owner:
            owner_name = guild.owner.display_name if guild.owner.display_name != guild.owner.name else guild.owner.name
            embed.add_field(name="Propriétaire", value=f"{owner_name} ({guild.owner.mention})", inline=True)
        else:
            embed.add_field(name="Propriétaire", value="Non spécifié", inline=True)

        embed.add_field(name="Nombre de membres", value=guild.member_count, inline=True)
        embed.add_field(name="Nombre de salles textuelles", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Nombre de salles vocales", value=len(guild.voice_channels), inline=True)

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(InfoCog(bot))
