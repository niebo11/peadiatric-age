import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import pandas as pd

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

actual_talking = ""

symptoms = {'Fever': 'fever', 'Cough': 'tos', 'Croupy cough': 'crup', 'Dysphonia/aphony': 'dysphonia',
                'Shortness of breath or working of breathing':'resp', 'Tachypnea/Polypnea': 'tachypnea'}

data = pd.DataFrame(columns = ['sex', 'sports', 'smokers_home', 'inclusion_criteria', 'sympt_epi',
                               'school_symptoms_member_1', 'school_symptoms_member_2', 'school_confirmed',
                               'symptoms_binary', 'fever', 'tos', 'crup', 'dysphonia', 'resp', 'tachypnea',
                               'ausc_resp', 'wheezing', 'crackles', 'odynophagia', 'nasal_congestion',
                               'fatiga', 'headache', 'conjuntivitis', 'ocular_pain', 'gi_symptoms', 'abdominal_pain',
                               'vomiting', 'dyarrea', 'dermatologic', 'rash', 'adenopathies', 'hepato', 'splenomegaly',
                               'hemorrhagies', 'irritability', 'neuro', 'seizures', 'hypotonia', 'shock',
                               'taste_smell', 'smell', 'vrs_result', 'flu_a_result', 'flu_b_result',
                               'bacterial_infection', 'comorbi_binary', 'obesity', 'flu_binary', 'vaccines_binary',
                               'coviral'])

@bot.command("me", help="Description of the bot")
async def me(ctx):
    await ctx.send("Hi, my name is Covid_Bot, I was created by Aleix Sarroca Soler and Niebo Zhang and I am here "
                   "to helping in everything I can. My most important task is "
                   "to help parents to detect a possible case of CoVid-19 in their children by comparing different"
                   " other cases I have. For this reason I will ask you some questions about the child, if you want me to"
                   " try to help you use the \"!covid\" command. Nice to meet you!")

    message_tempt = ('For the following symptoms please mark with 👍 the ones you are having or you had.'
                   ' When you completed the form react to this message with 👍')

    await ctx.send(message_tempt)

    for value in symptoms:
        await ctx.send(value)

    notEnd = True

    while(notEnd):
        reaction, user = await bot.wait_for('reaction_add', check=check2)

        if reaction.message == message_tempt:
            notEnd = False
        else:
            data[symptoms[reaction.message]] = 1

@bot.command("covid", help='Nothing Yet')
async def covid_predict(ctx):
    actual_talking = ctx.author
    await ctx.send('Now I am going to ask you a few questions and I would try to predict if you are ill :c.\n'
                   'I am not scientifically accurate so If you don\'t feel well, please go to your nearest hospital '
                   'as soon as possible.\n Please answer with 👍 or 👎 reaction, thanks for your collaboration.')

    await ctx.send('Which is your gender? Answer with :mens: :womens: reaction.')

    def check(reaction, user):
        return user == actual_talking

    def check2(reaction, user):
        return user == actual_talking and str(reaction.emoji) == '👍'

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == ':mens:':
        data['sex'] = 1
    elif str(reaction.emoji) == ':womens:':
        data['sex'] = 2

    await ctx.send('Do you practice any sport regularly? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['sports'] = 1
    elif str(reaction.emoji) == '👎':
        data['sports'] = 2

    await ctx.send('Does anyone smoke at your home? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['smokers_home'] = 1
    elif str(reaction.emoji) == '👎':
        data['smokers_home'] = 2

    data['inclusion_criteria'] = -1

    await ctx.send('Anyone at home with suspected COVID-19 symptoms? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['symp_epi'] = 1
    elif str(reaction.emoji) == '👎':
        data['symp_epi'] = 0

    await ctx.send('Anyone at School had COVID-19 symptoms? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['school_symptoms_member_1'] = 1
        data['school_symptoms_member_2'] = 1
    elif str(reaction.emoji) == '👎':
        data['school_symptoms_member_1'] = 0
        data['school_symptoms_member_2'] = 0

    await ctx.send('Anyone at School with confirmed COVID-19? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['school_confirmed'] = 1
    elif str(reaction.emoji) == '👎':
        data['school_confirmed'] = 0

    await ctx.send('Do you present COVID-19 symptoms? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['symptoms_binary'] = 1
    elif str(reaction.emoji) == '👎':
        data['symptoms_binary'] = 0

bot.run(TOKEN)
