import pygame
import os
import random
from functools import reduce
import threading as t
from math import floor

#Définition de la taille de la fenetre
WIDTH,HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Casse brique") # On nomme la fenetr

FPS = 60 # Constante nombre d'images par seconde

#Police d'écriture et couleur des textes (score, vies, message victoire)
pygame.font.init() 
FONT = pygame.font.SysFont('Impact', 40)
WINNER_FONT = pygame.font.SysFont('Impact', 150)
MENU_FONT = pygame.font.SysFont("Impact", 50)
WHITE = (255, 255, 255)

#Définition des Sons et musiques
pygame.mixer.init() 
MUSIC = pygame.mixer.music.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Music.wav')
PLATFORM_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Bounce2.wav')
BORDER_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Bounce1.wav')
BRICK_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Brick Break.wav')
LIVELOSS_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Live Loss.wav')
GAMEOVER_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Game Over.mp3')
YOU_WIN = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\You Win.mp3')
YOU_WIN_2 = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\You Win2.wav')

PLATFORM_SPEED, SPHERE_SPEED = 10, 8 # Constante vitesse de mouvement de la platforme & de la balle

WIDTH_SPHERE, HEIGHT_SPHERE = 12, 12

WIDTH_BRICK, HEIGHT_BRICK = 50, 20 # Taille des briques

WIDTH_PLATFORM, HEIGHT_PLATFORM = 90, 20 # Taille de la platforme

# Définition des évènements

LIVES = pygame.USEREVENT + 2 # Vie Perdue
GT_POWER = pygame.USEREVENT + 3 # La balle traverse les briques
GT_POWER_END = pygame.USEREVENT + 4 # La balle ne traverse plus les briques
M_POWER = pygame.USEREVENT + 5 # La balle colle à la platforme
M_POWER_END = pygame.USEREVENT + 6 # La balle ne colle plus à la platforme
SD_POWER = pygame.USEREVENT + 7 # Vitesse de la balle diminuée
SD_POWER_END = pygame.USEREVENT + 8 # Vitesse de la balle normal
SU_POWER = pygame.USEREVENT + 9 # Vitesse de la balle augmentée
SU_POWER_END = pygame.USEREVENT + 10 # Vitesse de la balle normal
TRI_POWER = pygame.USEREVENT + 11
EXTEND_POWER = pygame.USEREVENT + 12
EXTEND_POWER_END = pygame.USEREVENT + 13
REDUCE_POWER = pygame.USEREVENT + 14
REDUCE_POWER_END = pygame.USEREVENT + 15

# Importation des images
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Fond.jpeg'), (WIDTH,HEIGHT)) # Image d'arrière plan

# Images de briques et power up + redimension
BRICK_BLUE = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Brique_bleu.png'), (WIDTH_BRICK, HEIGHT_BRICK))
BRICK_GRAY = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Brique_grise.png'), (WIDTH_BRICK, HEIGHT_BRICK))
BRICK_YELLOW = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Brique_jaune.png'), (WIDTH_BRICK, HEIGHT_BRICK))
BRICK_RED = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Brique_rouge.png'), (WIDTH_BRICK, HEIGHT_BRICK))
BRICK_GREEN = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Brique_verte.png'), (WIDTH_BRICK, HEIGHT_BRICK))
BRICK_PURPLE = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Brique_violette.png'), (WIDTH_BRICK, HEIGHT_BRICK))
BRICK_DMG = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Brique_dmg.png'), (WIDTH_BRICK, HEIGHT_BRICK))
GT_POWER_UP = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\GT power up.png'), (WIDTH_PLATFORM, HEIGHT_PLATFORM))
M_POWER_UP = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\M power up.png'), (WIDTH_PLATFORM, HEIGHT_PLATFORM))
SD_POWER_UP = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\SD power up.png'), (WIDTH_PLATFORM, HEIGHT_PLATFORM))
SU_POWER_UP = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\SU power up.png'), (WIDTH_PLATFORM, HEIGHT_PLATFORM))
TRI_POWER_UP = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\TRI power up.png'), (WIDTH_PLATFORM, HEIGHT_PLATFORM))
EXTEND_POWER_UP = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\EXT power up.png'), (WIDTH_PLATFORM, HEIGHT_PLATFORM))
REDUCE_POWER_UP = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\RED power up.png'), (WIDTH_PLATFORM, HEIGHT_PLATFORM))

ALL_POWER_UP = [M_POWER_UP, GT_POWER_UP, SD_POWER_UP, SU_POWER_UP, TRI_POWER_UP, EXTEND_POWER_UP, REDUCE_POWER_UP]
COLOR = [BRICK_BLUE, BRICK_RED, BRICK_GREEN, BRICK_PURPLE, BRICK_YELLOW, BRICK_GRAY, BRICK_DMG]# Liste avec toutes les différentes couleurs de briques

PLATFORM_0 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Platform.png'), (90,20))
PLATFORM_1 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Platform1.png'), (90,20))
PLATFORM_2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Platform2.png'), (90,20))
PLATFORM = [PLATFORM_0, PLATFORM_1, PLATFORM_2]

SMALL_PLATFORM = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Small Platform.png'), (45,20))

BIG_PLATFORM_0 = pygame.transform.scale(PLATFORM_0, (180,20))
BIG_PLATFORM_1 = pygame.transform.scale(PLATFORM_1, (180,20))
BIG_PLATFORM_2 = pygame.transform.scale(PLATFORM_2, (180,20))
BIG_PLATFORM = [BIG_PLATFORM_0, BIG_PLATFORM_1, BIG_PLATFORM_2]


SPHERE = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\sphere.png'), (WIDTH_SPHERE + 6, HEIGHT_SPHERE + 6)) # Image de la balle + redimension

sprite_platform = 0

#---------Fonction qui gère les affichages---------
def draw_window(platform, spheres, brick, liveNumber, level, rect_power_up, power_up, power_up_active, lifes_brick):# On affichera la platforme, la balle, les bricks, le score, les vies et le level en cours

    global sprite_platform
    sprite_platform += 0.25

    WIN.blit(BACKGROUND, (0,0))#Affichage arrière-plan

    pygame.draw.rect(WIN,  "black", (0, 0, WIDTH, 45))

    #Affichage du level en cours
    levelText = FONT.render(f"Level: {level}", 1, WHITE)
    WIN.blit(levelText, (0, 0))

    for i in range (1, liveNumber+1):#Affichage des vies
        WIN.blit(SPHERE, (WIDTH-40*i, 15))

    for i in range (len(ALL_POWER_UP)):
        if power_up_active[i]:
            WIN.blit(ALL_POWER_UP[i], (225 + WIDTH_PLATFORM * i, 15))

    if not power_up_active[5] and not power_up_active[6]:
        WIN.blit(PLATFORM[floor(sprite_platform % 3)], (platform.x, platform.y))
    elif power_up_active[5]:
        WIN.blit(BIG_PLATFORM[floor(sprite_platform % 3)], (platform.x, platform.y))
    elif power_up_active[6]:
        WIN.blit(SMALL_PLATFORM, (platform.x, platform.y))

    for sphere in spheres:
        WIN.blit(SPHERE, (sphere.x - (16 - WIDTH_SPHERE), sphere.y - (16 - HEIGHT_SPHERE)))#Affichage balle

    #Affichage des briques
    for i, b in enumerate(brick):
        ligne = (b.y -100)// HEIGHT_BRICK

        if ligne == 5 and lifes_brick[i] == 1:
            WIN.blit(COLOR[ligne], (b.x, b.y))
        elif ligne == 5 and lifes_brick[i] == 0:
            WIN.blit(COLOR[ligne + 1], (b.x, b.y))
        else:
            WIN.blit(COLOR[ligne], (b.x, b.y))

    for i, power in enumerate(power_up):
        WIN.blit(ALL_POWER_UP[power], (rect_power_up[i].x, rect_power_up[i].y))
            
    pygame.display.flip()# Actualisation de l'écran

#------Gestion des mouvements de la platforme----------
def platform_movement(keys_pressed, platform):
    if keys_pressed[pygame.K_LEFT] and platform.x > 0: # Aller à gauche
        platform.x -= PLATFORM_SPEED
      
    if keys_pressed[pygame.K_RIGHT]and platform.x < WIDTH-90: # Aller à droite
        platform.x += PLATFORM_SPEED

#--------Fonction qui gère les collisions entre la balle et les bordures---------
def sphere_border_collision(spheres, sphereMove, platform, border, power_up_active):
    for i, sphere in enumerate(spheres):
        if sphere.colliderect(border[0]): # Bordure haut
            sphere.y += 1 # On déplace la balle hors de portée de la bordure
            sphereMove[i][1] *= -1 # La balle part en sens inverse
            BORDER_SOUND.play() # Joue le son de collision avec la bordure
            
        if sphere.colliderect(border[1]): # Bordure gauche
            sphere.x += 1
            sphereMove[i][2] *= -1
            BORDER_SOUND.play()
            
        if sphere.colliderect(border[2]): # Bordure droite
            sphere.x -= 1
            sphereMove[i][2] *= -1
            BORDER_SOUND.play()

        if sphere.colliderect(border[3]): # Bordure en bas = vie perdu
            if len(spheres) == 1:
                LIVELOSS_SOUND.play() # Joue le son de perte de vie
                pygame.event.post(pygame.event.Event(LIVES)) # Déclenchement évènement perte de vie
                power_up_active[4] = False
                sphere.x = platform.x + WIDTH_PLATFORM // 2 - WIDTH_SPHERE // 2
                sphere.y = platform.y - HEIGHT_SPHERE
                sphereMove[i][0] = False
                sphereMove[i][1] = -1
                sphereMove[i][2] = 0
            else:
                spheres.remove(sphere)
                sphereMove.remove(sphereMove[i])

#--------Fonction qui gère les collisions avec les briques-----------
def sphere_brick_collision(brick, spheres, sphereMove, rect_power_up, power_up, power_up_active, lifes_brick):
    for i, sphere in enumerate(spheres):
        b = sphere.collidelist(brick)
        if b > -1: # Si la sphère est en contact avec une brique
            if power_up_active[1]:
                chance = random.randrange(0,10)
            else:
                chance = random.randrange(0,4)

            if chance == 0 and len(rect_power_up) <= 2:
                rect_power_up.append(pygame.Rect(brick[b].x, brick[b].y, WIDTH_PLATFORM, HEIGHT_PLATFORM))
                power_up.append(random.randrange(0, len(ALL_POWER_UP)))
            
            if not power_up_active[1]:
                if abs(brick[b].left - sphere.right) < WIDTH_SPHERE:
                    sphereMove[i][2] = abs(sphereMove[i][2]) * -1
                if abs(brick[b].right - sphere.left) < WIDTH_SPHERE:
                    sphereMove[i][2] = abs(sphereMove[i][2])
                if abs(brick[b].top - sphere.bottom) < WIDTH_SPHERE:
                    sphereMove[i][1] = abs(sphereMove[i][1]) * -1
                if abs(brick[b].bottom - sphere.top) < WIDTH_SPHERE:
                    sphereMove[i][1] = abs(sphereMove[i][1])

            BRICK_SOUND.play() # Son de cassage d'une brique

            if lifes_brick[b] == 0:
                brick.pop(b)
                lifes_brick.pop(b)

            elif power_up_active[1]:
                brick.pop(b)
                lifes_brick.pop(b)

            else:
                lifes_brick[b] -= 1


#--------Fonction qui gère les collisions avec la platforme-----------
def sphere_platform_collision(spheres, platform, sphereMove, power_up_active):
    
    for i, sphere in enumerate(spheres):
        if sphere.colliderect(platform): # Si la balle touche la platforme
            if sphereMove[i][0]: # Si la balle est en mouvement, on joue le son en cas de collision avec la platforme (evite spam son and balle immobile au début)
                PLATFORM_SOUND.play()
                if power_up_active[0] and i == 0:
                    sphereMove[i][0] = False
                    sphere.y = HEIGHT - 50 - HEIGHT_SPHERE
        
            # En fonction d'où atterrit le milieu de la balle, vitesse latéral et verticale proportionnée (9 cas possibles)
            if sphere.x + WIDTH_SPHERE // 2 >= platform.x and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 1:
                sphereMove[i][1] = -0.35
                sphereMove[i][2] = -0.65
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 1 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 2:
                sphereMove[i][1] = -0.45
                sphereMove[i][2] = -0.55
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 2 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 3:
                sphereMove[i][1] = -0.5
                sphereMove[i][2] = -0.5
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 3 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 4:
                sphereMove[i][1] = -0.55
                sphereMove[i][2] = -0.45
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 4 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 5:
                sphereMove[i][1] = -0.6
                sphereMove[i][2] = -0.4
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 5 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 6:
                sphereMove[i][1] = -0.7
                sphereMove[i][2] = -0.3
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 6 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 7:
                sphereMove[i][1] = -0.8
                sphereMove[i][2] = -0.2
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 7 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 8:
                sphereMove[i][1] = -0.9
                sphereMove[i][2] = -0.1

            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 8 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 10:
                sphereMove[i][1] *= -1

            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 10 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 11:
                sphereMove[i][1] = -0.9
                sphereMove[i][2] = 0.1
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 11 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 12:
                sphereMove[i][1] = -0.8
                sphereMove[i][2] = 0.2
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 12 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 13:
                sphereMove[i][1] = -0.7
                sphereMove[i][2] = 0.3
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 13 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 14:
                sphereMove[i][1] = -0.6
                sphereMove[i][2] = 0.4
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 14 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 15:
                sphereMove[i][1] = -0.55
                sphereMove[i][2] = 0.45
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 15 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 16:
                sphereMove[i][1] = -0.5
                sphereMove[i][2] = 0.5
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 16 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 17:
                sphereMove[i][1] = -0.45
                sphereMove[i][2] = 0.55
            elif sphere.x + WIDTH_SPHERE // 2 >= platform.x + (platform.w / 18) * 17 and sphere.x + WIDTH_SPHERE // 2 < platform.x + (platform.w / 18) * 18:
                sphereMove[i][1] = -0.35
                sphereMove[i][2] = 0.65

#---------Gestion des movements de la balle------------
def sphere_movement(keys_pressed, spheres, platform, sphereMove, position, power_up_active):

    for i, sphere in enumerate(spheres):
        if sphereMove[i][0] and not power_up_active[2] and not power_up_active[3]: #Fait bouger la sphère sur x et y
            sphere.y += sphereMove[i][1]*SPHERE_SPEED
            sphere.x += sphereMove[i][2]*SPHERE_SPEED
        if sphereMove[i][0] and power_up_active[2]: #Fait bouger la sphère sur x et y
            sphere.y += sphereMove[i][1]*(SPHERE_SPEED - 2)
            sphere.x += sphereMove[i][2]*(SPHERE_SPEED - 2)
        if sphereMove[i][0] and power_up_active[3]: #Fait bouger la sphère sur x et y
            sphere.y += sphereMove[i][1]*(SPHERE_SPEED + 2)
            sphere.x += sphereMove[i][2]*(SPHERE_SPEED + 2)

        # Gestion du déplacement de la balle quand immobile sur la platforme
        if not sphereMove[i][0]:
            sphere.x = platform.x + platform.w // 2 - sphere.w // 2

        # Si la balle est à l’arrêt, on appuie sur espace pour la faire partir
        if keys_pressed[pygame.K_SPACE] and not sphereMove[i][0]:
            sphereMove[i][0] = True
            sphereMove[i][1] = -1
            sphereMove[i][2] = 0

def power_up_movement(rect_power_up, power_up, platform):
    for i, rectangle in enumerate(rect_power_up):
        rectangle.y += 2
        if rectangle.colliderect(platform):
            if power_up[i] == 0:
                pygame.event.post(pygame.event.Event(M_POWER))
            if power_up[i] == 1:
                pygame.event.post(pygame.event.Event(GT_POWER))
            if power_up[i] == 2:
                pygame.event.post(pygame.event.Event(SD_POWER))
            if power_up[i] == 3:
                pygame.event.post(pygame.event.Event(SU_POWER))
            if power_up[i] == 4:
                pygame.event.post(pygame.event.Event(TRI_POWER))
            if power_up[i] == 5:
                pygame.event.post(pygame.event.Event(EXTEND_POWER))
            elif power_up[i] == 6:
                pygame.event.post(pygame.event.Event(REDUCE_POWER))

            rect_power_up.remove(rect_power_up[i])
            power_up.remove(power_up[i])
        elif rectangle.y > HEIGHT:
            rect_power_up.remove(rect_power_up[i])
            power_up.remove(power_up[i])
        
#-----Si on a gagné, c'est à dire complété les 4 niveaux-------
def draw_win():
    # Gestion Sons: on arête la musique et on joue les sons de victoire
    pygame.mixer.music.stop()
    YOU_WIN.play()
    YOU_WIN_2.play()

    # Affichage du texte de victoire
    text = WINNER_FONT.render('You Win', 1, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    pygame.display.update() # On rafraîchit l’écran 
    pygame.time.delay(5000)# On affiche tout ca pendant 5 secondes avant le redémarrage du jeu

#-----Si on a perdu-----
def draw_loss():
    # Gestion Sons: on arête la musique et on joue les sons de défaite
    pygame.mixer.music.stop()
    GAMEOVER_SOUND.play()

    # Affichage du texte de défaite
    text = WINNER_FONT.render('GAME OVER', 1, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    pygame.display.update() # On rafraîchît l'écran
    pygame.time.delay(5000) # On affiche tout ca pendant 5 secondes avant le redémarrage du jeu

#--------Si on a complété un niveau
def draw_level_cleared(level):
    # Affichage du texte de niveau suivant
    text = WINNER_FONT.render(f'Level {level}', 1, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    pygame.display.update() # On rafraîchît l'écran
    pygame.time.delay(3000) # On affiche tout ca pendant 3 secondes avant le passage au niveau suivant

def main(level, unique_level):
    clock = pygame.time.Clock() #variable horloge
    number_of_bricks = 0 # Initialisation de la variable du nombre de briques à casser
    sphereMove = [[False, -1, 0]] # liste des propriétés de la sphère ([0] : en mouvement, [1] : direction sur l'axe y, [2] : direction sur l'axe x )
    liveNumber = 3 # Nombre de vies
    spheres = []
    power_up_active = [False, False, False, False, False, False, False]
    power_up = []
    rect_power_up = []

    #Déclaration des différentes Hitboxs 
    platform = pygame.Rect((WIDTH // 2) - 45, HEIGHT - 50, 90, 20) # Hitbox de la platforme
    spheres.append(pygame.Rect((WIDTH // 2) - WIDTH_SPHERE // 2, HEIGHT - 50 - HEIGHT_SPHERE, WIDTH_SPHERE, HEIGHT_SPHERE)) # Hitbox de la balle

    position =  spheres[0].x - platform.x

    # Hitbox des briques, crées à partir d'un fichier texte
    with open(os.path.dirname(os.path.abspath(__file__)) + f'\Assets\Level {level}.txt', 'r') as file: # On ouvre le fichier texte
        brick = [] # Matrice briques initialisé 

        for i, line in enumerate(file.read().split('\n')): # Pour chaque ligne de notre fichier texte
            l = [] # Ligne matrice initialisé

            for value in line: # Pour chaque caractère dans la ligne du texte
                l.append(value) # On l'ajoute à la ligne de notre matrice

            brick.append(l) # Quand on a parcouru la ligne de texte, on stock la ligne de matrice dans la matrice

    # On parcoure chaque emplacement dans notre matrice
    lifes_brick = [] 
    for i, row in enumerate(brick):
        for j, value in enumerate(row):

            if value == '1': # Si on trouve '1' à cet emplacement
                brick[i][j]=(pygame.Rect(j * WIDTH_BRICK, 100 + i * HEIGHT_BRICK, WIDTH_BRICK, HEIGHT_BRICK)) # On créer une hitbox de brique 
                number_of_bricks += 1 # Incrémentation du nombre de briques à casser

                if i == 5:
                    lifes_brick.append(1)
                else:
                    lifes_brick.append(0)

    brick = reduce(lambda x,y: x+y, brick)
    for i in range(brick.count('0')):
        brick.remove('0')

    #Définition des bordures, stocké dans une liste
    border = []
    borderTop = pygame.Rect(0, 40, WIDTH, 10)
    borderLeft = pygame.Rect(-10, 0, 10, HEIGHT)
    borderRight = pygame.Rect(WIDTH, 0, 10, HEIGHT)
    borderBottom = pygame.Rect(0, HEIGHT + 10, WIDTH, 10)
    border.extend([borderTop, borderLeft, borderRight, borderBottom])
    
    pygame.mixer.music.play(-1) #On lance la musique, elle se répète à l'infinie

    while True: # Boucle principale du jeu, se répète à l'infinie tant qu'on appuie pas sur la croix

        clock.tick(FPS) #La fenêtre tourne à 60 images par secondes

    #Définition des évènements
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:#"quitter le jeu": on quitte la boucle
                pygame.quit()
                break
            if event.type == LIVES:# Perte d'une vie sur bordure basse touchée
                liveNumber -=1
            if event.type == M_POWER:
                power_up_active[0] = True
                pygame.time.set_timer(M_POWER_END, 15000)
            if event.type == M_POWER_END:
                power_up_active[0] = False
                pygame.time.set_timer(M_POWER_END, 0)
            if event.type == GT_POWER:
                power_up_active[1] = True
                pygame.time.set_timer(GT_POWER_END, 15000)
            if event.type == GT_POWER_END:
                power_up_active[1] = False
                pygame.time.set_timer(GT_POWER_END, 0)
            if event.type == SD_POWER:
                power_up_active[2] = True
                pygame.event.post(pygame.event.Event(SU_POWER_END))
                pygame.time.set_timer(SD_POWER_END, 15000)
            if event.type == SD_POWER_END:
                power_up_active[2] = False
                pygame.time.set_timer(SD_POWER_END, 0)
            if event.type == SU_POWER:
                power_up_active[3] = True
                pygame.event.post(pygame.event.Event(SD_POWER_END))
                pygame.time.set_timer(SU_POWER_END, 15000)
            if event.type == SU_POWER_END:
                power_up_active[3] = False
                pygame.time.set_timer(SU_POWER_END, 0)
            if event.type == TRI_POWER:
                power_up_active[4] = True
                spheres.append(pygame.Rect(platform.x, HEIGHT - 50 - HEIGHT_SPHERE, WIDTH_SPHERE, HEIGHT_SPHERE))
                spheres.append(pygame.Rect(platform.x + WIDTH_PLATFORM - WIDTH_SPHERE, HEIGHT - 50 - HEIGHT_SPHERE, WIDTH_SPHERE, HEIGHT_SPHERE))
                sphereMove.append([True, -0.7, -0.3])
                sphereMove.append([True, -0.7, 0.3])
            if event.type == EXTEND_POWER:
                power_up_active[5] = True
                platform.w = 180
                pygame.event.post(pygame.event.Event(REDUCE_POWER_END))
                pygame.time.set_timer(EXTEND_POWER_END, 15000)
            if event.type == EXTEND_POWER_END:
                power_up_active[5] = False
                if not power_up_active[6]:
                    platform.w = 90
                pygame.time.set_timer(EXTEND_POWER_END, 0)
            if event.type == REDUCE_POWER:
                power_up_active[6] = True
                platform.w = 45
                pygame.event.post(pygame.event.Event(EXTEND_POWER_END))
                pygame.time.set_timer(REDUCE_POWER_END, 15000)
            if event.type == REDUCE_POWER_END:
                power_up_active[6] = False
                if not power_up_active[5]:
                    platform.w = 90
                pygame.time.set_timer(REDUCE_POWER_END, 0)

        if len(spheres) == 1:
            power_up_active[4] = 0

        keys_pressed = pygame.key.get_pressed() #Vérification de quelles touches sont appuyées
        
        p1 = t.Thread(target = sphere_border_collision(spheres, sphereMove, platform, border, power_up_active))
        p2 = t.Thread(target = sphere_platform_collision(spheres, platform, sphereMove, power_up_active))
        p3 = t.Thread(target = sphere_brick_collision(brick, spheres, sphereMove, rect_power_up, power_up, power_up_active, lifes_brick))
        p4 = t.Thread(target = power_up_movement(rect_power_up, power_up, platform))
        p5 = t.Thread(target = sphere_movement(keys_pressed, spheres, platform, sphereMove, position, power_up_active))
        p6 = t.Thread(target = platform_movement(keys_pressed, platform))
        p7 = t.Thread(target = draw_window(platform, spheres, brick, liveNumber, level, rect_power_up, power_up, power_up_active, lifes_brick))
      
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()

        if liveNumber <= 0: #Quand on n'a plus de vies
            draw_loss() #Appelle fonction perdu
            break #On quitte la boucle principale du jeu

        if len(brick) == 0:#Quand on a cassé toutes les briques 
            level += 1 # On passe au level suivant
            # Si on a fini tous les niveaux
            if level > 5 or unique_level:
                draw_win() #Appelle fonction gagné
                break #On quitte la boucle principale du jeu
            else:
                draw_level_cleared(level) # Appelle de la fonction qui affiche qu'on passe au level suivant
                # On réinitialise nos variables
                sphereMove = [[False, -1, 0]]
                liveNumber = 3 
                power_up_active = [False, False, False, False, False, False, False]
                power_up = []
                rect_power_up = []
                number_of_bricks = 0
                spheres = []
                spheres.append(pygame.Rect((WIDTH/2) - WIDTH_SPHERE // 2, HEIGHT - 50 - HEIGHT_SPHERE, WIDTH_SPHERE, HEIGHT_SPHERE))
                # On ouvre le fichier texte du nouveau niveau et on recréer les briques
                with open(os.path.dirname(os.path.abspath(__file__)) + f'\Assets\Level {level}.txt', 'r') as file: # On ouvre le fichier texte
                    brick = [] # Matrice briques initialisé 

                    for i, line in enumerate(file.read().split('\n')): # Pour chaque ligne de notre fichier texte
                        l = [] # Ligne matrice initialisé

                        for value in line: # Pour chaque caractère dans la ligne du texte
                            l.append(value) # On l'ajoute à la ligne de notre matrice

                        brick.append(l) # Quand on a parcouru la ligne de texte, on stock la ligne de matrice dans la matrice

                # On parcoure chaque emplacement dans notre matrice
                lifes_brick = [] 
                for i, row in enumerate(brick):
                    for j, value in enumerate(row):
                        
                        if value == '1': # Si on trouve '1' à cet emplacement
                            brick[i][j]=(pygame.Rect(j * WIDTH_BRICK, 100 + i * HEIGHT_BRICK, WIDTH_BRICK, HEIGHT_BRICK)) # On créer une hitbox de brique 
                            number_of_bricks += 1 # Incrémentation du nombre de briques à casser

                            if i == 5:
                                lifes_brick.append(1)
                            else:
                                lifes_brick.append(0)

                brick = reduce(lambda x,y: x+y, brick)
                for i in range(brick.count('0')):
                    brick.remove('0')

#----MENU-----

RECT_WIDTH, RECT_HEIGHT = 300, 60
MENU_COLOR = (22, 155, 155)

def draw_menu(outline_size, outline_size_level, level_select):
    WIN.blit(BACKGROUND, (0, 0))

    if not level_select:
        option_1 = MENU_FONT.render("Start", 1, "white")
        WIN.blit(option_1, (WIDTH/2 - option_1.get_width()/2, (HEIGHT//4) - option_1.get_height()/2))
        pygame.draw.rect(WIN, MENU_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size[0])

        option_2 = MENU_FONT.render("Level Select", 1, "white")
        WIN.blit(option_2, (WIDTH/2 - option_2.get_width()/2, (HEIGHT//4) * 2 - option_2.get_height()/2))
        pygame.draw.rect(WIN, MENU_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) * 2 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size[1])

        option_3 = MENU_FONT.render("Quit", 1, "white")
        WIN.blit(option_3, (WIDTH/2 - option_3.get_width()/2, (HEIGHT//4) * 3 - option_3.get_height()/2))
        pygame.draw.rect(WIN, MENU_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) * 3 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size[2])

    else:
        level_1 = MENU_FONT.render("Level 1", 1, "white")
        WIN.blit(level_1, (WIDTH/2 - level_1.get_width()/2, (HEIGHT//7) - level_1.get_height()/2))
        pygame.draw.rect(WIN, MENU_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//7) - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size_level[0])

        level_2 = MENU_FONT.render("Level 2", 1, "white")
        WIN.blit(level_2, (WIDTH/2 - level_2.get_width()/2, (HEIGHT//7) * 2 - level_2.get_height()/2))
        pygame.draw.rect(WIN, MENU_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//7) * 2 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size_level[1])

        level_3 = MENU_FONT.render("Level 3", 1, "white")
        WIN.blit(level_3, (WIDTH/2 - level_3.get_width()/2, (HEIGHT//7) * 3 - level_3.get_height()/2))
        pygame.draw.rect(WIN, MENU_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//7) * 3 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size_level[2])

        level_4 = MENU_FONT.render("Level 4", 1, "white") 
        WIN.blit(level_4, (WIDTH/2 - level_4.get_width()/2, (HEIGHT//7) * 4 - level_4.get_height()/2))
        pygame.draw.rect(WIN, MENU_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//7) * 4 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size_level[3])

        level_5 = MENU_FONT.render("Level 5", 1, "white")
        WIN.blit(level_5, (WIDTH/2 - level_5.get_width()/2, (HEIGHT//7) * 5 - level_5.get_height()/2))
        pygame.draw.rect(WIN, MENU_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//7) * 5 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size_level[4])

        back = MENU_FONT.render("Return", 1, "white")
        WIN.blit(back, (WIDTH/2 - back.get_width()/2, (HEIGHT//7) * 6 - back.get_height()/2))
        pygame.draw.rect(WIN, MENU_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//7) * 6 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size_level[5])

    pygame.display.update() 


def menu():
    clock = pygame.time.Clock()
    options_rect = []
    options_rect_level = []
    level_select = False
    outline_size = [2, 2, 2]
    outline_size_level = [2, 2, 2, 2, 2, 2]
    for i in range(1, 4):
        options_rect.append(pygame.Rect(WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) * i - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT))
    for i in range(1, 7):
        options_rect_level.append(pygame.Rect(WIDTH/2 - RECT_WIDTH/2, (HEIGHT//7) * i - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT))
    

    while True:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#Quitter la fenetre en appuyant sur la croix
                pygame.quit() 
        if event.type == pygame.MOUSEBUTTONDOWN: #Quand on appuie sur un boutton de la souris
            if mouse_x >= WIDTH or mouse_y >= HEIGHT: #Si la souris est en dehors de la fenetre, on recommence
               continue

            if options_rect[0].collidepoint(mouse_x, mouse_y) and not level_select:
                main(1, False)

            elif options_rect[1].collidepoint(mouse_x, mouse_y) and not level_select:
                level_select = True

            elif options_rect[2].collidepoint(mouse_x, mouse_y) and not level_select:
                pygame.quit()
                break


            elif options_rect_level[0].collidepoint(mouse_x, mouse_y) and level_select:
                main(1, True)
                
            elif options_rect_level[1].collidepoint(mouse_x, mouse_y) and level_select:
                main(2, True)

            elif options_rect_level[2].collidepoint(mouse_x, mouse_y) and level_select:
                main(3, True)

            elif options_rect_level[3].collidepoint(mouse_x, mouse_y) and level_select:
                main(4, True)

            elif options_rect_level[4].collidepoint(mouse_x, mouse_y) and level_select:
                main(5, True)

            elif options_rect_level[5].collidepoint(mouse_x, mouse_y) and level_select:
                level_select = False

            pygame.time.delay(100)
        
        for i in range(3):
            if options_rect[i].collidepoint(mouse_x, mouse_y):
                outline_size[i] = 5
            else:
                outline_size[i] = 2

        for i in range(6):
            if options_rect_level[i].collidepoint(mouse_x, mouse_y):
                outline_size_level[i] = 5
            else:
                outline_size_level[i] = 2

        draw_menu(outline_size, outline_size_level, level_select)

if __name__ == '__main__':
    while True:
        menu()
