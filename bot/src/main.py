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
            'Shortness of breath or working of breathing':'resp', 'Tachypnea/Polypnea': 'tachypnea',
            'Respiratory ausculation': 'ausc_resp', 'Odynophagia': 'odynophagia',
            'Nasal congestion': 'nasal_congestion', 'Fatigue/Malaise':'fatiga', 'Headache':'headache',
            'Conjuntivitis': 'conjuntivitis', 'Retro-ocular pain': 'ocular_pain',
            'Gastrointestinal symptoms':'gi_symptoms', 'Skin signs/ symptoms' : 'dermatologic',
            'Lymphadenopathies': 'adenophaties', 'Hepatomegaly': 'hepato', 'Splenomegaly': 'splenomegaly',
            'Hemorrhagies': 'hemorrhagies', 'Irritability': 'irritability', 'Neurologic manifestations': 'neuro',
            'Shock signs': 'shock', 'Alteration in taste':'taste_smell', 'Alteration in smell': 'smell'}

respiratory_symptoms = {'Wheezing(sibilants)': 'wheezing', 'Crackles': 'crackles'}

grastrointestinal_symptoms = {'Abdominal pain': 'abdominal_pain', 'Vomiting/Nausees' : 'vomiting',
                              'Diarrhoes': 'dyarrea'}

# TODO skin symptoms

neurologic_symptoms = {'Seizures': 'seizures', 'Hypotonia/flaccidity': 'hypotonia'}

extra_symptoms = {'Respiratory ausculation': respiratory_symptoms,
                  'Gastrointestinal symptoms': grastrointestinal_symptoms,
                  'Neurologic manifestations': neurologic_symptoms}

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

    tmpt = 'Which is your gender? Answer with 🚹 🚺 reaction.'

    await ctx.send(tmpt)

    def checkSex(reaction, user):
        return reaction.message.content == tmpt and user == actual_talking and (str(reaction.emoji) == '🚹' or str(reaction.emoji) == '🚺')

    def check(reaction, user):
        return reaction.message.content == tmpt and user == actual_talking

    def check2(reaction, user):
        return user == actual_talking and str(reaction.emoji) == '👍'

    reaction, user = await bot.wait_for('reaction_add', check=checkSex)

    if str(reaction.emoji) == '🚹':
        data['sex'] = 1
    elif str(reaction.emoji) == '🚺':
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

    message_aux = ('Which of these symptoms do you present? Mark them with the 👍 reaction. When you have ended'
                   ' react to this message with 👍.')
    await ctx.send(message_aux)

    for symptom in symptoms:
        await ctx.send(symptom)

    notEnd = False
    while(notEnd):
        reaction, user = await bot.wait_for('reaction_add', check=check2)
        if reaction.message.content == message_aux:
            notEnd = True
        else:
            if reaction.message.content in extra_symptoms:
                print('entra')
                for item in extra_symptoms[reaction.message.content]:
                    tmpt = ('Do you have ' + item + ' symptom. React with 👍/👎')
                    await ctx.send(tmpt)
                    reaction, user = await bot.wait_for('reaction_add', check=check)
                    if str(reaction.emoji) == '👍':
                        data['symptoms_binary'] = 1

                await ctx.send('Keep reacting to your symptoms. Remember to react with 👍 if you finished.')

            data[symptoms[reaction.message.content]] = 1

#TOTS ELS SIMPTOMAS VAN AQUI

    await ctx.send('Have you taken any antigenic test for other respiratory viruses? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        #PREGUNTAR ELS VIRUSES
    elif str(reaction.emoji) == '👎':
        #NO PREGUNTAR ELS VIRUSES

    await ctx.send('Do you have any bacterial infection? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['bacterial_infection'] = 1
    elif str(reaction.emoji) == '👎':
        data['bacterial_infection'] = 2

    data['comorbi_binary'] = 1

    await ctx.send('Do you have obesity? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['obesity'] = 1
    elif str(reaction.emoji) == '👎':
        data['obesity'] = 0

    await ctx.send('Seasonal Flu vaccine administered? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['flu_binary'] = 1
    elif str(reaction.emoji) == '👎':
        data['flu_binary'] = 0

    await ctx.send('Routine vaccines up to date? Answer with 👍/👎.')

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['vaccines_binary'] = 1
    elif str(reaction.emoji) == '👎':
        data['vaccines_binary'] = 0

    data['coviral'] = 9

bot.run(TOKEN)
