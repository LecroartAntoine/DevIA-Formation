import requests
import time
import re

__version__ = "1.2a"

class DefisUrl():
    def __init__(self, urlget, urlpost = None, debug = False, proxy = None, verify=False) :
        self.urlget = urlget
        self.urlpost = urlpost
        self.signature = None
        self.text = None
        self.debug = debug
        self.proxies = dict()
        self.verify = verify
        if proxy is not None:
            self.proxies['http'] = proxy
            self.proxies['https'] = proxy
        if self.urlpost == None:
            self.urlpost = re.sub('/get/','/post/',self.urlget)
    
    def get(self):
        question = requests.get(self.urlget, verify=self.verify, proxies=self.proxies)
        if self.debug: # on peut afficher le code de retour de la requête :
            print('GET:', question)
            # et le texte récupéré (qui contient la signature et l'énoncé) :
            print('TEXT:', question.text)
        # on sépare les lignes de l'entrée
        lignes = question.text.split("\n")
        #print(lignes)
        # la première ligne contient la signature
        self.signature=lignes[0]
        return lignes[1:]
        
    def post(self,reponse):
        res = requests.post(self.urlpost, verify=self.verify,
                            data={"sig":self.signature,"rep":reponse},
                            proxies=self.proxies)
        if self.debug:
            print(res)
            print(res.text)
        return res.text

print("defiurl.py version",__version__)