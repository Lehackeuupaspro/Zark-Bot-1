import discord
from discord.ext import commands, tasks
import random
import json
from datetime import datetime, timedelta
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.devinettes_utilisees = []
        self.cog_category = "FunCommands"
        self.Compliment_utilisees = []
        






    @commands.command()
    async def devinette(self, ctx):
        """Le bot pose une devinette à l'utilisateur."""
        devinettes = [
            ("Quel animal peut vivre le plus longtemps ?", "La tortue"),
            ("Qu'est-ce qui a des racines aussi profondes que le ciel est haut ?", "Un arbre"),
            ("Je peux voler sans ailes, pleurer sans les yeux. Où que je sois, la mort est toujours proche. Que suis-je ?", "Le temps"),
            ("Plus on m'enlève, plus je deviens grand. Qui suis-je ?", "Un trou"),
            ("Qu'est-ce qui peut être brisé, mais ne peut jamais être tenu ?", "Une promesse"),
            ("Quand je suis vieux, je suis rapide. Quand je suis jeune, je suis lent. Que suis-je ?", "Un bougeoir"),
            ("Plus vous en prenez, plus vous en laissez derrière. Qu'est-ce que c'est ?", "Un pas"),
            ("Je suis devant vous, mais vous ne pouvez jamais me toucher. Que suis-je ?", "L'avenir"),
            ("Qu'est-ce qui a des dents mais ne peut pas manger ?", "Une fourchette"),
            ("Plus on en prend, plus il en reste. Qu'est-ce que c'est ?", "Un trou"),
            ("Je vole sans ailes, je pleure sans yeux. Là où je passe, la mort s'ensuit. Que suis-je ?", "Le vent"),
            ("Quand vous m'utilisez, vous me cassez. Pourtant, si vous ne m'utilisez pas, je n'existe pas. Que suis-je ?", "Un œuf"),
            ("Qu'est-ce qui a des clés mais ne peut pas ouvrir de portes ?", "Un piano"),
            ("Je commence et termine avec la lettre 'e', mais je contiens seulement une lettre. Que suis-je ?", "Une enveloppe"),
            ("Je peux voyager tout autour du monde tout en restant dans un coin. Que suis-je ?", "Un timbre"),
            ("Plus vous prenez, plus vous me laissez. Que suis-je ?", "Un empreinte"),
            ("Je suis léger comme une plume, pourtant le plus fort homme ne peut me tenir longtemps. Que suis-je ?", "Le souffle"),
            ("Qu'est-ce qui est toujours devant vous mais vous ne pouvez jamais l'atteindre ?", "L'avenir"),
            ("Qu'est-ce qui vole sans ailes et pleure sans yeux ?", "Le vent"),
            ("Qu'est-ce qui a des dents mais ne peut pas manger ?", "Une fourchette"),
            ("Je suis pris le matin, mais libéré la nuit. Que suis-je ?", "Le sommeil"),
            ("Qu'est-ce qui peut être brisé, mais ne peut jamais être tenu ?", "Une promesse"),
            ("Je suis lourd à l'aller, mais léger au retour. Qu'est-ce que je suis ?", "Un cerf-volant"),
            ("Quel est le comble pour un électricien ?", "De ne pas être au courant"),
            ("Qu'est-ce qui peut être cassé, mais jamais touché ?", "Une promesse"),
            ("Je suis toujours devant vous, mais vous ne pouvez jamais me voir. Que suis-je ?", "Votre futur"),
            ("Plus on en a, moins on en voit. Qu'est-ce que c'est ?", "L'obscurité"),
            ("Qu'est-ce qui est pris le matin mais libéré la nuit ?", "Le sommeil"),
            ("Quel animal peut vivre le plus longtemps ?", "La tortue"),
            ("Je suis pris le matin, mais libéré la nuit. Que suis-je ?", "Le sommeil"),
            ("Quand je suis vieux, je suis rapide. Quand je suis jeune, je suis lent. Que suis-je ?", "Un bougeoir"),
            # Ajoutez ici davantage de nouvelles devinettes
        ]

        devinette, reponse = random.choice(devinettes)
        
        embed = discord.Embed(
            title="Devine la devinette",
            description=devinette,
            color=0x660066  # Couleur violette
        )
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg")
        await ctx.send(embed=embed)
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            response_message = await self.bot.wait_for("message", timeout=30.0, check=check)

            if response_message.content.lower() == reponse.lower():
                response_embed = discord.Embed(
                    title="Bonne réponse !",
                    description=f"La réponse est bien : {reponse}",
                    color=0x660066  # Couleur verte
                )
                await ctx.send(embed=response_embed)
            else:
                response_embed = discord.Embed(
                    title="Mauvaise réponse !",
                    description=f"La réponse correcte était : {reponse}",
                    color=0x660066  # Couleur rouge
                )
                await ctx.send(embed=response_embed)
        except asyncio.TimeoutError:
            await ctx.send("Désolé, vous avez mis trop de temps pour répondre.")




    @commands.command()
    async def compliment(self, ctx, member: discord.Member = None):
        """Donne un compliment encourageant."""
        compliments = [
            "Tu es incroyablement talentueux !",
            "Ta gentillesse illumine la journée de tout le monde !",
            "Tu as un sourire qui pourrait éclairer une pièce sombre.",
            "Les gens aiment être autour de toi à cause de ton énergie positive.",
            "Ta détermination est inspirante.",
            "Tu es plus fort(e) que tu ne le penses.",
            "Ton sens de l'humour met toujours tout le monde de bonne humeur !",
            "Ta créativité est vraiment impressionnante.",
            "Chacune de tes idées est brillante et originale.",
            "Ton attitude positive est contagieuse.",
            "Tu es toujours prêt(e) à aider les autres, peu importe les circonstances.",
            "Ta persévérance est admirable et inspirante.",
            "Ton amitié est un cadeau précieux pour ceux qui te connaissent.",
            "Ta présence rayonne de positivité et de bonté.",
            "Chaque jour, tu apportes du bonheur à ceux qui t'entourent.",
            "Ton charisme est indéniable et attire les regards.",
            "Tes efforts ne passent jamais inaperçus et sont grandement appréciés.",
            "Ta générosité n'a pas de limites et inspire les autres à faire de même.",
            "Tu es un exemple de persévérance et de courage.",
            "Tes qualités sont nombreuses et chacune est remarquable à sa manière.",
            "Ton authenticité est une qualité rare et précieuse.",
            "Ta voix a le pouvoir d'apaiser et de réconforter ceux qui l'écoutent.",
            "Ton sourire a le don de mettre instantanément de bonne humeur.",
            "Ton sens du style est impeccable et te distingue des autres.",
            "Ta bienveillance envers autrui crée un environnement positif.",
            "Tu es une source constante d'inspiration pour ceux qui t'entourent.",
            "Tes actions parlent plus fort que les mots et laissent une empreinte durable.",
            "Ton énergie rayonnante illumine les moments les plus sombres.",
            "Ta présence calme et apaisante a un effet réconfortant sur les autres.",
            "Ta capacité à trouver des solutions est impressionnante et utile.",
            "Tes conseils sont toujours avisés et précieux.",
            "Tu es la preuve vivante qu'une personne peut avoir un impact positif sur le monde."
        ]

        compliments_non_utilises = [compliment for compliment in compliments if compliment not in self.Compliment_utilisees]

        if not compliments_non_utilises:
            embed = discord.Embed(
                title="Compliments épuisés",
                description="Tu as déjà entendu tous les compliments disponibles !",
                color=0x660066  # Couleur orange
            )
            await ctx.send(embed=embed)
            return

        compliment = random.choice(compliments_non_utilises)
        self.Compliment_utilisees.append(compliment)
        
        embed = discord.Embed(
            title="Compliment",
            description=compliment,
            color=0x660066  # Couleur vert foncé
        )
        
        bot_avatar_url = "https://media.discordapp.net/attachments/1091849987786277015/1155069172372480000/Screenshot_20230923_090146_com.android.chrome_edit_140043245876547.jpg"
        embed.set_author(name=ctx.author.name, icon_url=bot_avatar_url)
        
        if member:
            await ctx.send(f"{member.mention},", embed=embed)
        else:
            await ctx.send(embed=embed)


    @commands.command(name='member_count')
    async def member_count(self, ctx):
        # Récupérer le nombre de membres dans le serveur
        member_count = ctx.guild.member_count

        # Créer un objet Embed avec la couleur spécifiée
        embed = discord.Embed(title="Nombre de membres", color=0x660066)
        embed.add_field(name="Total", value=member_count)

        # Envoyer l'embed dans le canal où la commande a été appelée
        await ctx.send(embed=embed)

    @commands.command(name='liststreams', help='Affiche les membres du serveur en train de streamer.')
    async def streams_list(self, ctx):
        # Accédez à la liste des membres du serveur
        members = ctx.guild.members

        # Créez une liste pour stocker les membres en train de streamer
        streaming_members = []

        for member in members:
            # Vérifiez si le membre est en train de streamer
            if member.activity and isinstance(member.activity, discord.Streaming):
                streaming_members.append(member.display_name)

        # Joignez la liste des membres en train de streamer en une chaîne
        streaming_str = ', '.join(streaming_members)

        # Créez un embed avec la couleur 0x660066
        embed = discord.Embed(title='Membres en train de streamer', color=0x660066)

        if streaming_str:
            embed.description = streaming_str
        else:
            embed.description = 'Aucun membre n\'est actuellement en train de streamer.'

        # Envoyez l'embed
        await ctx.send(embed=embed)


 

def setup(bot):
    bot.add_cog(Fun(bot))
