import pygame
import os
import random
import threading as t
pygame.init()

WIDTH, HEIGHT = 608, 800 #Taille de la fenetre largeur/hauteur

FPS = 60 #Définition du nombre d'images par secondes

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #On définit la fenêtre
pygame.display.set_caption("Pac Man") #Nom de la fenetre

ROWS = 19 #Nombres de lignes de la matrice qui gère la carte
COLS = 22 #Nombres de colones de la matrice qui gère la carte
SIZE = WIDTH/ROWS #Ratio entre taille de la fenêtre et nombre de lignes

#---Définition des évènements
SCORE = pygame.USEREVENT + 1 #Score
LIFE = pygame.USEREVENT + 2 #Perte d'une Vie
POWER_UP = pygame.USEREVENT + 3 #Évènement "pac man peut manger les fantômes"
POWER_UP_END = pygame.USEREVENT + 4 #Fin de l'évènement "pac man peut manger les fantômes"
EAT_GHOST_1 = pygame.USEREVENT +5 #Pac man a mangé le fantôme n°1
EAT_GHOST_2 = pygame.USEREVENT +6 #Pac man a mangé le fantôme n°2
EAT_GHOST_3 = pygame.USEREVENT +7 #Pac man a mangé le fantôme n°3
INVINCIBLE = pygame.USEREVENT +8 #Pac man est invincible pendant 3 secondes


#---Importation et initialisation des musiques-------------
pygame.mixer.init() 
MUSIC = pygame.mixer.music.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Music.wav' )
WAKKA = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Wakka.wav' )
WINNER = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '\Assets\You win.wav' )
GAME_OVER = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Game Over.wav' )

#--------Initialisation des polices d'écriture---------------
pygame.font.init() 
FONT = pygame.font.SysFont('Impact', 40 )
END_FONT = pygame.font.SysFont("Impact", 100 )

WIDTH_PMAN, HEIGHT_PMAN = 25, 25 # Définition taille du pac man
PAC_MAN = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Pac Man.png' ), (WIDTH_PMAN, HEIGHT_PMAN) ) #Importation et redimension de l'image du pac man
PMAN_SPEED = 2 #Définition vitesse du pac man

#Importation et redimension des images des fantômes
RED_GHOST_R = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Red ghost r.png'), (WIDTH_PMAN, HEIGHT_PMAN) )
RED_GHOST_L = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Red ghost l.png'), (WIDTH_PMAN, HEIGHT_PMAN) )
BLUE_GHOST_R = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Blue ghost r.png'), (WIDTH_PMAN, HEIGHT_PMAN) )
BLUE_GHOST_L = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Blue ghost l.png'), (WIDTH_PMAN, HEIGHT_PMAN) )
YELLOW_GHOST_R = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Yellow ghost r.png'), (WIDTH_PMAN, HEIGHT_PMAN) )
YELLOW_GHOST_L = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Yellow ghost l.png'), (WIDTH_PMAN, HEIGHT_PMAN) )
SICK_GHOST = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Sick ghost.png'), (WIDTH_PMAN, HEIGHT_PMAN) )

OUTLINE_COLOR = (0, 170, 255) #Couleur contour des murs

#----Variables globals---------
want_to_move = [False, False, False, False] #Mouvements du pac man (liste contenant les 4 directions possibles, vrai si on veut bouger dans cette direction)
move_image = -2 #Direction de l'image du pac man
#Comme pac man mais pour les fantômes, chaque fantôme à ces variables globals uniques
ghost_1_want_to_move = [False, False, False, False]
ghost_1_move = -2
alea_1 = 0 #Variable qui génère les mouvements du fantôme aléatoirement 
ghost_2_want_to_move = [False, False, False, False]
ghost_2_move = -2
alea_2 = 0
ghost_3_want_to_move = [False, False, False, False]
ghost_3_move = -2
alea_3 = 0

#----Fonction affichage---------
#On reçoit la carte à dessiner, le pac man, le score, les fantômes, le nombre de vie et le booléen qui gère le "power up"
def  draw_window(map, pac_man, score, ghost_1, ghost_2, ghost_3, lives, power_up):
    WIN.fill("black")#On remplit l'arrière plan en noir

    for i in range (1, lives+1):#Affichage des vies: on affiche une image de pac man pour représenter une vie, en bas à droite de l'écran
        WIN.blit(PAC_MAN, (WIDTH-WIDTH_PMAN * i - (i*20), HEIGHT - SIZE))
    
    # Affichage de la carte:
    for i, row in enumerate(map):
        y = SIZE * i #On multiplie l'indice de notre matrice "carte" par le ratio taille de l'écran/nombre de colones dans la carte pour trouver la position de y sur l'écran
        for j, value in enumerate(row):
            x = SIZE * j #On multiplie l'indice de notre matrice "carte" par le ratio taille de l'écran/nombre de colones dans la carte pour trouver la position de x sur l'écran
            if value == '#': # Si '#' = si mur
                pygame.draw.rect(WIN, OUTLINE_COLOR, (x, y, SIZE+2, SIZE+2), 4 ) # Affiche un contour rectangulaire d'épaisseur 4
            elif value == '1': # Si '1' = si nourriture 
                pygame.draw.rect(WIN, "white", (x + SIZE/2, y+ SIZE/2, 4, 4) ) # Affiche petit un carré banc de 4 de coté
            elif value == '2': # Si '2' = si 'power up'
                pygame.draw.circle(WIN, "white", (x + SIZE/2, y+SIZE/2), SIZE/5) # Affiche un rond blanc de Size/5 de large
            elif value == ':': # Si ':' = si porte qui laisse passer les fantômes, mais pas pac man
                pygame.draw.rect(WIN, OUTLINE_COLOR, (x, y+ SIZE/2, SIZE, 4) ) # Affiche une ligne bleu de Size de long, 4 de haut

    # Affichage du pac man
    if move_image == -2 : # Si pac man va vers la gauche
        WIN.blit(pygame.transform.rotate(PAC_MAN, 180), (pac_man.x+5, pac_man.y+5) ) # On affiche l'image du pac man tourné vers la gauche
    if move_image == -1: # Si pac man va vers la droite
        WIN.blit(pygame.transform.rotate(PAC_MAN, 0), (pac_man.x+5, pac_man.y+5) ) # On affiche l'image du pac man tourné vers la droite
    if move_image == 2: # Si pac man va vers le haut
        WIN.blit(pygame.transform.rotate(PAC_MAN, 270), (pac_man.x+5, pac_man.y+5) ) # On affiche l'image du pac man tourné vers le haut
    if move_image == 1: # Si pac man va vers le bas 
        WIN.blit(pygame.transform.rotate(PAC_MAN, 90), (pac_man.x+5, pac_man.y+5) ) # On affiche l'image du pac man tourné vers le bas

    # Affichage des fantômes
    if power_up:# Si pac man a mangé un 'power up', l'image des fantômes devient l'image d'un fantôme 'malade'

        WIN.blit(SICK_GHOST, (ghost_1.x+3, ghost_1.y+3)) 
        WIN.blit(SICK_GHOST, (ghost_2.x+3, ghost_2.y+3))
        WIN.blit(SICK_GHOST, (ghost_3.x+3, ghost_3.y+3))
    
    else:# Sinon, affichage de chaque fantôme avec leur couleur respective
        # Fantôme 1
        if ghost_1_move == -2: # Si le fantôme va vers la gauche
            WIN.blit(BLUE_GHOST_L, (ghost_1.x+3, ghost_1.y+3))
        if ghost_1_move == -1: # Si le fantôme va vers la droite
            WIN.blit(BLUE_GHOST_R, (ghost_1.x+3, ghost_1.y+3))

        # Fantôme 2
        if ghost_2_move == -2:
            WIN.blit(RED_GHOST_L, (ghost_2.x+3, ghost_2.y+3))
        if ghost_2_move == -1:
            WIN.blit(RED_GHOST_R, (ghost_2.x+3, ghost_2.y+3))

        # Fantôme 3
        if ghost_3_move == -2:
            WIN.blit(YELLOW_GHOST_L, (ghost_3.x+3, ghost_3.y+3))
        if ghost_3_move == -1:
            WIN.blit(YELLOW_GHOST_R, (ghost_3.x+3, ghost_3.y+3))

    # Affichage du score, en bas à gauche
    text = FONT.render(str(f"Score: {score}"), 1, "white")
    WIN.blit(text, (0, HEIGHT-text.get_height()) )
    

    pygame.display.update()# On rafraîchit la fenêtre

#--------Fonction qui gère l'interaction de pac man avec la carte---------
def map_interaction(map, pac_man):# On reçoit la carte et pac man

    for i, row in enumerate(map): # Pour chaque ligne de la matrice carte
        for j, value in enumerate(row): # Pour chaque colone dans la ligne de la matrice carte
            
            if round(pac_man.x/SIZE)  == j and round(pac_man.y/SIZE)  == i and value == '1': # Si l'emplacement où est pac man contient de la nourriture 
                pygame.event.post(pygame.event.Event(SCORE)) # Évènement score 
                WAKKA.play() # On joue le son 'pac man a mangé'
                map[i][j] = 0 # On enlève la nourriture de cet emplacement

            if round(pac_man.x/SIZE)  == j and round(pac_man.y/SIZE)  == i and value == '2': # Si l'emplacement où est pac man contient un 'power up'
                pygame.event.post(pygame.event.Event(POWER_UP)) # Évènement 'power up'
                map[i][j] = 0 # On enlève le 'power up' de cet emplacement

            if round(pac_man.x/SIZE)  == j and round(pac_man.y/SIZE)  == i and value == '3': # Si l'emplacement où est pac man est le téléporteur gauche
                pac_man.x = WIDTH-SIZE*3 # Pac ma est téléporté à droite

            if round(pac_man.x/SIZE)  == j and round(pac_man.y/SIZE)  == i and value == '4': # Si l'emplacement où est pac man est le téléporteur droit
                pac_man.x = SIZE*2 # Pac ma est téléporté à gauche

#-------Fonction qui gère les déplacements de pac man-------------
def movement(keys_pressed, pac_man, hitmap): # On reçoit les touches pressées, pac man et la carte de collision
    # Variables globales pour pac man
    global want_to_move 
    global move_image

    if keys_pressed[pygame.K_LEFT] : # Bouton gauche pressé
        want_to_move[0] = True # On veut bouger à gauche
        want_to_move[1] = False # On ne veut pas bouger à droite en même temps qu'à gauche
        
    if keys_pressed[pygame.K_RIGHT]: # Bouton droit pressé
        want_to_move[0] = False # On ne veut pas bouger à droite en même temps qu'à gauche
        want_to_move[1] = True # On veut bouger à droite
        
    if keys_pressed[pygame.K_UP]: # Bouton haut pressé
        want_to_move[2] = True # On veut bouger en haut
        want_to_move[3] = False # On ne veut pas bouger en bas en même temps qu'en haut
        
    if keys_pressed[pygame.K_DOWN]: # Bouton bas pressé
        want_to_move[2] = False # On ne veut pas bouger en haut en même temps qu'en bas
        want_to_move[3] = True # On veut bouger en bas
    
    if want_to_move[0]: #Si on veut aller à gauche
        if not hitmap[round(pac_man.y / SIZE)][round(pac_man.x / SIZE) - 1].colliderect(pac_man): # S'il n'y a pas de mur à gauche
            pac_man.x -= PMAN_SPEED # On bouge à gauche
        else:
            want_to_move[0] = False # Sinon on ne bouge plus à gauche 
        if not want_to_move[2] and not want_to_move[3]: # Si on n'est pas entrain de bouger en haut ou en bas
                    move_image = -2 # L'image de pac man sera tourné vers la gauche

    if want_to_move[1]: #Si on veut aller à droite
        if not hitmap[round(pac_man.y / SIZE)][round(pac_man.x / SIZE) + 1].colliderect(pac_man):  # S'il n'y a pas de mur à droite
            pac_man.x += PMAN_SPEED # On bouge à droite
        else:
            want_to_move[1] = False  # Sinon on ne bouge plus à droite
        if not want_to_move[2] and not want_to_move[3]: # Si on n'est pas entrain de bouger en haut ou en bas
            move_image = -1 # L'image de pac man sera tourné vers la droite

    if want_to_move[2]: #Si on veut aller en haut
        if not hitmap[round(pac_man.y / SIZE) - 1][round(pac_man.x / SIZE)].colliderect(pac_man): # S'il n'y a pas de mur en haut
            pac_man.y -= PMAN_SPEED # On bouge en haut
        else:
            want_to_move[2] = False # Sinon on ne bouge plus en haut
        if not want_to_move[0] and not want_to_move[1]:# Si on n'est pas entrain de bouger à droite ou à gauche
            move_image = 1  # L'image de pac man sera tourné vers le haut

        
    if want_to_move[3]: #Si on veut aller en bas
        if not hitmap[round(pac_man.y / SIZE) + 1][round(pac_man.x / SIZE)].colliderect(pac_man): # S'il n'y a pas de mur en bas
            pac_man.y += PMAN_SPEED # On bouge en bas
        else:
            want_to_move[3] = False # Sinon on ne bouge plus en bas
        if not want_to_move[0] and not want_to_move[1]: # Si on n'est pas entrain de bouger à droite ou à gauche
            move_image = 2 # L'image de pac man sera tourné vers le bas
        
#----Fonction qui gère les mouvements du fantôme 1------------
def ghost_1_movement(ghost_1, hitmap, map): # On reçoit le fantôme 1, la carte des collisions et la carte 

    global ghost_1_want_to_move # Variable global des mouvements du fantôme 1
    global ghost_1_move # Variable global de l'orientation de l'image du fantôme 1
    global alea_1 # Variable global du nombre aléatoire qui détermine la direction que prendra le fantôme

    if alea_1 == -2 : # Si la variable aléatoire est -2
        ghost_1_want_to_move[0] = True # Le fantôme veut aller à gauche
        
    if alea_1 == -1: # Si la variable aléatoire est -1
        ghost_1_want_to_move[1] = True # Le fantôme veut aller à droite
        
    if alea_1 == 0: # Si la variable aléatoire est 0
        ghost_1_want_to_move[2] = True # Le fantôme veut aller en haut
        
    if alea_1 == 1: # Si la variable aléatoire est 1
        ghost_1_want_to_move[3] = True # Le fantôme veut aller en bas
        
    if ghost_1_want_to_move[0]: # Si le fantôme veut aller à gauche
        ghost_1_move = -2 # On oriente l'image du fantôme vers la gauche
        ghost_1.x -= PMAN_SPEED # Le fantôme bouge vers la gauche
        if hitmap[round(ghost_1.y / SIZE)][round(ghost_1.x / SIZE) - 1].colliderect(ghost_1): # Si le fantôme entre en collision avec un mur
            ghost_1.x += PMAN_SPEED # Il recule (pour ne plus être en collision)
            alea_1 = random.randrange(0, 2) # On génère un nouveau nombre aléatoire pour donner un nouvelle direction vers le haut ou le bas (0 ou 1)
            ghost_1_want_to_move[0] = False # Le fantôme ne veut plus aller à gauche

    # Comme précédemment mais vers la droite
    if ghost_1_want_to_move[1]: 
        ghost_1.x += PMAN_SPEED
        ghost_1_move = -1
        if hitmap[round(ghost_1.y / SIZE)][round(ghost_1.x / SIZE) + 1].colliderect(ghost_1):
            ghost_1.x -= PMAN_SPEED 
            alea_1 = random.randrange(0, 2)
            ghost_1_want_to_move[1] = False
    
    # Comme précédemment mais vers le haut
    if ghost_1_want_to_move[2]: 
        ghost_1.y -= PMAN_SPEED
        if hitmap[round(ghost_1.y / SIZE) - 1][round(ghost_1.x / SIZE)].colliderect(ghost_1) and map[round(ghost_1.y / SIZE) - 1][round(ghost_1.x / SIZE)] != ':': # On s'assure aussi que le mur n'est pas le portail qui laisse passer les fantômes mais pas pac man (':'), il est juste au dessus du spawn des fantômes. 
            ghost_1.y += PMAN_SPEED 
            alea_1 = random.randrange(-2, 0) # On génère un nouveau nombre aléatoire pour donner un nouvelle direction vers la gauche ou la droite (-2 ou -1)
            ghost_1_want_to_move[2] = False
    # Comme précédemment mais vers le bas
    if ghost_1_want_to_move[3]: 
        ghost_1.y += PMAN_SPEED
        if hitmap[round(ghost_1.y / SIZE) + 1][round(ghost_1.x / SIZE)].colliderect(ghost_1):
            ghost_1.y -= PMAN_SPEED 
            alea_1 = random.randrange(-2, 0)
            ghost_1_want_to_move[3] = False       

#----Fonction qui gère les mouvements du fantôme 2, même fonctionnement que 'ghost_1_mouvement'------------
def ghost_2_movement(ghost_2, hitmap, map):

    global ghost_2_want_to_move
    global ghost_2_move
    global alea_2

    if alea_2 == -2 :
        ghost_2_want_to_move[0] = True   
        
    if alea_2 == -1:
        ghost_2_want_to_move[1] = True

    if alea_2 == 0:
        ghost_2_want_to_move[2] = True
        
    if alea_2 == 1:
        ghost_2_want_to_move[3] = True
        
    if ghost_2_want_to_move[0]: 
        ghost_2.x -= PMAN_SPEED
        ghost_2_move = -2
        if hitmap[round(ghost_2.y / SIZE)][round(ghost_2.x / SIZE) - 1].colliderect(ghost_2):
            ghost_2.x += PMAN_SPEED
            alea_2 = random.randrange(0, 2)
            ghost_2_want_to_move[0] = False

    if ghost_2_want_to_move[1]: 
        ghost_2.x += PMAN_SPEED
        ghost_2_move = -1
        if hitmap[round(ghost_2.y / SIZE)][round(ghost_2.x / SIZE) + 1].colliderect(ghost_2):
            ghost_2.x -= PMAN_SPEED 
            alea_2 = random.randrange(0, 2)
            ghost_2_want_to_move[1] = False
            
    if ghost_2_want_to_move[2]: 
        ghost_2.y -= PMAN_SPEED
        if hitmap[round(ghost_2.y / SIZE) - 1][round(ghost_2.x / SIZE)].colliderect(ghost_2) and map[round(ghost_2.y / SIZE) - 1][round(ghost_2.x / SIZE)] != ':':
            ghost_2.y += PMAN_SPEED 
            alea_2 = random.randrange(-2, 0)
            ghost_2_want_to_move[2] = False

    if ghost_2_want_to_move[3]: 
        ghost_2.y += PMAN_SPEED
        if hitmap[round(ghost_2.y / SIZE) + 1][round(ghost_2.x / SIZE)].colliderect(ghost_2):
            ghost_2.y -= PMAN_SPEED 
            alea_2 = random.randrange(-2, 0)
            ghost_2_want_to_move[3] = False       

#----Fonction qui gère les mouvements du fantôme 3, même fonctionnement que 'ghost_1_mouvement'------------
def ghost_3_movement(ghost_3, hitmap, map):

    global ghost_3_want_to_move
    global ghost_3_move
    global alea_3

    if alea_3 == -2 : # Aller à gauche
        ghost_3_want_to_move[0] = True   
        
    if alea_3 == -1: # Aller à droite
        ghost_3_want_to_move[1] = True
        
    if alea_3 == 0: # Aller en haut
        ghost_3_want_to_move[2] = True
        
    if alea_3 == 1: # Aller en bas
        ghost_3_want_to_move[3] = True
        
    if ghost_3_want_to_move[0]: 
        ghost_3.x -= PMAN_SPEED
        ghost_3_move = -2
        if hitmap[round(ghost_3.y / SIZE)][round(ghost_3.x / SIZE) - 1].colliderect(ghost_3):
            ghost_3.x += PMAN_SPEED
            alea_3 = random.randrange(0, 2)
            ghost_3_want_to_move[0] = False
                
    if ghost_3_want_to_move[1]: 
        ghost_3.x += PMAN_SPEED
        ghost_3_move = -1
        if hitmap[round(ghost_3.y / SIZE)][round(ghost_3.x / SIZE) + 1].colliderect(ghost_3):
            ghost_3.x -= PMAN_SPEED 
            ghost_3_want_to_move[1] = False
            alea_3 = random.randrange(0, 2)

    if ghost_3_want_to_move[2]: 
        ghost_3.y -= PMAN_SPEED
        if hitmap[round(ghost_3.y / SIZE) - 1][round(ghost_3.x / SIZE)].colliderect(ghost_3) and map[round(ghost_3.y / SIZE) - 1][round(ghost_3.x / SIZE)] != ':':
            ghost_3.y += PMAN_SPEED 
            alea_3 = random.randrange(-2, 0)
            ghost_3_want_to_move[2] = False

    if ghost_3_want_to_move[3]: 
        ghost_3.y += PMAN_SPEED
        if hitmap[round(ghost_3.y / SIZE) + 1][round(ghost_3.x / SIZE)].colliderect(ghost_3):
            ghost_3.y -= PMAN_SPEED 
            alea_3 = random.randrange(-2, 0)
            ghost_3_want_to_move[3] = False       

#------Fonction qui gère la collision entre pac man et les fantômes--------
def got_catched(pac_man, ghost_1, ghost_2, ghost_3, power_up): # On reçoit pac man, les fantômes, et l'état du power up (actif/inactif)

    if pac_man.colliderect(ghost_1): # Si pac man entre en collision avec le fantôme 1
        if power_up: # Si le power up est actif
            pygame.event.post(pygame.event.Event(EAT_GHOST_1) ) # Évènement le Fantôme est mangé
        else: # Sinon
            pygame.event.post(pygame.event.Event(LIFE) ) # Événement perte d'une vie
            
    # Même chose avec le fantôme 2
    if pac_man.colliderect(ghost_2):
        if power_up:
            pygame.event.post(pygame.event.Event(EAT_GHOST_2) )
        else:
            pygame.event.post(pygame.event.Event(LIFE) )

    # Même chose avec le fantôme 3
    if pac_man.colliderect(ghost_3):
        if power_up:
            pygame.event.post(pygame.event.Event(EAT_GHOST_3) )
        else:
            pygame.event.post(pygame.event.Event(LIFE) )
            
#-----Gestion de la défaite-----
def draw_lose():
    pygame.mixer.music.stop() # On stop la musique
    GAME_OVER.play() # On joue le son de défaite
    #Affichage du texte de défaite
    text = END_FONT.render("GAME OVER", 1, "white") # définition du texte de défaite
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2)) # On affiche le texte de défaite au milieu de la fenêtre
    pygame.display.update() # on actualise l'affichage de la fenêtre
    pygame.time.delay(5000) # On met le jeu en pause 5 secs avant de redémarrer

#-----Gestion de la victoire-----
def draw_win():
    pygame.mixer.music.stop() # On stop la musique
    WINNER.play() # On joue le son de la victoire
    #Affichage du texte de victoire
    text = END_FONT.render("YOU WIN", 1, "white") # définition du texte de victoire 
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2)) # On affiche le texte de victoire au milieu de la fenêtre
    pygame.display.update() # on actualise l'affichage de la fenêtre
    pygame.time.delay(5000) # On met le jeu en pause 5 secs avant de redémarrer

#------Fonction Principale du jeu---------- 
def main():
    pygame.mixer.music.play(-1) # On lance la musique, elle se répète à l'infinie
    clock = pygame.time.Clock() # Variable horloge
    score = 0 # Score initialisé à 0
    lives = 3 # Nombre de vies initialisés à 3
    run = True # Booléen de la boucle while qui fait tourner le jeu
    power_up = False # On initialise l'état du power up à faux
    invincible = False # On initialise l'état invincible de pac man à faux
    
    # Création des matrices carte et carte de collision à partir d'un fichier texte qui contient la carte
    with open(os.path.dirname(os.path.abspath(__file__)) +'\Assets\PacManMap.txt', 'r') as file: # Ouverture du fichier texte avec le nom 'file'
        liste = list(file) # On convertit le texte en un liste
        print (liste)
        map=[] # Matrice carte initialisé
        hitmap =[] # Matrice carte de collision initialisé
        for line in liste: # Pour chaque chaîne de caractère dans la liste (correspondant à une ligne)
            l=[] # Liste qui contiendra un ligne pour la matrice carte
            hit_l=[] # Liste qui contiendra un ligne pour la matrice carte de collision
            for value in line.split(','): # On sépare chaque élément d'une chaîne de caractère 
                if value != '\n': # On ne traitera la les '\n' du fichier texte
                    l.append(value) # On récupère chaque caractère et on le stock dans la ligne correspondante dans la matrice carte
                    # Pour la matrice 'carte de collision'
                    if value == '#':
                        hit_l.append('#') # On récupère les murs
                    elif value == ':':   
                        hit_l.append(':') # On récupère le mur franchissable par les fantômes mais pas par pac man
                    elif value == ';':
                        hit_l.append(';') # On récupère les murs spéciaux, invisibles, qui sont dans le spawn des fantômes (pour éviter les mouvements latéraux au spawn)
                    else:
                        hit_l.append(0) # Tout le rest sera stocker comme '0'
            map.append(l) # On stocke la ligne dans la matrice carte
            hitmap.append(hit_l) # On stocke la ligne dans la matrice carte de collision
  
    # Initialisation des hitboxs
    for i, row in enumerate(hitmap):
        for j, value in enumerate(row): # On prend chaque caractères stockés dans la matrice carte de collision
            if value == '#' or value == ':' or value == ';': # On leur donne un rectangle de collisions si se sont des murs (ou murs spéciaux)
                hitmap[i][j]=(pygame.Rect(j*SIZE, i*SIZE, SIZE, SIZE))
            else: # Sinon on leur donne un rectangle de collision nul
                hitmap[i][j]=(pygame.Rect(0, 0, 0, 0))
    pac_man = pygame.Rect(9*SIZE, 16*SIZE, SIZE+4, SIZE+4) # Rectangle de collision de pac man à sa position initiale
    # Rectangle de collision des fantômes à leur position initiale
    ghost_1 = pygame.Rect(9*SIZE, 10*SIZE, SIZE, SIZE)
    ghost_2 = pygame.Rect(9*SIZE, 10*SIZE, SIZE, SIZE)
    ghost_3 = pygame.Rect(9*SIZE, 10*SIZE, SIZE, SIZE)

    # Importation des variables globals (pour les remettre à zéro si nécessaire)
    global ghost_1_move
    global ghost_1_want_to_move
    global ghost_2_move
    global ghost_2_want_to_move
    global ghost_3_move
    global ghost_3_want_to_move
    global move
    global want_to_move


    while run:
        clock.tick(FPS) #La fenêtre tourne à 60 images par secondes

        # Gestion des évènements
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quitter la fenêtre en appuyant sur la croix
                pygame.quit() 
                break

            if event.type == LIFE and invincible != True: # Si on entre en collision avec un fantôme et que pac man n'est pas invincible
                lives -= 1 # On perd une vie
                invincible = True # On devient invincible
                pygame.time.set_timer(INVINCIBLE, 3000) # Timer d'invincibilité pour 3 secondes
                # Pac man est réinitialisé à sa position d'origine, immobile 
                pac_man.x = 9*SIZE
                pac_man.y = 16*SIZE
                want_to_move = [False, False, False, False]
                move = -2
                
            if event.type == INVINCIBLE: # Quand le timer d'invincibilité est déclenché
                pygame.time.set_timer(INVINCIBLE, 0) # On le supprime
                invincible = False # Pac man n'est plus invincible

            if event.type == POWER_UP: # Quand pac man consomme un power up
                power_up = True # Pac man peut manger les fantômes
                pygame.time.set_timer(POWER_UP_END, 8000) # Timer de power up pour 8 secondes  

            if event.type == POWER_UP_END: #Quand le timer power up est déclenché 
                power_up = False # Pac man ne peut plus mangé les fantômes
                pygame.time.set_timer(POWER_UP_END, 0) # Timer power up supprimé

            # Évènement fantôme mangé
            # Fantôme 1 renvoyé à son spawn prêt à repartir
            if event.type == EAT_GHOST_1: 
                ghost_1_want_to_move = [False, False, False, False]
                ghost_1_move = -2
                ghost_1.x = 9*SIZE
                ghost_1.y = 10*SIZE

            # Fantôme 2 renvoyé à son spawn prêt à repartir
            if event.type == EAT_GHOST_2:
                ghost_2_want_to_move = [False, False, False, False]
                ghost_2_move = -2
                ghost_2.x = 9*SIZE
                ghost_2.y = 10*SIZE

            # Fantôme 3 renvoyé à son spawn prêt à repartir 
            if event.type == EAT_GHOST_3:
                ghost_3_want_to_move = [False, False, False, False]
                ghost_3_move = -2
                ghost_3.x = 9*SIZE
                ghost_3.y = 10*SIZE
            
            if event.type == SCORE : # Événement nourriture mangé
                score += 1 # Score incrémenté

        keys_pressed = pygame.key.get_pressed() #Vérification de quelles touches sont appuyées

        draw_window(map, pac_man, score, ghost_1, ghost_2, ghost_3, lives, power_up) # Appelle fonction affichage

        # Appelle des fonctions de déplacement de pac man et des fantômes, sous forme de "thread", pour qu'ils soient exécutés en parallèle, pour gagner en temps d'execution (non nécessaire mais j'avais envi de tester)
        p1 = t.Thread(target=ghost_1_movement(ghost_1, hitmap, map))
        p2 = t.Thread(target=ghost_2_movement(ghost_2, hitmap, map))
        p3 = t.Thread(target=ghost_3_movement(ghost_3, hitmap, map))
        p4 = t.Thread(target=movement(keys_pressed, pac_man, hitmap))
       
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        
        map_interaction(map, pac_man) # Appelle fonction des interactions entre pac man et la carte
        got_catched(pac_man, ghost_1, ghost_2, ghost_3, power_up) # Appelle fonction de collision entre pac man et les fantômes
        
        if score == 152: # Si pac man à mangé toute la nourriture 
            draw_win() # Appelle fonction affichage de victoire
            run = False  # On stop la boucle du jeu
        if lives == 0: # Si on a perdu toutes nos vies
            draw_lose() # Appelle fonction affichage de défaite
            run = False # On stop la boucle du jeu

# Appelle fonction du jeu, le jeu se relance à l'infini (appuie sur croix pour quitter)
while True:
    main()
        
