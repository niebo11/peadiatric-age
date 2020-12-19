# Discord CoVid-19 predictor Bot
QuizBot és un chat bot fet per l'assignatura llenguatges de programació del primer quadrimestre de 2020. La funció principal del chat bot és realitzar enquestes a partir del format del compilador que s'ha realitzat també per aquesta finalitat. El compilador llegeix una enquesta seguint un format gramatical i el transforma en dades que podrà llegir el nostre bot i realitza les enquestes. A més QuizBot permet fer gràfiques amb els resultats obtinguts i, per tant, facilitar l'anàlisis de les respostes obtingudes.

## Prerequisits

Per poder executar el QuizBot és necessari tenir instal·lat **Python3** i **Telegram**. A més en cas necessari també instal·lar les llibreries que es troben a *requeriments.txt*:

```
$ pip3 install -r requirements.txt
```

## Compilador

### Manual

El llenguatge *Enquestes* és un llenguatge que serveix per definir enquestes. El llenguatge ens permet declarar preguntes on està definit de la següent manera:

```
'Identificador de la pregunta' : PREGUNTA 'pregunta'
```
També té un altre tipus d'objectes que són les respostes, similar a les preguntes però té certes diferències:

```
'Identificador de la resposta' : RESPOSTA
'Identificador opcio 1' : 'opcio 1' ;
'Identificador opcio 2' : 'opcio 2' ;
'Identificador opcio 3' : 'opcio 3' ;
```

Un altre tipus de objectes són els *ITEMS* que ens permeten relacionar les preguntes amb respostes:
```
'Identificador item' : ITEM 'Identificador pregunta' -> 'Identificador resposta' 
```
Dins de les enquestes també tenim alternatives, és a dir, és un tipus d'objecte que ens permet relacionar preguntes amb preguntes tenint en compte el tipus de resposta que s'ha obtingut de l'usuari:
```
'Identificador alternativa': ALTERNATIVA 'Identificador pregunta' ['tupla resposta i identificador item']
```
Finalment per crear l'objecte enquesta s'ha de fer servir la següent estructura:
```
'Identificador enquesta' : ENQUESTA 'llista d'identificador de preguntes'
```
S'ha de tenir en compte que per cada codi només és pot declarar només un objecte **ENQUESTA**, en cas contrari es donarà error de compilació. És necessari finalitzar el codi amb **END** per donar per acabar el codi.

### Compilació

Per compilar el codi hi ha dues opcions:

1. Podem fer servir *test.main.py* que llegirà el codi i guardarà el graf a '../bot/' amb 'identificadorEnquesta'.pickle com nom de l'enquesta.
2. Fer servir *test.graph.py* que farà el mateix que *test.main.py* però també ens il·lustrarà amb un graf que és el flux que segueix l'enquesta que hem compilat amb el codi. (**S'ha de tenir en compte que el graph no es guarda al local**)

## Manual QuizBot

QuizBot és un bot bastant intuïtiu d'utilitzar que conté unes comandes predeterminades. Per més informació del que pot fer QuizBot fer servir la comanda **/help**. S'ha de tenir certs conceptes en compte a l'hora de fer servir QuizBot:
1. Les comandes */pie*, */bar*, */report* prenen l'última enquesta per defecte, en cas que no s'hagi executat cap enquesta QuizBot no retornarà cap report.
1. És necessari haver contestat almenys una enquesta per fer servir les comandes */pie*, */bar*, */report*
2. Els identificador són únics dins de cada enquesta, però poden existir identificadors semblants entre enquestes, per tant els identificadors enquestes són únics però els items (preguntes i respostes) i les alternatives no ho són necessàriament.

Els resultats de les enquestes es guardaran al mateix directori amb nom *IDEnquestaresults.pickle*.

## Execució

Per executar el QuizBot només fa falta executar la comanda següent:
```
$ python3 bot.py
```
I finalment ja podreu fer servir el QuizBot amb identificador **@JoanMuntanerBot** a Telegram

## Test existents

Existeixen 3 enquestes predefinits per testejar QuizBot:

1. Tenim *enquesta.txt* que és la versió més simplificada d'una enquesta. Enquesta segueix el format de l'enunciat que ens donen. La seva utilitat és veure que QuizBot funciona correctament.
2. *enquesta2.txt* és una versió més complexa de *enquesta.txt*, conté una alternativa dins d'una pregunta que també és una alternativa. Aquesta versió ens permet testejar que les alternatives amb alternatives funcionen correctament.
3. Finalment, *enquesta3.txt* és una versió ampliada de l'anterior, aquí s'ha ficat una pregunta més després de les alternatives. Aquesta versió ens permet veure que si encara queden preguntes després de finalitzar les alternatives, el QuizBot torna correctament fins a l'última pregunta.

# Test


## Autor
- Niebo Zhang Ye [zhangniebo@gmail.com]
- Aleix Sarroca Soler
