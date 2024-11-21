import requests, json

def connect():

        params = {'realm': '/partenaire'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {"grant_type": "client_credentials", "client_id": "PAR_cassoulet_7cf36b8a34476a5c87a9760a13c5821ac29e5c1d83a3076c8527dfc13a4d1911", "client_secret": "a5134b0e9e403797c02cfd76686b2c5787476e792f3f78b8fe9f68413c9e42ca", "scope": "api_offresdemploiv2 o2dsoffre"}

        response = requests.post('https://entreprise.pole-emploi.fr/connexion/oauth2/access_token', params=params, headers=headers, data=data)

        dico = json.loads(response.text)

        headers = {'Authorization': f'Bearer {dico["access_token"]}'}
        return(headers)

def get_domaines(headers):

    domaines = [
        ['A', 'Agriculture / Pêche / Espaces verts et naturels / Soins aux animaux'],
        ['B', "Arts / Artisanat d'art"],
        ['C', 'Banque / Assurance'],
        ['C15', 'Immobilier'],
        ['D', 'Commerce / Vente'],
        ['E', 'Communication / Multimédia'],
        ['F', 'Bâtiment / Travaux Publics'],
        ['G', 'Hôtellerie - Restauration / Tourisme / Animation'],
        ['H', 'Industrie'],
        ['I', 'Installation / Maintenance'],
        ['J', 'Santé'],
        ['K', 'Services à la personne / à la collectivité'],
        ['L', 'Spectacle'],
        ['L14', 'Sport'],
        ['M', 'Achats / Comptabilité / Gestion'],
        ['M13', "Direction d'entreprise"],
        ['M14', 'Conseil/Etudes'],
        ['M15', 'Ressources Humaines'],
        ['M16', 'Secrétariat / Assistanat'],
        ['M17', 'Marketing / Stratégie commerciale'],
        ['M18', 'Informatique / Télécommunication'],
        ['N', 'Transport / Logistique']
    ]

    return(domaines)

def get_types_contrats(headers):
    types = requests.get('https://api.pole-emploi.io/partenaire/offresdemploi/v2/referentiel/typesContrats', headers=headers)

    types = json.loads(types.text)

    types_contrats = []
    for type in types:
        types_contrats.append([type['code'], type['libelle']])

    return(types_contrats)

def get_niveaux_formations(headers):
    niveaux = requests.get('https://api.pole-emploi.io/partenaire/offresdemploi/v2/referentiel/niveauxFormations', headers=headers)

    niveaux = json.loads(niveaux.text)

    niveaux_formations = []
    for niveau in niveaux:
        niveaux_formations.append([niveau['code'], niveau['libelle']])

    return(niveaux_formations)

def recherche(headers, salaire = 0, domaine = 0, exp = 0, type = 0, qualif = 0, dep = 0, lvl = 0, mots_cles = 0, handicap = 0):
    requete = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?"

    if salaire:
        requete += f"salaireMin={salaire}&periodeSalaire=M&"

    if domaine:
        requete += f"grandDomaine={domaine}&"

    if exp:
        requete += f"experience={exp}&"

    if type:
        requete += f"typeContrat={type}&"

    if qualif:    
        requete += f"qualification={qualif}&"

    if dep:
        requete += f"departement={dep}&"

    if lvl:
        requete += f"niveauFormation={lvl}&"

    if mots_cles:
        requete += f"motsCles={mots_cles}&"

    if handicap != 0:
        requete += f"entreprisesAdaptees={handicap}"

    response = requests.get(requete, headers=headers)

    liste_jobs = []

    # Conversion de la réponse en objet JSON
    try:
        jobs = json.loads(response.text)
        for job in jobs["resultats"]:
            liste_jobs.append([job['lieuTravail']['libelle'], job['intitule'], job['origineOffre']['urlOrigine']])
    except:
        liste_jobs.append("Aucun résultat")

    return(liste_jobs)

def insert_BDD(data):


    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore

    # Use a service account.
    try:
        cred = credentials.Certificate(certificat)
        app = firebase_admin.initialize_app(cred)
    except ValueError:
        pass
    
    db = firestore.client()

    data['date'] = firestore.SERVER_TIMESTAMP
    db.collection('API_pole_emploi').add(data)
