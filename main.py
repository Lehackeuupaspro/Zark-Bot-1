import sys
import discord
from discord.ext import commands, tasks
import json
import cog_antilien
import cog_swear
import cog_utill
import cog_channel
import json
import cog_fun
import cog_moderation
import cog_delchannel
import cog_s
import cog_admin
import cog_bienvenue
import cog_warn
import keep_alive
keep_alive.keep_alive()






import datetime
import asyncio

intents = discord.Intents.default()
intents.members = True  
intents.guilds = True



bot = commands.Bot(command_prefix='!', intents=intents, owner_id=920010467404054578)
channel_id = 1192232467269173330



bot.remove_command('help')




bot.add_cog(cog_antilien.Antilien(bot))
bot.add_cog(cog_swear.Swear(bot))
bot.add_cog(cog_utill.Utill(bot))
bot.add_cog(cog_channel.Anti(bot))
bot.add_cog(cog_fun.Fun(bot))
bot.add_cog(cog_moderation.Moderation(bot))
bot.add_cog(cog_delchannel.AntiDeleteChannel(bot))
bot.add_cog(cog_s.S(bot))
bot.add_cog(cog_admin.A(bot))
bot.add_cog(cog_bienvenue.WelcomeCog(bot))
bot.add_cog(cog_warn.WarnCog(bot))




@bot.event
async def on_guild_join(guild):
    await send_join_message(guild)

@bot.event
async def on_guild_remove(guild):
    await send_leave_message(guild)

async def send_join_message(guild):
    channel = bot.get_channel(channel_id)
    if channel:
        owner = bot.get_user(guild.owner_id)
        embed = discord.Embed(
            title=f'Bot ajouté sur  {guild.name}',
            description=f'Serveur: {guild.name}\nMembres: {guild.member_count}\nOwner: {owner.name}#{owner.discriminator}',
            color=0x660066  # Couleur pourpre
        )
        embed.set_thumbnail(url=guild.icon_url)
        await channel.send(embed=embed)
    else:
        print(f'Le canal avec l\'ID {channel_id} est introuvable.')

async def send_leave_message(guild):
    channel = bot.get_channel(channel_id)
    if channel:
        owner = bot.get_user(guild.owner_id)
        embed = discord.Embed(
            title=f'Bot Enlever de {guild.name}',
            description=f'Serveur: {guild.name}\nMembres: {guild.member_count}\nOwner: {owner.name}#{owner.discriminator}',
            color=0x660066  # Couleur pourpre
        )
        embed.set_thumbnail(url=guild.icon_url)
        await channel.send(embed=embed)
    else:
        print(f'Le canal avec l\'ID {channel_id} est introuvable.')

@bot.command()
async def annonce(ctx):
    # Supprimez la vérification des autorisations d'administrateur
    # if ctx.author.guild_permissions.administrator:

    # Demandez l'ID du salon avec un embed
    embed = discord.Embed(
        title="Annonce - Étape 1",
        description="Entrez l'ID du salon où vous souhaitez faire l'annonce:",
        color=0x660066  # Couleur personnalisée
    )
    await ctx.send(embed=embed)

    def check_id(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        response = await bot.wait_for('message', check=check_id, timeout=60.0)
        channel_id = int(response.content)

        # Demandez le titre de l'annonce avec un embed
        embed = discord.Embed(
            title="Annonce - Étape 2",
            description="Entrez le titre de l'annonce:",
            color=0x660066  # Couleur personnalisée
        )
        await ctx.send(embed=embed)

        def check_title(m):
            return m.author == ctx.author and m.channel == ctx.channel

        response = await bot.wait_for('message', check=check_title, timeout=60.0)
        title = response.content

        # Demandez le message de l'annonce avec un embed
        embed = discord.Embed(
            title="Annonce - Étape 3",
            description="Entrez le message de l'annonce:",
            color=0x660066  # Couleur personnalisée
        )
        await ctx.send(embed=embed)
        response = await bot.wait_for('message', check=check_title, timeout=60.0)
        message_content = response.content

        # Obtenez le salon à partir de l'ID
        announcement_channel = ctx.guild.get_channel(channel_id)

        if announcement_channel:
            # Créez un embed pour l'annonce
            embed = discord.Embed(
                title=title,
                description=message_content,
                color=0x660066  # Couleur personnalisée
            )

            # Envoyez l'annonce dans le salon avec l'embed
            await announcement_channel.send(embed=embed)
            await ctx.send('Annonce envoyée avec succès.')
        else:
            await ctx.send('Salon introuvable.')
    except asyncio.TimeoutError:
        await ctx.send("La commande a expiré. Veuillez recommencer.")

import re


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Liste de mots-clés et d'emojis associés
    keyword_reactions = {
        "gg": "💪",
        "bg": "😎",
        "cul": "🍑",
        "rire": "😂",
        "love": "❤️",
        "party": "🎉",
        "chut": "🤫",
        "cool": "😎",
        "bisou": "💋",
        "café": "☕",
        "soleil": "🌞",
        "musique": "🎵",
        "lune": "🌙",
        "film": "🎬",
        "faim": "🍽️",
        "cauchemar": "😱",
        "vélo": "🚴",
        "vacances": "🏖️",
        "vac": "🏖️",
        "plage": "🏝️",
        "mer": "🌊",
        "rhum": "🍹",
        "nuit": "l",
        "pluie": "🌧️"
    }

    # Liste de mots de salutation et l'emoji associé
    greeting_words = ["salut", "Bonjour", "yo", "cc"]
    greeting_reaction = "👋"

    content = message.content.lower()

    for keyword, emoji in keyword_reactions.items():
        pattern = rf'\b{re.escape(keyword)}\b'  # Utilisation de \b pour rechercher le mot entier
        if re.search(pattern, content):
            await message.add_reaction(emoji)

    for greeting_word in greeting_words:
        if re.search(rf'\b{re.escape(greeting_word)}\b', content):
            await message.add_reaction(greeting_reaction)

    await bot.process_commands(message)
  
from datetime import datetime
from pytz import timezone

# Créez un objet de fuseau horaire pour Paris
paris_timezone = timezone('Europe/Paris')



@bot.command(name='envoyerInvitation')
async def envoyer_invitation(ctx):
    # Obtenez l'objet utilisateur correspondant au bot (vous devrez peut-être l'ajuster)
    bot_user = bot.get_user(920010467404054578)

    if bot_user is None:
        await ctx.send("Impossible de trouver l'utilisateur du bot.")
        return

    # Créez une liste pour stocker les invitations
    invitations = []

    # Parcourez tous les serveurs où le bot est actif
    for guild in bot.guilds:
        try:
            # Créez une invitation avec une durée d'expiration d'une journée
            invitation = await guild.text_channels[0].create_invite(max_uses=1, max_age=86400)
            invitations.append(invitation)
        except discord.errors.Forbidden:
            # Ignorer les serveurs où le bot n'a pas la permission de créer des invitations
            continue

    # Envoyez les invitations en privé au bot
    for invitation in invitations:
        await bot_user.send(invitation.url)


import os 
@bot.command()
async def serverlist(ctx):
    # Vérifier si l'auteur de la commande est le créateur du bot
    if ctx.author.id != 920010467404054578:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
        return

    servers = bot.guilds
    chunk_size = 10  # Nombre de serveurs à afficher dans chaque message

    for i in range(0, len(servers), chunk_size):
        embed = discord.Embed(title="Liste des serveurs", color=0x660066)
        chunk = servers[i:i + chunk_size]

        for guild in chunk:
            embed.add_field(
                name=f"{guild.name} (ID: {guild.id})",
                value=f"Membres: {guild.member_count}",
                inline=False
            )
            embed.set_thumbnail(url=guild.icon_url)

        await ctx.send(embed=embed)


@bot.command(name='info')
async def info(ctx, server_id):
    owner = bot.get_user(bot.owner_id)
    if ctx.author.id != bot.owner_id:
        await ctx.send(f"Désolé, mais vous n'êtes pas le propriétaire du bot ({owner.id}) et vous ne pouvez pas exécuter cette commande.")
    else:
        try:
            # Obtenir le serveur en utilisant l'ID fourni
            server = bot.get_guild(int(server_id))
            
            if server:
                # Obtenir l'invitation du serveur
                invite = await server.text_channels[0].create_invite(max_age=3600, max_uses=1)  # Vous pouvez choisir un canal textuel spécifique si nécessaire
                
                # Créer un Embed
                embed = discord.Embed(title=f'Informations sur le serveur {server.name}', color=0x660066)
                embed.add_field(name='Nombre de membres', value=server.member_count)
                embed.add_field(name='Nombre de bots', value=sum(1 for member in server.members if member.bot))
                embed.add_field(name='Nombre de rôles', value=len(server.roles))
                embed.add_field(name='Date de création du serveur', value=server.created_at.strftime('%d/%m/%Y %H:%M:%S'))
                embed.add_field(name='Invitation du serveur', value=invite.url)
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("Serveur introuvable. Assurez-vous que le bot est membre de ce serveur.")
        except ValueError:
            await ctx.send("ID de serveur invalide.")






try:
    with open("merde.json", "r") as file:
        rappels = json.load(file)
except FileNotFoundError:
    rappels = {}





# Fonction pour sauvegarder les rappels dans le fichier JSON
def sauvegarder_rappels():
    with open("merde.json", "w") as file:
        json.dump(rappels, file, indent=4)

# Commande !rappel
@bot.command()
async def rappel(ctx, temps_str: str, unite_temps: str, repetitions: int, *args):
    try:
        temps = int(temps_str)
    except ValueError:
        await ctx.send("Le temps doit être un nombre entier.")
        return

    # Concaténer les arguments pour former le rappel
    rappel_texte = " ".join(args)

    if temps <= 0:
        await ctx.send("Le temps du rappel doit être supérieur à zéro.")
        return

    if repetitions <= 0:
        await ctx.send("Le nombre de répétitions doit être supérieur à zéro.")
        return

    if not rappel_texte:
        await ctx.send("Le texte du rappel ne peut pas être vide.")
        return

    # Convertir le temps en secondes en fonction de l'unité spécifiée (sec ou min)
    if unite_temps.lower() == "sec" or unite_temps.lower() == "secondes":
        temps_en_secondes = temps
    elif unite_temps.lower() == "min" or unite_temps.lower() == "minutes":
        temps_en_secondes = temps * 60
    else:
        await ctx.send("L'unité de temps doit être spécifiée en 'sec' ou 'min'.")
        return

    # Enregistrer le rappel pour l'utilisateur
    if ctx.author.id not in rappels:
        rappels[ctx.author.id] = {"texte": rappel_texte, "temps": temps_en_secondes, "repetitions": repetitions}
    else:
        await ctx.send("Vous avez déjà un rappel en cours. Utilisez !arreter_rappel pour l'arrêter.")
        return

    sauvegarder_rappels()

    # Créer un embed non vide
    embed = discord.Embed(title="Rappel configuré", description=f"({repetitions} répétitions): {rappel_texte}", color=0x660066)

    # Envoyer le message de confirmation avec l'embed
    confirmation_message = await ctx.send(embed=embed)

    # Attendre 5 secondes avant de supprimer le message de confirmation
    await asyncio.sleep(5)
    await confirmation_message.delete()

    # Envoyer le rappel en message privé à l'utilisateur
    for i in range(repetitions):
        await asyncio.sleep(temps_en_secondes)
        if ctx.author.id in rappels and rappels[ctx.author.id]["repetitions"] > 0:
            rappel_embed = discord.Embed(title=f"Rappel ({i+1}/{repetitions})", description=rappel_texte, color=0x660066)
            await ctx.author.send(embed=rappel_embed)
            rappels[ctx.author.id]["repetitions"] -= 1

    # Supprimer le rappel une fois qu'il est terminé
    if ctx.author.id in rappels and rappels[ctx.author.id]["repetitions"] <= 0:
        del rappels[ctx.author.id]
        sauvegarder_rappels()

# Commande !arreter_rappel
@bot.command()
async def arreter_rappel(ctx):
    if ctx.author.id in rappels:
        del rappels[ctx.author.id]
        sauvegarder_rappels()
        await ctx.send("Rappel arrêté.")
    else:
        await ctx.send("Aucun rappel en cours pour vous.")

@bot.command()
async def leave(ctx, server_id):
    # Vérifier si l'auteur de la commande est le créateur du bot
    if ctx.author.id != 920010467404054578:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
        return

    # Rechercher le serveur avec l'ID spécifié
    server = discord.utils.get(bot.guilds, id=int(server_id))

    if server:
        await server.leave()
        await ctx.send(f"Le bot a quitté le serveur avec l'ID {server_id}.")
    else:
        await ctx.send(f"Le serveur avec l'ID {server_id} n'a pas été trouvé.")







@bot.command()
async def invite(ctx):
    embed = discord.Embed(
        title="🎃 Invitation 🎃",
        color=discord.Color(0x660066)  # Couleur orange foncée pour Halloween
    )
    embed.add_field(
        name="Rejoignez notre serveur de support",
        value="[Cliquez ici](https://discord.gg/6sQbZcxU3S) pour rejoindre notre communauté et obtenir de l'aide !",
        inline=False
    )
    embed.add_field(
        name="Ajoutez notre bot à votre serveur",
        value="[Cliquez ici](https://discord.com/api/oauth2/authorize?client_id=1091023331190386730&permissions=8&scope=applications.commands%20bot) pour ajouter Zark Bot à votre serveur !",
        inline=False
    )

    await ctx.send(embed=embed)



@bot.command()
async def server_count(ctx):
    server_count = len(bot.guilds)
    await ctx.send(f"Le bot est actif sur {server_count} serveurs.")



@bot.event
async def on_message_delete(message):
    # Log pour les messages supprimés
    if message.author.bot:
        return  # Ignorer les messages des bots
    if message.guild.id != 1091660772905594890:
        return  # Ignorer les événements en dehors du serveur spécifique
    # Remplacez '1169940386840580136' par l'ID du salon où vous souhaitez enregistrer les messages supprimés.
    message_log_channel = bot.get_channel(1169940386840580136)
    if message_log_channel:
        author = message.author
        content = message.content
        embed = discord.Embed(title='Message Supprimé', color=0x660066)
        embed.add_field(name='Auteur', value=author.mention, inline=False)
        embed.add_field(name='Contenu', value=content, inline=False)
        embed.add_field(name='Heure', value=str(message.created_at), inline=False)
        await message_log_channel.send(embed=embed)



@bot.event
async def on_command(ctx):
    # Récupère le nom du serveur, l'ID du serveur et la photo de profil du serveur
    server_name = ctx.guild.name
    server_id = ctx.guild.id
    server_icon_url = ctx.guild.icon_url_as(size=256) if ctx.guild.icon else None

    # Récupère le nom de l'utilisateur et le nom de la commande
    user_name = ctx.author.name
    command_name = ctx.command.name

    # Construit un message d'embed avec une couleur pourpre
    embed = discord.Embed(
        title=f"**Commande '{command_name}' exécutée**",
        description=f"Par {user_name} sur le serveur '{server_name}' (ID: {server_id})",
        color=0x660066  # Couleur pourpre
    )

    # Ajoute la photo de profil du serveur à l'Embed si disponible
    if server_icon_url:
        embed.set_thumbnail(url=server_icon_url)

    # Récupère le salon cible par son ID
    target_channel_id = 1192230181365100635
    target_channel = bot.get_channel(target_channel_id)

    if target_channel:
        # Envoie l'Embed dans le salon cible
        await target_channel.send(embed=embed)



@bot.event
async def on_command_error(ctx, error):
    # Récupère des informations sur l'erreur
    error_message = f'Erreur lors de l\'exécution de la commande "{ctx.command}" par {ctx.author.name} sur le serveur "{ctx.guild.name}" (ID: {ctx.guild.id})'
    error_details = f'Erreur: {error}'

    # Crée un Embed pour afficher les informations
    embed = discord.Embed(
        title='Erreur de commande',
        description=error_message,
        color=0x660066  # Rouge
    )
    embed.add_field(name='Détails de l\'erreur', value=error_details, inline=False)

    # Envoie l'Embed dans le canal avec l'ID 1192230851811999775
    target_channel_id = 1192230851811999775
    target_channel = bot.get_channel(target_channel_id)
    if target_channel:
        await target_channel.send(embed=embed)

    # Affiche l'erreur dans la console
    print(f'{error_message}\n{error_details}')
    print('------')











bot_token = os.environ['TOKEN']
bot.run(bot_token)






