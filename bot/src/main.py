import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

actual_talking = ""


@bot.command("covid", help='Nothing Yet')
async def covid_predict(ctx):
    actual_talking = ctx.author
    await ctx.send('Now I am going to ask you a few questions and I would try to predict if you are ill :c.\n'
                   'I am not scientifically accurate so If you don\'t feel well, please go to your nearest hospital '
                   'as soon as possible.\n Please answer with 👍 or 👎 reaction, thanks for your collaboration.')

    await ctx.send('Do you have testicles?')

    def check(reaction, user):
        return user == actual_talking

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👎':
        await ctx.send('Congratulation! You are not a stupid men.')
    else:
        await ctx.send('Did you know that men die more from COVID-19?')

    print(reaction)


bot.run(TOKEN)
