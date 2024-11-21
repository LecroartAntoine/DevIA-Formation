import random
import discord
from unidecode import unidecode

with open ("Insultes.txt", "r", encoding = 'utf-8') as file:
    insultes = file.read()

insultes = insultes.split('\n')

with open ("Salutations.txt", "r", encoding = 'utf-8') as file:
    salutations = file.read()

salutations = salutations.split('\n')

variantes = ['le beau gosse', ", ça va ?", 'ma couille droite', 'mon gars sur', ", à l'aise blaize ?", 'mon bébou', ", ça va bébou ?", 'le king', "ma p'tite gueule"]
bot_insultes = ['FDP', 'connard', 'enculé', 'gros con', 'petit con']

def handle_response(message_raw, name):

    message_raw = message_raw.lower()
    message_raw = message_raw.split()
    message = []
    for mot in message_raw:
        message.append(unidecode(mot))

    juron = False
    for mot in message:
        if mot in insultes:
            juron = True
    if juron:
        return f'{name} parles mieux {bot_insultes[random.randrange(0, len(bot_insultes))]}'

    elif message[0] in salutations:

        return f'Salut {name} {variantes[random.randint(0, 8)]}'

    elif message[-1] == '?':
        return f'Poses pas de questions {bot_insultes[random.randrange(0, len(bot_insultes))]}'

    if message[0] == '/help':
        return 'Appelles le SAV au 36 30'
