import discord
from discord.ext import commands
import asyncio


class S(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def s1(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        confirm_embed = discord.Embed(
            title="Confirmation",
            description=
            "Voulez-vous créer et supprimer les salons et rôles ? Répondez avec 'oui' ou 'non'.",
            color=0x660066)
        await ctx.send(embed=confirm_embed)

        try:
            response = await self.bot.wait_for("message",
                                               check=check,
                                               timeout=30)
            if response.content.lower() == "oui":
                # Supprimer tous les salons existants
                for channel in ctx.guild.channels:
                    await channel.delete()

                # Créer des rôles avec des permissions et des couleurs
                roles_data = [
                    ("Fondateur", discord.Permissions(administrator=True),
                     0xFF0000),
                    ("Admin",
                     discord.Permissions(manage_messages=True,
                                         kick_members=True,
                                         ban_members=True), 0x00FF00),
                    ("Modérateur",
                     discord.Permissions(manage_messages=True,
                                         kick_members=True,
                                         ban_members=True), 0x0000FF),
                    ("Membre",
                     discord.Permissions(read_messages=True,
                                         send_messages=True), 0xFFFF00)
                ]

                for role_name, permissions, color in roles_data:
                    await ctx.guild.create_role(name=role_name,
                                                permissions=permissions,
                                                color=discord.Color(color))

                # Informations sur les catégories et les salons
                category_data = [
                    ("🏠 Accueil",
                     ["🚨 annonce", "👋 Présentations", "📜 Règlements"]),
                    ("🌟 Communauté",
                     ["🗣️ Discussions", "📖 Anecdotes", "🎨 Zone créative"]),
                    ("🎉 Événements", [
                        "🎊 Annonces événements", "🗓️ Planning",
                        "📣 post-événements"
                    ]),
                    ("🔗 Partenariats",
                     ["🤝 Partenaires vérifiés", "📩 partenariat"]),
                    ("🎮 Gaming",
                     ["🎮 Discussion", "👥 coéquipiers", "📺 Streams"]),
                    ("📚 Savoir",
                     ["🧠 connaissances", "📝 Tutoriels", "🤔 Questions"]),
                    ("🎵 Musique", [
                        "🎶 Partage de musique", "🎧 Recommandations",
                        "🎤 Créations musicales"
                    ]), ("📷 Médias", ["📸 Photos", "🎥 Vidéos", "🎭 artistique"])
                ]

                # Créer les catégories et les salons
                for category_name, channel_names in category_data:
                    category = await ctx.guild.create_category(category_name)

                    for channel_name in channel_names:
                        await category.create_text_channel(channel_name)

                # Créer la catégorie des salons vocaux et les salons vocaux
                voice_category = await ctx.guild.create_category(
                    '🎤 Salons vocaux 🎤')
                voice_channels = [
                    '🌟 Communauté 🌟',
                    '🎉 Événements 🎉',
                    '🎮 Gaming 🎮',
                    '🎵 Musique 🎵',
                ]
                for channel_name in voice_channels:
                    await voice_category.create_voice_channel(channel_name)

                success_embed = discord.Embed(
                    title="Création terminée",
                    description=
                    "Tous les salons et rôles ont été créés avec succès!",
                    color=0x660066)
                await ctx.send(embed=success_embed)
            else:
                cancel_embed = discord.Embed(
                    title="Annulation",
                    description=
                    "La création des salons et rôles a été annulée.",
                    color=0x660066)
                await ctx.send(embed=cancel_embed)
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="Temps écoulé",
                description=
                "Vous n'avez pas répondu à temps. La création des salons et rôles a été annulée.",
                color=0x660066)
            await ctx.send(embed=timeout_embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def s2(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        confirm_embed = discord.Embed(
            title="Confirmation",
            description=
            "Voulez-vous créer et supprimer les salons et rôles ? Répondez avec 'oui' ou 'non'.",
            color=0x660066)
        await ctx.send(embed=confirm_embed)

        try:
            response = await self.bot.wait_for("message",
                                               check=check,
                                               timeout=30)
            if response.content.lower() == "oui":
                # Supprimer tous les salons existants
                for channel in ctx.guild.channels:
                    await channel.delete()

                # Créer des rôles avec des permissions et des couleurs
                roles_data = [(":pick: Mineur", discord.Permissions(),
                               discord.Color(0xFF5733)),
                              (":man_mage: Mage", discord.Permissions(),
                               discord.Color(0x7139B2)),
                              (":shield: Guerrier", discord.Permissions(),
                               discord.Color(0x33FF7A)),
                              (":art: Artiste", discord.Permissions(),
                               discord.Color(0x337BFF))]

                for role_name, permissions, color in roles_data:
                    await ctx.guild.create_role(name=role_name,
                                                permissions=permissions,
                                                color=color)

                # Informations sur les catégories et les salons
                category_data = [
                    ("🏠 Accueil", ["💬-général", "📢-annonces"]),
                    ("⚔️ Minecraft", [
                        "🎮-discussion-générale", "⛏️-suggestions",
                        "💼-recrutement"
                    ]),
                    ("🛠️ Mods et Plugins",
                     ["📦-modpacks", "⚙️-plugins-et-commandes", "📚-tutoriels"]),
                    ("🎮 Jeux", [
                        "🕹️-minecraft-bedwars", "🎲-skyblock",
                        "🎯-minecraft-survival"
                    ]),
                    ("🌍 Globaux",
                     ["🌐-serveur-minecraft", "💬-autres-jeux", "🎉-détente"]),
                    ("📷 Médias", ["📸 Photos", "🎥 Vidéos", "🎭 artistique"]),
                    ("🎵 Musique", [
                        "🎶 Partage de musique", "🎧 Recommandations",
                        "🎤 Créations musicales"
                    ])
                ]

                # Créer les catégories et les salons
                for category_name, channel_names in category_data:
                    category = await ctx.guild.create_category(category_name)

                    for channel_name in channel_names:
                        await category.create_text_channel(channel_name)

                # Créer la catégorie des salons vocaux et les salons vocaux
                voice_category = await ctx.guild.create_category(
                    '🔊 Salons Vocaux')
                voice_channels = [
                    '🎙️ Discussion générale VC', '🎮 Minecraft VC',
                    '🎵 Musique VC'
                ]
                for channel_name in voice_channels:
                    await voice_category.create_voice_channel(channel_name)

                success_embed = discord.Embed(
                    title="Création terminée",
                    description=
                    "Tous les salons et rôles ont été créés avec succès!",
                    color=0x660066)
                await ctx.send(embed=success_embed)
            else:
                cancel_embed = discord.Embed(
                    title="Annulation",
                    description=
                    "La création des salons et rôles a été annulée.",
                    color=0x660066)
                await ctx.send(embed=cancel_embed)
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="Temps écoulé",
                description=
                "Vous n'avez pas répondu à temps. La création des salons et rôles a été annulée.",
                color=0x660066)
            await ctx.send(embed=timeout_embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def s3(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        confirm_embed = discord.Embed(
            title="Confirmation",
            description=
            "Voulez-vous créer et supprimer les salons et rôles ? Répondez avec 'oui' ou 'non'.",
            color=0x660066)
        await ctx.send(embed=confirm_embed)

        try:
            response = await self.bot.wait_for("message",
                                               check=check,
                                               timeout=30)
            if response.content.lower() == "oui":
                # Supprimer tous les salons existants
                for channel in ctx.guild.channels:
                    await channel.delete()

                # Créer des rôles avec des permissions et des couleurs
                roles_data = [
                    ("Fondateur", discord.Permissions(administrator=True),
                     discord.Color(0xFF5733)),
                    ("Admin", discord.Permissions(), discord.Color(0x7139B2)),
                    ("Modérateur", discord.Permissions(),
                     discord.Color(0x33FF7A)),
                    ("Membre", discord.Permissions(), discord.Color(0x337BFF))
                ]

                for role_name, permissions, color in roles_data:
                    await ctx.guild.create_role(name=role_name,
                                                permissions=permissions,
                                                color=color)

                # Informations sur les catégories et les salons
                category_data = [
                    ("🏢 Bureau Principal", [
                        "📊 Général", "💼 Ressources Humaines",
                        "📂 Projets en Cours", "📆 Calendrier", "💬 Communication"
                    ]),
                    ("📢 Annonces", [
                        "🗨️ Discussion Générale", "📣 Publicité",
                        "🎙️ Conférences", "🌐 Collaboration"
                    ]),
                    ("🚀 Idées et Suggestions", [
                        "🌐 Partenariats", "📈 Développement Commercial",
                        "🔄 Retours Clients", "📚 Formation"
                    ]),
                    ("💡 Créativité", [
                        "🎨 Galerie d'Art", "🎵 Musique et Créativité",
                        "✍️ Écriture et Littérature", "📸 Partage de Médias",
                        "🌐 International"
                    ]),
                    ("🎉 Espace Détente", [
                        "🎮 Jeux et Divertissement", "🍻 Bar Virtuel",
                        "🎯 Concours et Événements", "📦 Autres"
                    ]),
                    ("❓ Support Technique", [
                        "📥 Suggestions pour le Serveur",
                        "📌 Règlements et Informations",
                        "🔄 Changements et Mises à Jour"
                    ])
                ]

                # Créer les catégories et les salons
                for category_name, channel_names in category_data:
                    category = await ctx.guild.create_category(category_name)

                    for channel_name in channel_names:
                        await category.create_text_channel(channel_name)

                # Créer la catégorie des salons vocaux et les salons vocaux
                voice_category = await ctx.guild.create_category(
                    '🔊 Salons Vocaux')
                voice_channels = [
                    '🎤 Vocal Général', '🔊 Salon Principal',
                    '📢 Annonces Vocales', '🎙️ Salons de Réunion',
                    '🎶 Salon de Musique', '📚 Étude et Formation Vocale'
                ]
                for channel_name in voice_channels:
                    await voice_category.create_voice_channel(channel_name)

                success_embed = discord.Embed(
                    title="Création terminée",
                    description=
                    "Tous les salons et rôles ont été créés avec succès!",
                    color=0x660066)
                await ctx.send(embed=success_embed)
            else:
                cancel_embed = discord.Embed(
                    title="Annulation",
                    description=
                    "La création des salons et rôles a été annulée.",
                    color=0x660066)
                await ctx.send(embed=cancel_embed)
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="Temps écoulé",
                description=
                "Vous n'avez pas répondu à temps. La création des salons et rôles a été annulée.",
                color=0x660066)
            await ctx.send(embed=timeout_embed)

    @commands.command()
    async def help_s(self, ctx):
        """
        Affiche l'aide pour les commandes.
        """
        help_embed = discord.Embed(
            title="Aide des commandes",
            description="Voici la liste des commandes disponibles :",
            color=0x660066)
        help_embed.add_field(name="!s1",
                             value="Création d'un Serveur communautaire.",
                             inline=False)
        help_embed.add_field(name="!s2",
                             value="Création d'un Serveur Minecraft.",
                             inline=False)
        help_embed.add_field(name="!s3",
                             value="Création d'un Serveur Commercial.",
                             inline=False)
        help_embed.add_field(name="!s4",
                             value="Création d'un Serveur Détente.",
                             inline=False)

        await ctx.send(embed=help_embed)



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def s4(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        confirm_embed = discord.Embed(
            title="Confirmation",
            description="Voulez-vous créer et supprimer les salons? Répondez avec 'oui' ou 'non'.",
            color=0x660066)
        await ctx.send(embed=confirm_embed)

        try:
            response = await self.bot.wait_for("message", check=check, timeout=30)
            if response.content.lower() == "oui":
                # Supprimer tous les salons existants
                for channel in ctx.guild.text_channels:
                    await channel.delete()

                for channel in ctx.guild.voice_channels:
                    await channel.delete()

                # Informations sur les catégories et les salons
                category_data = [
                    ("🏝️ Serveur de Détente", [
                        "📢 Annonces", "📜 Règles", "🤝 Présentations", "🌈 Suggestions"
                    ]),
                    ("🎉 Salon des Fêtes", [
                        "🥳 Général", "🎈 Jeux", "🍹 Boisson", "🎶 Musique"
                    ]),
                    ("🌮 Salon de Discussion", [
                        "🗣️ Général", "🎯 Jeux de société", "🍔 Cuisine",
                    ]),
                    ("🎨 Salon Créatif", [
                        "🎨 Arts", "✍️ Écriture", "📸 Photos", "🎮 Jeux vidéo"
                    ]),
                    ("🐶 Animaux de Compagnie", [
                        "🐕 Chiens", "🐈 Chats", "🦜 Oiseaux", "🐇 Animaux exotiques"
                    ]),
                    ("🌴 Salon Chill", [
                        "💭 Méditation", "🌿 Nature", "☕ Café"
                    ]),
                    ("🎁 Cadeaux et Giveaways", [
                        "🎁 Échange de Cadeaux", "🎉 Giveaways"
                    ])
                ]

                # Créer les catégories et les salons
                for category_name, channel_names in category_data:
                    category = await ctx.guild.create_category(category_name)

                    for channel_name in channel_names:
                        await category.create_text_channel(channel_name)

                # Créer la catégorie des salons vocaux et les salons vocaux
                voice_category = await ctx.guild.create_category('🎙️ Salons Vocaux')
                voice_channels = [
                    '🎤 Karaoké', '🎵 Musique', '🎙️ Podcasts',
                    '🍻 Bar',
                ]
                for channel_name in voice_channels:
                    await voice_category.create_voice_channel(channel_name)

                success_embed = discord.Embed(
                    title="Création terminée",
                    description="Tous les salons et rôles ont été créés avec succès!",
                    color=0x660066)
                await ctx.send(embed=success_embed)
            else:
                cancel_embed = discord.Embed(
                    title="Annulation",
                    description="La création des salons a été annulée.",
                    color=0x660066)
                await ctx.send(embed=cancel_embed)
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="Temps écoulé",
                description="Vous n'avez pas répondu à temps. La création des salons a été annulée.",
                color=0x660066)
            await ctx.send(embed=timeout_embed)


    

    



    
    


    @s1.error
    async def s1_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            no_permission_embed = discord.Embed(
                title="Erreur de Permission",
                description=
                "Vous n'avez pas les permissions nécessaires pour exécuter cette commande.",
                color=0x660066)
            await ctx.send(embed=no_permission_embed)

    @s2.error
    async def s2_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            no_permission_embed = discord.Embed(
                title="Erreur de Permission",
                description=
                "Vous n'avez pas les permissions nécessaires pour exécuter cette commande.",
                color=0x660066)
            await ctx.send(embed=no_permission_embed)

    @s3.error
    async def s3_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            no_permission_embed = discord.Embed(
                title="Erreur de Permission",
                description=
                "Vous n'avez pas les permissions nécessaires pour exécuter cette commande.",
                color=0x660066)
            await ctx.send(embed=no_permission_embed)
