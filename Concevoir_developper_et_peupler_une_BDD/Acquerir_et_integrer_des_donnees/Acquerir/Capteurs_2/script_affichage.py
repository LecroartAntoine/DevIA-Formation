import json, requests, time

# Récupération des données
data = json.loads(requests.get('http://192.168.20.27/modulesGrove.php?all').text)

# Affichage si mouvement
if data['PIR'] == 1:
    requests.get(f"http://192.168.20.27/modulesGrove.php?texte=INTRUS !!& couleur=255,0,0")

# Affichage si température non lisible

while data['temperature'] == '?':
    time.sleep(1)

# Affichage température supérieure 25
if float(data['temperature']) > 25 :
    requests.get(f"http://192.168.20.27/modulesGrove.php?texte=Temp : {data['temperature']} C& couleur=0,255,0")

else:
    # Affichage température inférieure égale 25
    requests.get(f"http://192.168.20.27/modulesGrove.php?texte=Temp : {data['temperature']} C& couleur=0,0,255")