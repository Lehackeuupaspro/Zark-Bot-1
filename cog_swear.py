import discord
from discord.ext import commands
import os.path
import json
from unidecode import unidecode

class Swear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()

    def load_config(self):
        try:
            with open("Fonction-ipt/swear.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_config(self):
        with open("Fonction-ipt/swear.json", "w") as file:
            json.dump(self.config, file, indent=4)

    def create_swear_list_directory(self):
        if not os.path.exists("swear-list"):
            os.makedirs("swear-list")

    def load_swear_list(self, guild_id):
        file_path = os.path.join("swear-list", f"swear_{guild_id}.txt")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_swear_list(self, guild_id, swear_list):
        file_path = os.path.join("swear-list", f"swear_{guild_id}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(swear_list))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        lowercase_content = message.content.lower()
        guild_id = str(message.guild.id)
        swear_enabled = self.config.get(guild_id, {}).get("antiswear_enabled", False)

        if swear_enabled:
            swear_list = self.load_swear_list(guild_id)
            for swear_word in swear_list:
                if swear_word in lowercase_content:
                    await message.delete()
                    embed = discord.Embed(
                        title="Message Supprimé",
                        description=f"{message.author.mention}, veuillez éviter d'utiliser des termes offensants.",
                        color=0x660066
                    )
                    await message.channel.send(embed=embed)
                    break

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def antiswear(self, ctx):
        guild_id = str(ctx.guild.id)
        current_state = self.config.get(guild_id, {}).get("antiswear_enabled", False)
        new_state = not current_state
        self.config[guild_id] = {"antiswear_enabled": new_state}
        self.save_config()

        state_text = "activée" if new_state else "désactivée"
        embed = discord.Embed(
            title="Détection des insultes",
            description=f"La détection des insultes a été {state_text}.",
            color=0x660066
        )

        # Ajouter une image au bot dans l'embed
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")

        if new_state:
            default_swear_list = ["Connard", "Batard", "Enfoire", "Petasse", "Abruti"]
            swear_list = self.load_swear_list(guild_id)

            for word in default_swear_list:
                lowercase_word = word.lower()
                normalized_word = unidecode(lowercase_word)  # Normaliser le mot
                if normalized_word not in swear_list:
                    swear_list.append(normalized_word)

            self.save_swear_list(guild_id, swear_list)

            embed.add_field(
                name="Mots interdits ajoutés",
                value="5 mots interdits ont été ajoutés à la liste d'insultes par défaut **connard, batard, enfoire, petasse, abruti.**",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def listswear(self, ctx):
        guild_id = str(ctx.guild.id)
        swear_list = self.load_swear_list(guild_id)
        
        if swear_list:
            list_text = "\n".join(swear_list)
        else:
            list_text = "Aucun mot interdit dans la liste."
        
        embed = discord.Embed(
            title="Liste des mots interdits",
            description=list_text,
            color=0x660066
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addswear(self, ctx, *, word: str):
        guild_id = str(ctx.guild.id)
        swear_list = self.load_swear_list(guild_id)
        lowercase_word = word.lower()
        swear_list.append(lowercase_word)
        self.save_swear_list(guild_id, swear_list)
        await ctx.send(f"Le mot '{word}' a été ajouté à la liste d'insultes.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removeswear(self, ctx, *, word: str):
        guild_id = str(ctx.guild.id)
        swear_list = self.load_swear_list(guild_id)
        lowercase_word = word.lower()
        
        if lowercase_word in swear_list:
            swear_list.remove(lowercase_word)
            self.save_swear_list(guild_id, swear_list)
            await ctx.send(f"Le mot '{word}' a été supprimé de la liste d'insultes.")
        else:
            await ctx.send(f"Le mot '{word}' n'existe pas dans la liste d'insultes.")

    
    @commands.command()
    async def helpswear(self, ctx):
        embed = discord.Embed(
            title="Aide pour les commandes de détection des insultes",
            description="Ce cog gère la détection des insultes et les mots interdits.",
            color=0x660066
        )
        embed.add_field(
            name="Commandes disponibles :",
            value=(
                "`antiswear<on,off>`: Active ou désactive la détection des insultes.\n"
                "`listswear`: Affiche la liste des mots interdits.\n"
                "`addswear <mot>`: Ajoute un mot à la liste des mots interdits.\n"
                "`removeswear <mot>`: Supprime un mot de la liste des mots interdits."
            ),
            inline=False
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Swear(bot))
