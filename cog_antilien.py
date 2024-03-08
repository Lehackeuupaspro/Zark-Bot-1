from discord.ext import commands
import json
import discord

class Antilien(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()
        self.cog_category = "AntiLien"

    def load_config(self):
        try:
            with open("Fonction-ipt/config.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_config(self):
        with open("Fonction-ipt/config.json", "w") as file:
            json.dump(self.config, file, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author == message.guild.owner:
            return

        if str(message.guild.id) in self.config:
            antilink_config = self.config[str(message.guild.id)]
            if antilink_config.get("antilink_enabled", False):
                allowed_links = antilink_config.get("allowed_links", [])

                if not any(link in message.content for link in allowed_links):
                    if any(word in message.content for word in ["http://", "https://", "www."]) and "gift" not in message.content.lower():
                        await message.delete()
                        embed = discord.Embed(
                            title="Lien non autorisé",
                            description=f"{message.author.mention}, les liens ne sont pas autorisés ici.",
                            color=0x660066
                        )
                        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
                        sent_message = await message.channel.send(embed=embed)
                        await sent_message.delete(delay=5)



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def antilien(self, ctx, option: str):
        guild_id = str(ctx.guild.id)
        self.config[guild_id] = {
            "antilink_enabled": False,
            "allowed_links": []
        }

        if option.lower() == "on":
            self.config[guild_id]["antilink_enabled"] = True
            self.save_config()
            embed = discord.Embed(
                title="Fonction anti-lien activée",
                description="La fonction anti-lien a été activée avec succès.",
                color=0x660066
            )
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
            await ctx.send(embed=embed)
        elif option.lower() == "off":
            self.config[guild_id]["antilink_enabled"] = False
            self.save_config()
            embed = discord.Embed(
                title="Fonction anti-lien désactivée",
                description="La fonction anti-lien a été désactivée avec succès.",
                color=0x660066
            )
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Option invalide",
                description="Utilisez `on` ou `off`.",
                color=0x660066
            )
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addlink(self, ctx, link: str):
        guild_id = str(ctx.guild.id)
        if guild_id in self.config:
            allowed_links = self.config[guild_id]["allowed_links"]

            if link in allowed_links:
                embed = discord.Embed(
                    title="Lien déjà autorisé",
                    description=f"Le lien `{link}` est déjà dans la liste des liens autorisés.",
                    color=0x660066
                )
                await ctx.send(embed=embed)
            else:
                if any(link in message.content for link in allowed_links):
                    embed = discord.Embed(
                        title="Lien autorisé",
                        description=f"Le lien `{link}` a été ajouté à la liste des liens autorisés.",
                        color=0x660066
                    )
                    await ctx.send(embed=embed)
                else:
                    allowed_links.append(link)
                    self.save_config()
                    embed = discord.Embed(
                        title="Lien autorisé ajouté",
                        description=f"Lien : {link}",
                        color=0x660066
                    )
                    await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="La fonction anti-lien n'est pas activée. Utilisez `antilien on` d'abord.",
                color=0x660066
            )
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
            sent_message = await ctx.send(embed=embed)
            await sent_message.delete(delay=5)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removelink(self, ctx, link: str):
        guild_id = str(ctx.guild.id)
        if guild_id in this.config:
            allowed_links = self.config[guild_id]["allowed_links"]
            if link in allowed_links:
                allowed_links.remove(link)
                self.save_config()
                embed = discord.Embed(
                    title="Lien autorisé supprimé",
                    description=f"Lien : {link}",
                    color=0x660066
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Erreur",
                    description="Le lien spécifié n'est pas dans la liste des liens autorisés.",
                    color=0x660066
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="La fonction anti-lien n'est pas activée. Utilisez `antilien on` d'abord.",
                color=0x660066
            )
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
            sent_message = await ctx.send(embed=embed)
            await sent_message.delete(delay=5)

    @commands.command()
    async def listlinks(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in this.config:
            allowed_links = self.config[guild_id]["allowed_links"]
            if allowed_links:
                links_list = "\n".join(allowed_links)
                embed = discord.Embed(
                    title="Liste des liens autorisés",
                    description=links_list,
                    color=0x660066
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Liste des liens autorisés",
                    description="Aucun lien autorisé dans la liste.",
                    color=0x660066
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="La fonction anti-lien n'est pas activée.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def helplink(self, ctx):
        embed = discord.Embed(
            title="Aide pour les commandes de la fonction anti-lien",
            description="Ce cog gère la détection et la gestion des liens dans les messages.",
            color=0x660066
        )
        embed.add_field(
            name="Commandes disponibles :",
            value=(
                "`antilien on|off`: Active ou désactive la fonction anti-lien.\n"
                "`addlink <lien>`: Ajoute un lien à la liste des liens autorisés.\n"
                "`removelink <lien>`: Supprime un lien de la liste des liens autorisés.\n"
                "`listlinks`: Affiche la liste des liens autorisés."
            ),
            inline=False
        )
        await ctx.send(embed=embed)

    @addlink.error
    async def addlink_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Erreur de permissions",
                description="Vous n'avez pas les permissions nécessaires pour utiliser cette commande.",
                color=0x660066  # Couleur personnalisée (bleu)
            )
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
            await ctx.send(embed=embed)

    async def send_error_embed(self, ctx, title, description):
        embed = discord.Embed(
            title=title,
            description=description,
            color=0x660066  # Couleur personnalisée (bleu)
        )
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
        await ctx.send(embed=embed)

    @addlink.error 
    async def addlink_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await self.send_error_embed(ctx, "Erreur de permissions", "Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")

    @listlinks.error
    async def listlinks_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await self.send_error_embed(ctx, "Erreur de permissions", "Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")

    @removelink.error
    async def removelink_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await self.send_error_embed(ctx, "Erreur de permissions", "Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")

    @antilien.error
    async def antilien_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await self.send_error_embed(ctx, "Erreur de permissions", "Vous n'avez pas les permissions nécessaires pour utiliser cette commande.")



def setup(bot):
  bot.add_cog(CogAntilien(bot))