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

    certificat = {
    "type": "service_account",
    "project_id": "devia-f6704",
    "private_key_id": "26941e799930afd7d93243a7658f6e393a8e1884",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2zaB+TWzBmShz\n4oMW4QYmCCjEHwvhC3VhpI8rhV3BMJyUEuQkYifMvpSdIDdoQWxBZ1GQ4OevL2v9\nAoYDz0tL8Yj+CM6k6X1qhZZzOEmANfA2V5i0XpyzIrCzv4v8c9GJR8PgJBDuHkoC\n4vFDf+8msNUZ64pF7wxv0VHZgOlM7LBUXY0akOW2uaGHycUakcPKo5jKNjTlFd3i\nJK9zDSlW9Dzqu2gEC1sGRJvwfg3TsAMtEuJiTtGQyhe0TfR8nu3bQ0X1/oNCq5yn\nMFOKcH0grLp+B3kTDuLHkmeZ1Jgy/1qp9gIDE8oYnokMS9MyqmoxIM4ZekWcswYc\nuhzmyFQjAgMBAAECggEAFcUIgey9MOkJFOk6wfTBA10hYwnCI7t2RSSQcEG3rT7E\nHCuLw9F0pUC6Tg6ndTZQABH1Ir3F7upE1U1W9wkuvGKNSpjIkyxt5SD3jnfQ46sz\naiVQaC/ZlXO3e2XU8+w5szw6qsILdMVipv6udg1m8O1KKNtmDMyvvHk/DW9Orqb6\n+Y1hoQZg6b80kjB8est2y9+WXSHndkoH9ArRlf7v4dV57s8Sv9DtxiQ55zFVfsZW\nGUHDwBAtgsnjfkJjfqGBvAiiCP6DUAKwqp776/mjlWWmNJIpC9CHsCT66k90qJ/O\n2u2bMvu2+vtRVSgzwJ6FSqGCs7nYBPm1QoSZkjiVMQKBgQDmxAKY2UOrUVXzgh+/\nNkbK27B1MtXbKAHFGvsLY12pCButycHKsX4y+MS0Vz2Fo+SOauI2zM9LwZkRGvO5\nldI5QBc03yZ9focwXLEHKMmp0lNC+d53wkVdSUxHWKvJ02xhlSlUoel0jMTsuXti\ny/fZoGjU5I4AQDCmUH/YO81K5QKBgQDKyvhAE9FJWWFfj3V0PFURDYeLWYbnppf9\n/Pl6v8mMknVrrDFYyH343y9M7cAVP7KhRZK2PS27MwkFdQNQ2D82XBKyz1Hmi1/y\nApDAo9u3BQKOu2ggaWFAuHDXe1BrcXfUtrYgwPUtEar6tXkBfD/q56iOm2WZTgUt\nKurdg9VKZwKBgQDM4pzXrpb5JVblw9OCBqOl+pXaCI99bDDeGs1n2ApRSGSi0S4h\nU6OTh/HFmGuEGvaTR+ye8Qrf3PyVBlP8ozuqHvA7viDDbTKEStfWXm1mPNo17fmK\nZM8HO0vhUKX9pJxmq3Ots6++DjnNYAVfu27MJzLMSjyVlmhbUb+gccAczQKBgEYo\nXCRG9uPKYU6fIgJZkRB6Psdt7Kcd0n2TVHgr+71/OdJLWzMdAb/k7sdNhWOUiucS\nW8Rie/zElj1mEwSYG55h0jI8WVhKJaJjUtLinXO+7viUS1zTOEscxCU4S0Uwl0Vn\nBLFmMCwsbZuYxslFxBMvm/fiOQ8Fl/LdYy3JmzPHAoGAAcOiy5yl3K7Cf+es3lYH\nTkilmTjLkmk7XaqujZpUYglWXck+VbYPj9AauGFHnbySxhBjrCUoDWTq2+llXObT\ny6Pgtuqd6Vlz8L5kk/RD+b5hiOHgQeKUyqoJ+9746h6jrL4nPWxNTCb/tTtBXAlE\nR9AEf+oYudh9FksU6/hLsEQ=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ay7ci@devia-f6704.iam.gserviceaccount.com",
    "client_id": "103202386953107051931",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ay7ci%40devia-f6704.iam.gserviceaccount.com"
    }

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
