import discord
from discord.ext import commands
import json
import random


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.current_category_message = None 
        self.command_errors = {
            commands.MissingRequiredArgument: ("Erreur d'Argument", "Il manque un argument requis."),
            commands.BadArgument: ("Erreur d'Argument", "L'argument fourni est incorrect."),
            commands.CommandNotFound: ("Commande introuvable", "La commande spécifiée n'a pas été trouvée."),
            commands.MissingPermissions: ("Permissions insuffisantes", "Vous n'avez pas les permissions nécessaires pour exécuter cette commande."),
            commands.NotOwner: ("Non autorisé", "Vous n'êtes pas autorisé à exécuter cette commande."),
        }
        



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, membre: discord.Member, *, raison=None):
        """Expulser un membre du serveur."""
        await membre.kick(reason=raison)

        # Créer un Embed amélioré pour la réponse
        embed = discord.Embed(
            title="Membre Expulsé",
            description=f"{membre.mention} a été expulsé.",
            color=discord.Color(0x660066)  # Couleur violette
        )

        # Ajouter un champ avec des informations supplémentaires (vous pouvez personnaliser ceci selon vos besoins)
        embed.add_field(name="Raison de l'expulsion", value=raison if raison else "Aucune raison spécifiée", inline=False)

        # Inclure le nom du modérateur
        embed.set_footer(text=f"Modérateur : {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, membre: discord.Member, *, raison=None):
        """Bannir un membre du serveur."""
        await membre.ban(reason=raison)

        embed = discord.Embed(
            title="Membre Banni",
            description=f"{membre.mention} a été banni.",
            color=0x660066  # Couleur spécifiée (0x6A0DAD est une couleur violette)
        )

        # Ajoute plus d'informations dans l'embedding
        embed.add_field(name="Raison du bannissement", value=raison if raison else "Aucune raison spécifiée", inline=False)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=False)
        embed.add_field(name="Serveur", value=ctx.guild.name, inline=False)

        # Image du membre banni (optionnelle)
        if membre.avatar_url:
            embed.set_thumbnail(url=membre.avatar_url)

        await ctx.send(embed=embed)



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, membre):
        """Lever le bannissement d'un membre du serveur."""
        bans = await ctx.guild.bans()
        for ban_entry in bans:
            user = ban_entry.user
            if membre.lower() in user.name.lower():
                await ctx.guild.unban(user)
                
                embed = discord.Embed(
                    title="Membre Débanni",
                    description=f"{user.mention} a été débanni.",
                    color=0x660066  # Couleur spécifiée (0x6A0DAD est une couleur violette)
                )
                await ctx.send(embed=embed)
                return
        
        await ctx.send(f"Impossible de trouver un membre banni avec le nom '{membre}'.")


    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Erreur de Permissions", description="Vous n'avez pas la permission d'utiliser cette commande.", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title="Membre Introuvable", description="Le membre spécifié est introuvable.", color=discord.Color.red())
            await ctx.send(embed=embed)
          
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Erreur de Permissions", description="Vous n'avez pas la permission d'utiliser cette commande.", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title="Membre Introuvable", description="Le membre spécifié est introuvable.", color=discord.Color.red())
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int = None, *, reason: str = "Aucune raison spécifiée"):
        # Vérifier si l'utilisateur a les autorisations nécessaires pour exécuter la commande
        if ctx.author.guild_permissions.manage_roles:
            # Trouver le rôle "Muet" ou le créer s'il n'existe pas
            mute_role = discord.utils.get(ctx.guild.roles, name="Mute")
            if not mute_role:
                mute_role = await ctx.guild.create_role(name="Mute", color=discord.Color(0x660066))

            # Appliquer le rôle muet à l'utilisateur
            await member.add_roles(mute_role, reason=reason)

            # Empêcher l'utilisateur de parler dans tous les salons
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)

            # Créer un Embed amélioré pour la réponse
            embed = discord.Embed(
                title="Membre Muet",
                description=f"{member.mention} a été rendu muet",
                color=discord.Color(0x660066)
            )
            if duration:
                embed.add_field(name="Durée du mute", value=f"{duration} minute(s)")
            embed.add_field(name="Raison", value=reason)
            embed.set_thumbnail(url=member.avatar_url)  # Image du membre muet

            # Inclure le nom du modérateur
            embed.set_footer(text=f"Modérateur : {ctx.author.name}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

            if duration:
                await asyncio.sleep(duration * 60)  # Attendre la durée spécifiée
                await member.remove_roles(mute_role, reason="Expiration du temps de mute")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(mute_role, overwrite=None)  # Rétablir les permissions
        else:
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        # Vérifier si l'utilisateur a les autorisations nécessaires pour exécuter la commande
        if ctx.author.guild_permissions.manage_roles:
            # Trouver le rôle "Mute" s'il existe
            mute_role = discord.utils.get(ctx.guild.roles, name="Mute")

            if mute_role in member.roles:
                await member.remove_roles(mute_role, reason="Levée du mute par un modérateur")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(mute_role, overwrite=None)  # Rétablir les permissions
                embed = discord.Embed(
                    title="Membre Dé-Muet",
                    description=f"{member.mention} a été dé-muet",
                    color=discord.Color(0x660066)
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{member.mention} n'est pas muet.")
        else:
            await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")


    

   
   
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        """Verrouille un canal pour empêcher les membres d'envoyer des messages."""
        channel = channel or ctx.channel
        overwrites = channel.overwrites_for(ctx.guild.default_role)
        overwrites.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)

        # Créer un Embed amélioré pour la réponse
        embed = discord.Embed(
            title="Canal Verrouillé",
            description=f"Le canal {channel.mention} a été verrouillé.",
            color=discord.Color(0x660066)  # Couleur violette
        )

        # Inclure le nom du modérateur
        embed.set_footer(text=f"Modérateur : {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Déverrouille un canal pour permettre aux membres d'envoyer à nouveau des messages."""
        channel = channel or ctx.channel
        overwrites = channel.overwrites_for(ctx.guild.default_role)
        overwrites.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)

        # Créer un Embed amélioré pour la réponse
        embed = discord.Embed(
            title="Canal Déverrouillé",
            description=f"Le canal {channel.mention} a été déverrouillé.",
            color=discord.Color(0x660066)  # Couleur violette
        )

        # Inclure le nom du modérateur
        embed.set_footer(text=f"Modérateur : {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount <= 0:
            await ctx.send("Veuillez spécifier un nombre de messages à supprimer supérieur à zéro.")
            return

        deleted_messages = await ctx.channel.purge(limit=amount + 1)  # +1 pour inclure la commande elle-même
        author_profile_url = ctx.author.avatar_url_as(size=128)

        # Créer un Embed amélioré pour la réponse
        embed = discord.Embed(
            title="Messages Supprimés",
            description=f"{amount} messages ont été supprimés par {ctx.author.mention}.",
            color=discord.Color(0x660066)  # Couleur violette
        )
        embed.set_author(name=ctx.author.name, icon_url=author_profile_url)

        # Inclure le nom du modérateur
        embed.set_footer(text=f"Modérateur : {ctx.author.name}", icon_url=author_profile_url)

        await ctx.send(embed=embed, delete_after=5)

    
    command_errors = {
      commands.MissingPermissions: ("Erreur de permissions", "Vous n'avez pas les permissions nécessaires pour utiliser cette commande."),
      commands.MissingRequiredArgument: {
          "kick": ("Erreur d'Argument", "Utilisation incorrecte de la commande. Utilisez `kick <membre> [raison]`."),
          "ban": ("Erreur d'Argument", "Utilisation incorrecte de la commande. Utilisez `ban <membre> [raison]`."),
          "mute": ("Erreur d'Argument", "Utilisation incorrecte de la commande. Utilisez `mute <membre> [raison]`."),
          "unmute": ("Erreur d'Argument", "Utilisation incorrecte de la commande. Utilisez `unmute <membre>`."),
          "clear": ("Erreur d'Argument", "Utilisation incorrecte de la commande. Utilisez `clear <quantité>`.")
      },
      commands.BadArgument: ("Erreur d'Argument", "L'argument fourni est incorrect."),
    }

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      if type(error) in self.command_errors:
          if isinstance(self.command_errors[type(error)], tuple):
              title, message = self.command_errors[type(error)]
          elif ctx.command.name in self.command_errors[type(error)]:
              title, message = self.command_errors[type(error)][ctx.command.name]
          else:
              title, message = ("Erreur d'Argument", "Utilisation incorrecte de la commande.")
      else:
          title, message = ("Erreur", f"Une erreur s'est produite : {str(error)}")

      await self.send_error_embed(ctx, title, message)

    async def send_error_embed(self, ctx, title, message):
     
      embed = discord.Embed(title=title, description=message, color=0x660066)
      await ctx.send(embed=embed)




    @commands.command()
    async def help(self, ctx):
        bot_logo_url = "https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg"

        # Liste des catégories avec leurs emojis
        categories = [
              {
                "emoji": "⚙️",
                "name": "Commandes Antilien",
                "commands": [
                    ("antilien on|off", "Activer ou désactiver la fonction anti-lien."),
                    ("addlink <lien>", "Ajouter un lien autorisé à la liste."),
                    ("removelink <lien>", "Supprimer un lien autorisé de la liste."),
                    ("listlinks", "Afficher la liste des liens autorisés."),
                    ("helplink", "Afficher l'aide pour les commandes antilien.")
                ]
              },
              {
                "emoji": "😄",
                "name": "Commandes Amusantes",
                "commands": [
                    ("devinette", "Poser une devinette à l'utilisateur."),
                    ("compliment [membre]", "Donner un compliment encourageant.")
                ]
            },
                  
            {
                "emoji": "🔨",
                "name": "Commandes de Modération",
                "commands": [
                    ("kick <membre> [raison]", "Exclure un membre du serveur."),
                    ("ban <membre> [raison]", "Bannir un membre du serveur."),
                    ("mute <membre> [raison]", "Muter un membre."),
                    ("unmute <membre>", "Démuter un membre."),
                    ("nuke", "Nettoyer le canal actuel."),
                    ("lock [canal]", "Verrouiller un canal."),
                    ("unlock [canal]", "Déverrouiller un canal."),
                    ("clear <quantité>", "Effacer un certain nombre de messages."),
                    ("help_s", "Serveur Disponible"),
                    ("warn <membre> [raison]", "Avertir un membre."),
                    ("unwarn <membre> [raison]", "Retirer un avertissement à un membre."),
                    ("warnlist <membre>", "Afficher la liste des avertissements d'un membre.")
                ]
               
            },
            {
                "emoji": "🤬",
                "name": "Commandes du Filtre de Mots Inappropriés",
                "commands": [
                    ("antiswear", "Activer ou désactiver la détection des mots inappropriés."),
                    ("listswear", "Afficher la liste des mots interdits."),
                    ("addswear <mot>", "Ajouter un mot à la liste des mots interdits."),
                    ("removeswear <mot>", "Retirer un mot de la liste des mots interdits."),
                    ("helpswear", "Afficher l'aide pour les commandes de détection des mots inappropriés.")
                ]
            },
          {
                  "emoji": "🔒",
                  "name": "Commandes de Protection",
                  "commands": [
                      ("antibot on|off", "Activer ou désactiver l'arriver de bot"),
                      ("antichannel/on|off", "Activer ou désactiver la création de salons."),
                      ("deletechannel/on|off", "Activer ou désactiver la suppression de salons"),
                      ("filtremaj on|off", "Activer ou désactiver le filtre de majuscules."),
                      ("set (Nombre)", "Définir le pourcentage de majuscules autorisées.")
                  ]
              },
          ]

        # Créer l'embed avec les emojis et noms de catégorie
        embed = discord.Embed(
            title="Aide des Commandes du Bot",
            description="Cliquez sur une réaction ci-dessous pour choisir une catégorie.",
            color=0x660066
        )
        embed.set_thumbnail(url=bot_logo_url)

        for category in categories:
            embed.add_field(
                name=f"{category['emoji']} {category['name']}",
                value="Cliquez sur la réaction ci-dessous pour afficher les commandes.",
                inline=False
            )

        # Créer un message initial avec l'embed
        message = await ctx.send(embed=embed)

        # Ajouter des réactions pour chaque catégorie
        for category in categories:
            await message.add_reaction(category['emoji'])

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and reaction.emoji in [category['emoji'] for category in categories]

        while True:
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', check=check)
            except Exception:
                await message.delete()
                break

            # Trouver la catégorie correspondant à la réaction
            selected_category = next((category for category in categories if category['emoji'] == reaction.emoji), None)

            if selected_category:
                # Mettre à jour le message avec la liste des commandes de la catégorie
                category_embed = discord.Embed(
                    title=f"Commandes {selected_category['name']}",
                    description="\n".join([f"`{cmd}` - {desc}" for cmd, desc in selected_category['commands']]),
                    color=0x660066
                )
                await ctx.send(embed=category_embed)



def setup(bot):
  bot.add_cog(Moderation(bot))
    