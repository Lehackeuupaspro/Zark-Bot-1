import os
import discord
from discord.ext import commands
import json


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()

    def ensure_config_exists(self):
        if not os.path.exists('Fonction-ipt'):
            os.makedirs('Fonction-ipt')
        if not os.path.exists('merde.json'):
            with open('merde.json', 'w') as file:
                json.dump({}, file)
        if not os.path.exists('bot.json'):
            with open('bot.json', 'w') as file:
                json.dump({}, file)

    def load_config(self):
        self.ensure_config_exists()
        try:
            with open('merde.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_config(self):
        self.ensure_config_exists()
        try:
            with open('merde.json', 'w') as file:
                json.dump(self.config, file, indent=4)
        except Exception as e:
            print(f"Error while saving configuration: {e}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.is_antibot_enabled(member.guild.id) and member.bot:
            try:
                await member.kick(reason="Bot interdit sur le serveur")
                print(f"Bot {member.name} a été kické.")
            except Exception as e:
                print(f"Erreur lors du kick du bot : {e}")
        else:
            welcome_config = self.config.get(str(member.guild.id))

            welcome_channel = member.guild.get_channel(welcome_config["welcome_channel_id"])
            welcome_role_id = welcome_config.get("welcome_role_id")
            welcome_message = welcome_config.get("welcome_message")

            # Nouvel ajout : Date de création du compte
            created_at = member.created_at.strftime("%d/%m/%Y à %H:%M:%S")

            if welcome_channel:
                avatar_url = member.avatar_url
                avatar_image = await avatar_url.read()

                if not welcome_message:
                    welcome_message = f"Bienvenue {member.display_name} sur {member.guild.name} ! Nous sommes ravis de t'accueillir ici, {member.mention}. Ton compte a été créé le {created_at}."

                welcome_message = welcome_message.replace("{user}", member.mention)
                welcome_message = welcome_message.replace("{created_at}", created_at)

                embed = discord.Embed(
                    title=f"Bienvenue {member.display_name} sur {member.guild.name} !",
                    description=welcome_message,
                    color=0x660066
                )

                embed.set_thumbnail(url=avatar_url)

                member_count = member.guild.member_count
                embed.add_field(name="Membres", value=member_count, inline=True)

                await welcome_channel.send(embed=embed)
            else:
                print(f"Salon de bienvenue introuvable dans le serveur {member.guild.name}.")

            if welcome_role_id:
                role = member.guild.get_role(welcome_role_id)
                if role:
                    await member.add_roles(role)
                else:
                    print(f"Le rôle spécifié est introuvable dans le serveur {member.guild.name}.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def bienvenue(self, ctx):
        embed = discord.Embed(
            title="Configuration du salon de bienvenue",
            description="Veuillez fournir l'ID du salon de bienvenue :",
            color=0x660066
        )
        await ctx.send(embed=embed)

        def check_channel(message):
            return message.author == ctx.author

        try:
            response_channel = await self.bot.wait_for('message', check=check_channel, timeout=60)
            channel_id = int(response_channel.content)
            channel = ctx.guild.get_channel(channel_id)

            if channel:
                embed = discord.Embed(
                    title="Configuration du rôle pour les nouveaux membres",
                    description="Veuillez fournir l'ID du rôle à attribuer aux nouveaux membres (ou 0 pour ignorer cette étape) :",
                    color=0x660066
                )
                await ctx.send(embed=embed)

                def check_role(message):
                    return message.author == ctx.author

                response_role = await self.bot.wait_for('message', check=check_role, timeout=60)
                role_id = int(response_role.content)

                # Demandez le message de bienvenue personnalisé
                embed = discord.Embed(
                    title="Configuration du message de bienvenue",
                    description="Veuillez fournir le message de bienvenue (utilisez {user} pour mentionner le membre) :",
                    color=0x660066
                )
                await ctx.send(embed=embed)

                def check_message(message):
                    return message.author == ctx.author

                response_message = await self.bot.wait_for('message', check=check_message, timeout=600)
                welcome_message = response_message.content

                self.config[str(ctx.guild.id)] = {
                    "welcome_channel_id": channel_id,
                    "welcome_role_id": role_id if role_id != 0 else None,
                    "welcome_message": welcome_message
                }

                self.save_config()

                embed = discord.Embed(
                    title="Configuration du salon de bienvenue",
                    description=f"Le salon de bienvenue a été configuré pour ce serveur : {channel.mention}",
                    color=0x660066
                )
                await ctx.send(embed=embed)

                if role_id != 0:
                    role = ctx.guild.get_role(role_id)
                    if role:
                        embed = discord.Embed(
                            title="Configuration du rôle pour les nouveaux membres",
                            description=f"Le rôle {role.mention} a été configuré pour les nouveaux membres.",
                            color=0x660066
                        )
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("Le rôle spécifié est introuvable.")
            else:
                await ctx.send("Le salon spécifié est introuvable.")
        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé. La configuration a été annulée.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def antibot(self, ctx, state: str):
        if state.lower() == "on":
            self.set_antibot_state(ctx.guild.id, True)

            embed = discord.Embed(
                title="Fonction antibot activée 🎃",
                description="La fonction antibot est maintenant activée.",
                color=0x660066  # Couleur orange Halloween
            )

            await ctx.send(embed=embed)
        elif state.lower() == "off":
            self.set_antibot_state(ctx.guild.id, False)

            embed = discord.Embed(
                title="Fonction antibot désactivée 🦇",
                description="La fonction antibot est maintenant désactivée.",
                color=0x660066  # Couleur violette Halloween
            )

            await ctx.send(embed=embed)
        else:
            await ctx.send("Utilisez `antibot on` pour activer la fonction antibot ou `antibot off` pour la désactiver")

    def is_antibot_enabled(self, server_id):
        with open('bot.json', 'r') as file:
            settings = json.load(file)
            return settings.get(str(server_id), False)

    def set_antibot_state(self, server_id, state):
        with open('bot.json', 'r') as file:
            settings = json.load(file)
        settings[str(server_id)] = state
        with open('bot.json', 'w') as file:
            json.dump(settings, file, indent=4)

def setup(bot):
    bot.add_cog(WelcomeCog(bot))
