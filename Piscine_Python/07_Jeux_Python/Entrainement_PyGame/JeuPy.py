from pygame import *
import os
import random

mixer.init(44100,-16,2,2048)

init() #initialise pygame

largeur = 1000
hauteur = 700

vitesseMonVaisseau = 5
vitesseMaSoucoupe = 5 
vitesseShoot = 8

fenetre = display.set_mode((largeur,hauteur)) # création de la fenêtre de jeu


gameOver = False #flag qui permettra de quitter le jeu. Pour le moment, on veut pas sortir

monVaisseau=image.load(os.getcwd()+"/images/space-ship-png-6.png")  #charge l'image du vaisseau  et définit un objet image pour la manipuler
coordMonVaisseau=monVaisseau.get_rect()     #on crée un objet rect qui permettra d’obtenir des infos et de la manipuler
largeurMonVaisseau = coordMonVaisseau.right - coordMonVaisseau.left
coordMonVaisseau.centerx=int(largeur/2) #on initialise la position du vaisseau au milieu de l'écran
coordMonVaisseau.bottom=hauteur-10 # et en bas, à 10 pixels du bas de l'écran  

maSoucoupe=image.load(os.getcwd()+"/images/soucoupe90.png")  #charge l'image du vaisseau  et définit un objet image pour la manipuler
coordMaSoucoupe=maSoucoupe.get_rect()     #on crée un objet rect qui permettra d’obtenir des infos et de la manipuler
largeurSoucoupe = coordMaSoucoupe.right-coordMaSoucoupe.left
coordMaSoucoupe.right= largeurSoucoupe + 10#on initialise la position du vaisseau au milieu de l'écran
coordMaSoucoupe.top=10 # et en haut, à 10 pixels du bas de l'écran  

shoot=image.load(os.getcwd()+"/images/shoot3.png")  #charge l'image du vaisseau  et définit un objet image pour la manipuler
coordShoot=shoot.get_rect()     #on crée un objet rect qui permettra d’obtenir des infos et de la manipuler
coordShoot.left=0

explosion = image.load(os.getcwd()+"/images/explosion-clipart-animated-gif-5-original.gif")  #charge l'image du vaisseau  et définit un objet image pour la manipuler
coordExplosion=coordMaSoucoupe



bougeGauche = False
bougeDroite = False 

bougeSoucoupeDroite = True
bougeSoucoupeGauche = False 

shootEnCours = False 
startShoot = False

afficheSoucoupe = True

soucoupeDroite = False
soucoupeGauche = False

randomSide = True

random_bit = random.getrandbits(1)
randomSide = bool(random_bit)


def startSoucoupe(VarBool):

        print("Fonction startSoucoup, VarBool = ", VarBool)
        #time.delay(2000)
        if VarBool:
            coordMaSoucoupe.left= 10#on initialise la position du vaisseau au milieu de l'écran
            bougeSoucoupeDroite = True
            bougeSoucoupeGauche = False
        else:
            coordMaSoucoupe.right= largeur#on initialise la position du vaisseau au milieu de l'écran
            bougeSoucoupeGauche = True
            bougeSoucoupeDroite = False
        coordMaSoucoupe.top = random.randint(10,300)

startSoucoupe(randomSide)

#------------------------------------------- boucle principale du jeu ----------------------------------------
while not gameOver: #  on y reste tant que gameOver = False

    random_bit = random.getrandbits(1)
    randomSide = bool(random_bit)
    print ("randomSide = ", randomSide)

     # --- On dessine les éléments sur l'écran --------------
    path = os.getcwd()
    print("path = ", path)
    fenetre.fill((128,128,128))  # on remplit tout écran d'une couleur unie - ici un gris moyen
    #os.chdir("./images") #on se place dans le dossier contenant les fichiers du projet
    sonTir = mixer.Sound(os.getcwd()+"/sons/shoot.wav")
    sonExplosion = mixer.Sound(os.getcwd()+"/sons/explosion.wav")    

   

    # --- traitement des évènements --------------

        # -- file d'évènements ---- 
    for e in event.get():
        if e.type==QUIT: #si on veut fermer la fenêtre (croix en haut à droite)
            gameOver=True   # on change le flag qui nous fera quitter la boucle
            print("Game OVER !")

        if e.type == KEYDOWN :
            if e.key == K_ESCAPE :
                gameOver = True

            if e.key == K_LEFT : # si la touche appuyée est la flèche gauche
                bougeGauche = True
            
            if e.key == K_RIGHT : # si la touche appuyée est la flèche gauche
                bougeDroite = True
            
            if e.key == K_SPACE :
                if shootEnCours :
                    continue
                startShoot = True

        if e.type == KEYUP :    
            if e.key == K_LEFT : # si la touche appuyée est la flèche gauche
                bougeGauche = False
            
            if e.key == K_RIGHT : # si la touche appuyée est la flèche gauche
                bougeDroite = False


    #print('coordMonVaisseau.left = {0} ; coordMonVaisseau.right = {1}'.format(coordMonVaisseau.left,coordMonVaisseau.right))
    print('coordMaSoucoupe.left = {0} ; coordMaSoucoupe.right = {1} ; ; coordMaSoucoupe.top = {2} ; coordMaSoucoupe.bottom = {3}'.format(coordMaSoucoupe.left,coordMaSoucoupe.right,coordMaSoucoupe.top,coordMaSoucoupe.bottom))
    print('coordShoot.left = {0}, coordShoot.right = {1}, coordShoot.top = {2}, coordShoot.bottom = {3}'.format(coordShoot.left,coordShoot.right,coordShoot.top,coordShoot.bottom))
    



    # --- interprétation des évènements --------------
    if bougeGauche:
        if coordMonVaisseau.left > 0:
            coordMonVaisseau.left-= vitesseMonVaisseau
        else:
            coordMonVaisseau.left=0
    if bougeDroite:
        if coordMonVaisseau.right<largeur:
            coordMonVaisseau.right+=vitesseMonVaisseau
        else:
             coordMonVaisseau.right=largeur

    
    if coordMaSoucoupe.right>=largeur:
        bougeSoucoupeDroite=False
        bougeSoucoupeGauche=True

    if coordMaSoucoupe.left<=0:
        bougeSoucoupeDroite=True
        bougeSoucoupeGauche=False
    
    if bougeSoucoupeDroite:
        coordMaSoucoupe.right+=vitesseMaSoucoupe
    if bougeSoucoupeGauche:
        coordMaSoucoupe.right-=vitesseMaSoucoupe

    if startShoot and not shootEnCours:

        coordShoot.centerx = coordMonVaisseau.right - largeurMonVaisseau / 2
        coordShoot.bottom=coordMonVaisseau.top - 10
        fenetre.blit(shoot,coordShoot)
        sonTir.play()		#joue le son du tir
    
        startShoot = False
        shootEnCours = True

    if shootEnCours:
        coordShoot.top-=vitesseShoot
        if coordShoot.bottom>=10:
            fenetre.blit(shoot,coordShoot)
        else:
            shootEnCours = False
            coordShoot.left=0

    if coordShoot.colliderect(coordMaSoucoupe): #si le shoot est entré en collision avec la soucoupe
        print("Colision ???????????????????????")
        afficheSoucoupe = False
        sonExplosion.play()
        fenetre.blit(explosion,coordExplosion)
        startSoucoupe(randomSide)   
    else:
        afficheSoucoupe = True

    if afficheSoucoupe:
        fenetre.blit(maSoucoupe,coordMaSoucoupe)




    fenetre.blit(monVaisseau,coordMonVaisseau)
    
    

    display.flip() # rafraichit l'affichage de l'écran (double buffering)

    # délais court pour ralentir l'animation
    time.delay(5)

    vitesseMaSoucoupe = random.randint(0, 7)

    
    
    

quit() #si on est là c'est qu'on est sorti de la boucle, donc on quitte proprement
