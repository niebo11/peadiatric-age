import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import pickle
import pandas as pd
import sklearn
import wikipedia

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

symptoms_01 = {'wheezing', 'crackles', 'dermatologic', 'rash', 'neuro', 'seizures', 'hypotonia', 'shock',
               'taste_smell', 'smell'}

wikipedia.set_lang("en")

def init():
    data = {'sex': 1, 'sports': 2, 'smokers_home': 2, 'inclusion_criteria': 2, 'sympt_epi': 1,
        'school_symptoms_member___1' : 1, 'school_symptoms_member___2': 1, 'school_confirmed': 1,
        'symptoms_binary': 1, 'fever': 2, 'tos': 2, 'crup':2, 'dysphonia':2, 'resp':2, 'tachypnea':2,
        'ausc_resp':2, 'wheezing':2, 'crackles':2, 'odynophagia':2, 'nasal_congestion':2,
        'fatiga':2, 'headache':2, 'conjuntivitis':2, 'ocular_pain':2, 'gi_symptoms':1, 'abdominal_pain':2,
        'vomiting': 2, 'dyarrea':2, 'dermatologic':1, 'rash':1, 'adenopathies':2, 'hepato':2, 'splenomegaly':2,
        'hemorrhagies':2, 'irritability':2, 'neuro':1, 'seizures':1, 'hypotonia':1, 'shock':1,
        'taste_smell':1, 'smell':1, 'vrs_result':2, 'flu_a_result':2, 'flu_b_result':2,
        'bacterial_infection':2, 'obesity': 1, 'flu_binary': 1, 'vaccines_binary': 1, 'coviral': 9}
    return data

def init_disease():
    data = {'cardiopathy': 2, 'hypertension': 2, 'pulmonar_disease': 2, 'asma': 2, 'nephrology': 2, 'hepatic':2,
            'neurologic': 2, 'diabetes': 2, 'tuberculosi': 2, 'idp': 2, 'neoplasia': 2, 'kawasaki': 2,
            'inflammation': 2, 'vih_others': 2}
    return data

def wiki_summary(arg):
    definition = wikipedia.summary(arg, sentences=1, chars=100, auto_suggest=True, redirect = True)
    return definition

actual_talking = ""

diseases = {'cardiopathy': 'Cardiopathy', 'hypertension': 'Hypertension', 'pulmonar_disease': 'Pulmonar diseases',
            'asma': 'Asma', 'nephrology': 'Chronic renal disease', 'hepatic': 'Chronic liver disease',
            'neurologic': 'Chronic neurologic disease', 'diabetes': 'Diabetes', 'tuberculosi': 'Tuberculosis',
            'idp': 'Primary immunodeficiency', 'neoplasia': 'Onco-haematological diseases',
            'kawasaki': 'Kawasaki syndrome', 'inflammation': 'Other inflammatory diseases',
            'vih_others': 'HIV infection or other secondary immunodeficiencies'}


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

@bot.command("me", help="Description of the bot")
async def me(ctx):
    await ctx.send("Hi, my name is Covid_Bot, I was created by Aleix Sarroca Soler and Niebo Zhang and I am here "
                   "to helping in everything I can. My most important task is "
                   "to help parents to detect a possible case of CoVid-19 in their children by comparing different"
                   " other cases I have. For this reason I will ask you some questions about the child, if you want me to"
                   " try to help you use the \"!covid\" command. Nice to meet you!")

@bot.command("define", help="Describe the first word given.")
async def answer(ctx, args):
    try:
        arg = args.split()
        await ctx.send(wiki_summary(arg))
    except wikipedia.exceptions.DisambiguationError as e:
        await ctx.send(str(e))
        await ctx.send('+' * 60)
        await ctx.send('DisambiguationError: The page name is ambiguous')

@bot.command("covid", help='The bot predict the possibility of CoVid-19 from simple questions.')
async def covid_predict(ctx):
    data = init()
    comordibity = False
    actual_talking = ctx.author
    tmpt = 'Now I am going to ask you a few questions and I would try to predict if you are ill :c.\n I am not ' \
           'scientifically accurate so If you don\'t feel well, please go to your nearest hospital as soon as possible.' \
           '\n Please answer with 👍 or 👎 reaction, thanks for your collaboration.'
    await ctx.send(tmpt)

    def checkSex(reaction, user):
        return reaction.message.content == tmpt and user == actual_talking and (str(reaction.emoji) == '🚹' or str(reaction.emoji) == '🚺')

    def check(reaction, user):
        return reaction.message.content == tmpt and user == actual_talking and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎')

    def check2(reaction, user):
        return user == actual_talking and str(reaction.emoji) == '👍'

    tmpt = 'Which is your gender? Answer with 🚹 🚺 reaction.'
    await ctx.send(tmpt)
    reaction, user = await bot.wait_for('reaction_add', check=checkSex)

    if str(reaction.emoji) == '🚹':
        data['sex'] = 1
    elif str(reaction.emoji) == '🚺':
        data['sex'] = 2

    tmpt = 'Do you practice any sport regularly? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['sports'] = 1
    elif str(reaction.emoji) == '👎':
        data['sports'] = 2

    tmpt = 'Does anyone smoke at your home? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['smokers_home'] = 1
    elif str(reaction.emoji) == '👎':
        data['smokers_home'] = 2

    data['inclusion_criteria'] = -1

    tmpt = 'Anyone at home with suspected COVID-19 symptoms? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['sympt_epi'] = 1
    elif str(reaction.emoji) == '👎':
        data['sympt_epi'] = 0

    tmpt = 'Anyone at School had COVID-19 symptoms? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['school_symptoms_member___1'] = 1
        data['school_symptoms_member___2'] = 1
    elif str(reaction.emoji) == '👎':
        data['school_symptoms_member___1'] = 0
        data['school_symptoms_member___2'] = 0

    tmpt = 'Anyone at School with confirmed COVID-19? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['school_confirmed'] = 1
    elif str(reaction.emoji) == '👎':
        data['school_confirmed'] = 0

    tmpt = 'Do you present COVID-19 symptoms? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['symptoms_binary'] = 1
    elif str(reaction.emoji) == '👎':
        data['symptoms_binary'] = 0

    message_aux = ('Which of these symptoms do you present? Mark them with the 👍 reaction. When you have ended'
                   ' react to this message with 👍. Wait until we advise you to start reacting.')
    await ctx.send(message_aux)

    for symptom in symptoms:
        await ctx.send(symptom)

    await ctx.send("Go on with your reactions!")

    notEnd = True
    while(notEnd):
        reaction, user = await bot.wait_for('reaction_add', check=check2)
        if reaction.message.content == message_aux:
            notEnd = False
        else:
            if reaction.message.content in extra_symptoms:
                dict = extra_symptoms[reaction.message.content]
                await ctx.send('Before finishing reacting to symptoms please answer the following questions.')
                for item in dict:
                    tmpt = ('Do you have ' + item + ' symptom. React with 👍/👎')
                    await ctx.send(tmpt)
                    reaction, user = await bot.wait_for('reaction_add', check=check)
                    if str(reaction.emoji) == '👍':
                        if dict[item] in symptoms_01:
                            data[dict[item]] = 2
                        else:
                            data[dict[item]] = 1

                await ctx.send('Keep reacting to your symptoms. Remember to react to the first sentence '
                               'with 👍 if you finished.')
            elif reaction.message.content in symptoms:
                if symptoms[reaction.message.content] in symptoms_01:
                    data[symptoms[reaction.message.content]] = 0
                else:
                    data[symptoms[reaction.message.content]] = 1


    tmpt = 'Have you taken any antigenic test for other respiratory viruses? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    tmpt = 'Do you have any bacterial infection? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['bacterial_infection'] = 1
    elif str(reaction.emoji) == '👎':
        data['bacterial_infection'] = 2

    tmpt = 'Do you have obesity? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['obesity'] = 1
    elif str(reaction.emoji) == '👎':
        data['obesity'] = 0

    tmpt = 'Seasonal Flu vaccine administered? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['flu_binary'] = 1
    elif str(reaction.emoji) == '👎':
        data['flu_binary'] = 0

    tmpt = 'Routine vaccines up to date? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        data['vaccines_binary'] = 1
    elif str(reaction.emoji) == '👎':
        data['vaccines_binary'] = 0

    tmpt = 'Do you have any Comorbidities? Answer with 👍/👎.'
    await ctx.send(tmpt)

    reaction, user = await bot.wait_for('reaction_add', check=check)

    if str(reaction.emoji) == '👍':
        comorbidity = True

    if not comorbidity:
        predict_data = pd.DataFrame(data, index = [0])
        file = open('model_main.pickle', 'rb')
        model = pickle.load(file)

        pred = model.predict(predict_data)
        if pred[0] == '0':
            await ctx.send('Congratulations! There is a great chance you aren\'t having CoVid-19. In any case, if you '
                          'start feeling worse, remember to call your CAP or go to the nearest hospital possible. Even if'
                          ' you are having CoVid-19, remember to wear your mask properly when you go out and wash your hands'
                          ' frequently!')
        else:
            await ctx.send('You have a big chance to have CoVid-19. If you didn\' talk to your doctor yet, please do it '
                           'as soon as possible. Remember to avoid contact with unnecessary people to make the tracking '
                           'easier in case you are ill, also you must wear your mask properly when you go out and try to'
                           ' wash your hands frequently!')
    else:
        tmpt = ('Now we will give you a list of comorbidities, if you suffer from any of them please react with 👍. When'
                ' you ended, react with 👍 to this message.')
        await ctx.send(tmpt)
        disease = init_disease()
        diseases_inv = {v: k for k, v in diseases.items()}

        for item in diseases_inv:
            await ctx.send(item)
        notEnd = True
        while(notEnd):
            reaction, user = await bot.wait_for('reaction_add', check=check2)

            if reaction.message.content in diseases_inv:
                disease[diseases_inv[item]] = 1
            elif reaction.message.content == tmpt:
                notEnd = False

        data = {**data, **disease}

        predict_data = pd.DataFrame(data, index = [0])

        file = open('model_1.pickle', 'rb')
        model = pickle.load(file)

        pred = model.predict(predict_data)

        if pred[0] == '0':
            await ctx.send('Congratulations! There is a great chance you aren\'t having CoVid-19. In any case, if you '
                          'start feeling worse, remember to call your CAP or go to the nearest hospital possible. Even if'
                          ' you are not having CoVid-19, remember to wear your mask properly when you go out and wash your hands'
                          ' frequently!')
        else:
            await ctx.send('You have a big chance to have CoVid-19. If you didn\' talk to your doctor yet, please do it '
                           'as soon as possible. Remember to avoid contact with unnecessary people to make the tracking '
                           'easier in case you are ill, also you must wear your mask properly when you go out and try to'
                           ' wash your hands frequently!')

bot.run(TOKEN)
