# API par Élàne Carvalho & Antoine Lecroart

[↩️](..)
Bienvenue dans la documentation de l'API pour les fonctionnalités suivantes :

- /val qui retourne une valeur entiàre aléatoire comprise entre 0 et 100 
- /val?nb=n (oà¹ n est un nombre entier positif) qui retourne du code JSON contenant un tableau de n valeurs entiàres aléatoires comprises en -1000 et +1000
- /calc/add?n1=n&n2=m (oà¹ n et m sont des nombres entiers positifs) retourne un simple texte contenant le résultat de l'addition de n et m
- /calc/prod?n1=n&n2=m (oà¹ n et m sont des nombres entiers positifs) retourne un code HTML mis en forme qui présente dans un navigateur le calcul du produit de n et m sous la forme 4 x 5 = 20
- /img?num=n (oà¹ n vaut un chiffre compris en 1 et 9) pour retourner une des 9 images possibles

De plus, cette API permet également d'accéder aux informations des stations de vélo en libre-service de Besanà§on :

- stations_velo?id=n retourne l'ensemble des informations sur la station n (sous forme d'un document JSON) prises dans le document JSON : https://www.juleshaag.fr/devIA/devAPI/station_information.json
- stations_velo?id=n&addr qui retourne l'adresse de la station de vélo n, sous forme d'un texte
- stations_velo?id=n&cap qui retourne la capacité de la station de vélo n, sous forme d'un nombre entier
- stations_velo?id=toutes&cap qui retourne la capacité totale de l'ensemble des stations contenues dans le fichier
- stations_velo/n/addr qui retourne l'adresse de la station de vélo n, sous forme d'un texte
- stations_velo/n/cap qui retourne la capacité de la station de vélo n, sous forme d'un nombre entier
- stations_velo/toutes/cap qui retourne un JSON contenant, par id, la capacité de chaque station ainsi que la capacité de l'ensemble des stations contenues dans le fichier.

# Utilisation 

Pour utiliser cette API, téléchargez les fichiers pour l'execution du serveur : https://github.com/LecroartAntoine/DjangoApi/releases/tag/1.0 <br>

Il faudra ensuite installer python 3.8 ou ultérieur, sans oublier d'ajouter Python à  la variable PATH <br>

Ensuite, installez django et Pillow depuis le terminal: <br>
    `pip install django` <br>
    `pip install Pillow`

Puis, lancez le serveur en local.<br>
Pour cela, exécutez la commande suivante dans le terminal :<br>
    `python chemin/vers/serveur/manage.py runserver`

Cela démarrera le serveur local de l'API, ce qui vous permettra d'envoyer des requêtes à  l'aide de votre navigateur ou d'un autre client HTTP. Une fois le serveur démarré, vous pourrez accéder aux endpoints de l'API à  partir de l'URL http://127.0.0.1:8000/ OU http://localhost:8000.

### **/val**

Cet endpoint retourne une valeur entiàre aléatoire comprise entre 0 et 100.

- Endpoint : /val
- Méthode : GET
- Paramàtres : Aucun
- Réponse : Un nombre entier aléatoire compris entre 0 et 100

Exemple :

```
GET https://127.0.0.1:8000/val

Réponse : 42
```

### **/val?nb=n**

Cette endpoint retourne un tableau de n valeurs entiàres aléatoires comprises en -1000 et +1000.
- Endpoint : /val?nb=n
- Méthode : GET
- Paramàtres : nombre entier positif (obligatoire)
- Réponse : Un tableau JSON contenant n nombres entiers aléatoires compris entre -1000 et +1000

Exemple : 

```
GET http://127.0.0.1:8000/val?nb=5

Réponse : [345, -123, 789, 234, -897]
```

### **/calc/add?n1=n&n2=m**

Cette endpoint retourne un simple texte contenant le résultat de l'addition de n et m.

- Endpoint : /calc/add?n1=n&n2=m
- Méthode : GET
- Paramàtres :
    n1 : nombre entier positif (obligatoire)
    n2 : nombre entier positif (obligatoire)
- Réponse : Un texte contenant le résultat de l'addition de n1 et n2

Exemple :

```
GET http://127.0.0.1:8000/calc/add?n1=10&n2=5

Réponse : 15
```

### **/calc/prod?n1=n&n2=m**

Cette endpoint retourne un code HTML mis en forme qui présente dans un navigateur le calcul du produit de n et m sous la forme 4 x 5 = 20.

- Endpoint : /calc/prod?n1=n&n2=m
- Méthode : GET
- Paramàtres :
    n1 : nombre entier positif (obligatoire)
    n2 : nombre entier positif (obligatoire)
- Réponse : Une page HTML contenant le calcul du produit de n1 et n2 sous la forme "n1 x n2 = résultat"

Exemple :

```
GET http://127.0.0.1:8000/calc/prod?n1=4&n2=5

Réponse : 4 x 5 = 20
```

### **/img?num=n**

Cette endpoint retourne une des 9 images possibles à  partir du chiffre n compris entre 1 et 9.

- Endpoint : /img?num=n
- Méthode : GET
- Paramàtres :
    num : chiffre compris entre 1 et 9 (obligatoire)
- Réponse : L'image correspondant au chiffre spécifié

Exemple :

```
GET http://127.0.0.1:8000/img?num=3

Réponse : (l'image correspondant au chiffre 3)
```

## Utilisation accàs stations libre-service Besanà§on 

### **stations_velo?id=n**

Cette endpoint retourne l'ensemble des informations sur la station n (sous forme d'un document JSON) prises dans le document JSON : https://www.juleshaag.fr/devIA/devAPI/station_information.json.

- Endpoint : /stations_velo?id=n
- Méthode : GET
- Paramàtres :
    id : numéro de l'ID de la station (obligatoire)
- Réponse : Un document JSON contenant les informations de la station spécifiée par l'ID

Exemple : 

```
GET http://127.0.0.1:8000/stations_velo?id=17

Réponse : 
{
    "address": "5, RUE DE L'INDUSTRIE",
    "available_bikes": 7,
    "available_bike_stands": 12,
    "bike_stands": 19,
    "last_update": 1618576027000,
    "name": "La Fayette",
    "number": 17,
    "position": {
        "lat": 47.236488,
        "lng": 6.014331
    }
}
```

### **stations_velo?id=n&addr**

Cette endpoint retourne l'adresse de la station de vélo n, sous forme d'un texte.

- Endpoint : /stations_velo?id=n&addr
- Méthode : GET
- Paramàtres :
    id : numéro de l'ID de la station (obligatoire)
- Réponse : Un texte contenant l'adresse de la station spécifiée par l'ID

Exemple : 

```
GET http://127.0.0.1:8000/stations_velo?id=17&addr

Réponse : "5, RUE DE L'INDUSTRIE"
```

### **stations_velo?id=n&cap**

Cette endpoint retourne la capacité de la station de vélo n, sous forme d'un nombre entier.

- Endpoint : /stations_velo?id=n&cap
- Méthode : GET
- Paramàtres :
    id : numéro de l'ID de la station (obligatoire)
- Réponse : Un nombre entier représentant la capacité de la station spécifiée par l'ID

Exemple

```
GET http://127.0.0.1:8000/stations_velo?id=17&cap

Réponse : 19
```

### **stations_velo?id=n&cap&addr**

Cette endpoint retourne la capacité et l'adresse de la station de vélo n, sous forme d'un texte.

- Endpoint : /stations_velo?id=n&cap&addr
- Méthode : GET
- Paramàtres :
    id : numéro de l'ID de la station (obligatoire)
- Réponse : Un texte contenant la capacité et l'adresse de la station spécifiée par l'ID

Exemple

```
GET http://127.0.0.1:8000/stations_velo?id=17&cap

Réponse : 
"Adresse : 5, RUE DE L'INDUSTRIE
Capacité : 19"
```

### **stations_velo?id=toutes&cap**

Cette endpoint retourne la capacité totale de l'ensemble des stations contenues dans le fichier.

- Endpoint : /stations_velo?id=toutes&cap
- Méthode : GET
- Paramàtres :
    id : "toutes" (obligatoire)
- Réponse : Un nombre entier représentant la capacité totale de toutes les stations

Exemple : 

```
GET http://127.0.0.1:8000/stations_velo?id=toutes&cap

Réponse : 400
```

### **stations_velo/n/addr**

Cette endpoint retourne l'adresse de la station de vélo n, sous forme d'un texte.

- Endpoint : /stations_velo/n/addr
- Méthode : GET
- Paramàtres :
    n : numéro de l'ID de la station (obligatoire)
- Réponse : Un texte contenant l'adresse de la station spécifiée par l'ID

Exemple : 

```
GET http://127.0.0.1:8000/stations_velo/17/addr

Réponse : "5, RUE DE L'INDUSTRIE"
```

### **stations_velo/n/cap**

Cette endpoint retourne la capacité de la station de vélo n, sous forme d'un nombre entier.

- Endpoint : /stations_velo/n/cap
- Méthode : GET
- Paramàtres :
    n : numéro de l'ID de la station (obligatoire)
- Réponse : Un nombre entier représentant la capacité de la station spécifiée par l'ID

Exemple : 

```
GET http://127.0.0.1:8000/stations_velo/17/cap

Réponse : 19
```

### **stations_velo/toutes/cap**

Cette endpoint retourne un JSON contenant, par ID, la capacité de chaque station ainsi que la capacité de l'ensemble des stations contenues dans le fichier.

- Endpoint : /stations_velo/toutes/cap
- Méthode : GET
- Paramàtres : Aucun
- Réponse : Un document JSON contenant les capacités de toutes les stations, ainsi que la capacité totale de l'ensemble des stations

Exemple : 

```
GET http://127.0.0.1:8000/stations_velo/toutes/cap

Réponse : 
{
    "1":{
        "capacité": 20
    },
    "2":{}
        "capacité": 10
    },
    "3":{
        "capacité": 12
    },
    ...
    "Capacité totale": 1000
}
```

## Conclusion

Vous avez maintenant accàs à  l'API pour accéder à  différents aux informations des stations de vélo en libre-service de Besanà§on. N'oubliez pas de terminer le serveur local en utilisant la commande Ctrl+C dans votre terminal lorsque vous avez terminé d'utiliser l'API.
