import discord
from discord.ext import commands
import json

class Anti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def antichannel(self, ctx, action: str):
        guild_id = str(ctx.guild.id)
        config = self.load_config()
        
        # Création de l'Embed
        embed = self.create_embed("AntiChannel", "0x660066")
        
        if action.lower() == "on":
            # Activation de la création de salons pour le serveur actuel
            config[guild_id] = True
            self.save_config(config)
            embed.description = "La création de nouveaux salons est maintenant activée pour ce serveur."
            
            # Vérification et suppression du canal anti s'il existe
            anti_channel = discord.utils.get(ctx.guild.channels, name="nom_du_canal")
            if anti_channel:
                await anti_channel.delete()
            
            await ctx.send(embed=embed)
        elif action.lower() == "off":
            # Désactivation de la création de salons pour le serveur actuel
            config[guild_id] = False
            self.save_config(config)
            embed.description = "La création de nouveaux salons est maintenant désactivée pour ce serveur."
            await ctx.send(embed=embed)
        else:
            embed.description = "Utilisation incorrecte de la commande. Utilisez !antichannel on ou !antichannel off."
            await ctx.send(embed=embed)

    def create_embed(self, title, color):
        # Création de l'Embed avec le titre et la couleur personnalisée
        embed = discord.Embed(
            title=title,
            color=int(color, 16)  # Convertit la couleur hexadécimale en décimal
        )
        # Ajout du logo du bot à l'Embed
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
        return embed

    def load_config(self):
        try:
            with open("Fonction-ipt/channel.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config(self, config):
        with open("Fonction-ipt/channel.json", "w") as f:
            json.dump(config, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        config = self.load_config()
        if config.get(str(channel.guild.id), False):
            await channel.delete()
def setup(bot):
  bot.add_cog(Anti(bot))