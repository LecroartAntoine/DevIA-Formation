import json
import os

with open(os.path.dirname(os.path.abspath(__file__)) + '/demandes.json', "r") as file:

    data = json.load(file)

dico = data["data"]


for key in dico:

    data["data"][key]['etablissement'] = 'JulesHaag'
    data["data"][key]['classes'] = 'SNIR1'

    traitement = dico[key]['chemin'].split('/')
    
    for i, element in enumerate(traitement):

        if element == 'matieres':
            data["data"][key]['matiere'] = traitement[i+1]
            data["data"][key]['parcours'] = traitement[i+2]
            data["data"][key]['activite'] = traitement[i+3]

        elif element == 'progression':
            data["data"][key]['parcours'] = traitement[i+1]
            data["data"][key]['activite'] = traitement[i+2]

with open(os.path.dirname(os.path.abspath(__file__)) + "/demandes_traitées.json", "w") as file:

    json.dump(data, file)