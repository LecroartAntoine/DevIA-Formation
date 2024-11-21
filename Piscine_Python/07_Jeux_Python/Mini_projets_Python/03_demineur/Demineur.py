import pygame
import random
import os
from queue import Queue
pygame.init()

WIDTH, HEIGHT = 600, 600 #Taille de la fenetre

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #On définit la fenetre
pygame.display.set_caption("Démineur") #Nom de la fenetre

FPS = 60 #Nombre images par secondes

#Sons et musique
pygame.mixer.init() 
MUSIC = pygame.mixer.music.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Music.mp3')
BOOM = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Boom.wav')
GAMEOVER_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Game Over.mp3')
YOU_WIN = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\You Win.mp3')
YOU_WIN_2 = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\You Win2.wav')


# Valeur des différentes couleurs
RECT_COLOR = (200, 200, 200)
CLICKED_RECT_COLOR = (140, 140, 140)
FLAG_RECT_COLOR = (255, 0, 0)
MINE_RECT_COLOR = (0, 0, 0)

#Nombre de ligne, colonnes, mines
ROWS = 15
COLS = 15
MINES = 30

SIZE = WIDTH / ROWS #Taille d'une case

# Différentes polices de texte
END_FONT = pygame.font.SysFont("Impact", 100)
NUM_FONT = pygame.font.SysFont("Impact", 20)
NUM_COLOR = {1: "blue", 2: "green", 3: "red"}

def draw_window(field, cover_field): #Affichage fenetre
    for i, row in enumerate(field): #On sépare le champ de mine en ses différentes lignes
        y = SIZE * i # la position y vaut l'indice de la ligne + taille de i cases
        for j, value in enumerate(row): #On sépare chaque emplacement dans une ligne, value étant la valeur de la case
            x = SIZE * j # la position x vaut l'indice de la colonne dans la ligne + taille de i cases
            is_covered = cover_field[i][j] == 0 #Booléen Vrai si la case est recouverte
            is_flag = cover_field[i][j] == -1 #Booléen Vrai si la case est recouverte par un drapeau
            is_mine = value == -1 #Booléen vrai si la case contient une bombe
            
            #On colorie la case en rouge si c'est un drapeau
            if is_flag:
                pygame.draw.rect(WIN, FLAG_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(WIN, "black", (x, y, SIZE, SIZE), 2)
                continue

            #On colorie la case en gris clair si elle est recouverte
            if is_covered:
                pygame.draw.rect(WIN, RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(WIN, "black", (x, y, SIZE, SIZE), 2)
                continue
            #Sinon elle est découverte, on la colorie en gris foncé
            else:
                pygame.draw.rect(WIN, CLICKED_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(WIN, "black", (x, y, SIZE, SIZE), 2)
                #Si la case et découverte et que c'est une mine, on affiche un rond noir
                if is_mine:
                    pygame.draw.circle(WIN, MINE_RECT_COLOR, (x+ SIZE/2, y+SIZE/2), SIZE/2-5)
                    pygame.draw.rect(WIN, "black", (x, y, SIZE, SIZE), 2)
                    continue
                #Si la case est découverte et qu'elle a au moins 1 mine autour d'elle, on affiche le nombre de voisins d'une certaines couleur
                elif value > 0 and value < 4:
                    text = NUM_FONT.render(str(value), 1, NUM_COLOR[value])
                    WIN.blit(text, (x + (SIZE/2 - text.get_width()/2), y + (SIZE/2 - text.get_height()/2)))
                elif value >= 4:# au dela de 4 voisins, on affiche en noir
                    text = NUM_FONT.render(str(value), 1, "black")
                    WIN.blit(text, (x + (SIZE/2 - text.get_width()/2), y + (SIZE/2 - text.get_height()/2)))
    pygame.display.update()#On actualise l'écran

#----Fonction qui créer une liste des positions des cases environnantes, en s'assurant qu'elles existent-----------
def get_neighbors(r, c):#Reçoit numéro de ligne et colonne
    neighbors = []

    #Gauche et droite
    if r > 0:
        neighbors.append((r - 1, c))
    if r < ROWS - 1:
        neighbors.append((r + 1, c))

    #Haut et bas
    if c > 0:
        neighbors.append((r, c - 1))
    if c < COLS -1:
        neighbors.append((r, c + 1))

    #Diagonales
    if r > 0 and c > 0:
        neighbors.append((r - 1, c - 1))
    if r < ROWS - 1 and  c < COLS - 1:
        neighbors.append((r + 1, c + 1))
    if r < ROWS - 1 and c > 0:
        neighbors.append((r + 1, c - 1 ))
    if r > 0 and c < COLS - 1:
        neighbors.append((r - 1, c +1))

    return(neighbors) #Renvoie la liste des cases voisines

#--------Création champ de mine--------
def create_mine_field():
    field = [[0 for _ in range(COLS)] for _ in range(ROWS)]#Matrice champ de mine initialisé à 0
    mine_positions = [] #liste des positions de mines

    while len(mine_positions) < MINES:#Tant que la liste de mines créer est inférieur au nombre de mines souhaitées
        #On génère une coordonnée aléatoire, stocké dans un tuple
        r = random.randint(0, ROWS-1)
        c = random.randint(0, COLS-1)
        position = (r, c)

        if position in mine_positions:#Si la position existe déjà, on recommence
            continue

        mine_positions.append(position)#On ajoute la position à la liste des mines
        field[r][c] = -1 #On inscrit -1, dans le champ de mine, à cette position

    #Pour chaque mine, on appelle la fonction get_neighbors pour récupérer les positions des cases voisines
    for mine in mine_positions:
        neighbors = get_neighbors(mine[0], mine[1])
        for r, c in neighbors:
            if field[r][c] != -1: #Si le voisin n'est pas une bombe
                field[r][c] += 1 #On l'incrémente de 1 (conséquence, on saura combien de bombes autour de ce voisin)
    return(field)#On renvoie le champ de mine crée

#------Gestion de la souris-----------
def get_grid_pos(mouse_pos):
    mx, my = mouse_pos #On récupère la position x, y de la souris
    #On en déduit sur quelle case on est
    r = int(my / SIZE)
    c = int(mx / SIZE)
    return(r, c)#On renvoie la position de la case

#-------Gestion révélation de cases------------- 
def uncover_from_pos(r, c, cover_field, field):#On reçoit la position de la case qui vient d'être découvert, le champ de couverture et le champ de mine
    q = Queue() #On utilise la fonction queue pour créer une liste de cases. on regardera les voisins de cette case
    q.put((r, c))#On ajoute la position de la case qui vient d'être révélé
    done = [] #Liste des cases déjà révélés 

    while not q.empty(): #Tant que la queue n'est pas vide
        current = q.get() #On récupère la case en tête de la queue
        neighbors = get_neighbors(current[0], current[1]) #On récupère les voisins de cette case
        for x, y in neighbors:
            if (x, y) in done:# Si la case est déjà révélé, on passe à la suivante
                continue
            value = field[x][y]#On récupère la valeur associé à cette case
            if value == 0 and cover_field[x][y] != -1:#Si la case ne contient pas de mine et n'en a pas dans son voisinage (valeur 0) et si la case n'est pas un drapeau
                q.put((x, y)) #On l'ajoute à la queue
            if value != -1: #Si la case n'est pas un drapeau
                cover_field[x][y] = 1 #On la découvre
            done.append((x, y))#On ajoute la case aux cases traitées

#-----Gestion de la défaite-----
def draw_lose(field):#On reçoit le champ de mines
    #Gestion Sons: on arête la musique et on joue les sons de victoire
    pygame.mixer.music.stop()
    GAMEOVER_SOUND.play()
    #On révèle toutes les mines
    for i, row in enumerate(field):
        y = SIZE * i
        for j, value in enumerate(row):
            x = SIZE * j
            if value == -1:
                pygame.draw.rect(WIN, CLICKED_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.circle(WIN, MINE_RECT_COLOR, (x+ SIZE/2, y+SIZE/2), SIZE/2-5)
                pygame.draw.rect(WIN, "black", (x, y, SIZE, SIZE), 2)
    #Affichage du texte de défaite
    text = END_FONT.render("GAME OVER", 1, "white")
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)#On met le jeu en pause 5 secs avant de redémarrer

#-----Gestion de la victoire---------
def draw_win():
    #Gestion Sons: on arête la musique et on joue les sons de victoire
    pygame.mixer.music.stop()
    YOU_WIN.play()
    YOU_WIN_2.play()
    #Affichage du texte de victoire
    text = END_FONT.render("YOU WIN", 1, "white")
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)#On met le jeu en pause 5 secs avant de redémarrer

#----------Fonction principale du jeu------------
def main():
    clock = pygame.time.Clock() #variable horloge
    lost = False #Perdu initié à faux
    field = create_mine_field() #On crée une matrice champ de mines
    cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)] # On crée une deuxième matrice initié à 0 pour recouvrir la première
    count_covered = 0 #Compteur cases couvertes (pour déterminer si gagné)
    pygame.mixer.music.play(-1) #On lance la musique, elle se répète à l'infinie

    while True:

        clock.tick(FPS) #La fenêtre tourne à 60 images par secondes

        #---Gestion des événements-----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#Quitter la fenetre en appuyant sur la croix
                pygame.quit() 
                break
            #Gestion de la souris
            if event.type == pygame.MOUSEBUTTONDOWN: #Quand on appuie sur un boutton de la souris
                r, c = get_grid_pos(pygame.mouse.get_pos()) #On traduit la position de la souris en indice d'une case grâce à la fonction get_grid_pos
                if r >= ROWS or c >= COLS: #Si la souris est en dehors de la fenetre, on recommence
                    continue
                mouse_pressed = pygame.mouse.get_pressed()#On récupère le button de souris pressé
                if mouse_pressed[0] and cover_field[r][c] != -1: #Si clique gauche sur autre chose qu'un drapeau
                    cover_field[r][c] = 1 #On révèle la case

                    if field[r][c] == -1:# Si la case est une mine
                        BOOM.play()
                        lost = True #On a perdu

                
                    if field[r][c] == 0: #Si la case n'a pas de bombes autour d'elle
                        uncover_from_pos(r, c, cover_field, field) #On determine toutes les autres cases à révélé (on révèle toutes les cases jusqu'à tomber sur une case qui à une (ou plus) mine(s) autour d'elle)

                    #On compte toutes les cases encore couverte (pour determiner si gagné au non)
                    count_covered = 0
                    for i in range (0, COLS):
                        for j in range (0, ROWS):
                            if cover_field[i][j] != 1:
                                count_covered += 1

                elif mouse_pressed[2]:#Bouton droite souris, ajoute un drapeau
                    if cover_field[r][c] == -1:#Si on ajoute un drapeau sur un autre, la case redevient sans drapeau
                        cover_field[r][c] = 0
                    else:
                        cover_field[r][c] = -1#Sinon on ajoute un drapeau
    
        draw_window(field, cover_field)#Affichage

        if count_covered == MINES and not lost:#Si les cases encore couvertes sont égales au nombre de mines: c'est gagné
            draw_win()
            break
           

        if lost:#On a cliqué sur une mine: c'est perdu
            draw_lose(field)
            break

     
    
while True:#On fait tourner la fonction principale en boucle tant qu'on a pas appuyé sur la croix
    main()