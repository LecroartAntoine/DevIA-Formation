import pygame
import os
import random
from functools import reduce
import threading as t

#Définition de la taille de la fenetre
WIDTH,HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Space Invader") # On nomme la fenetre

#Police d'écriture et couleur des textes (score, message victoire)
pygame.font.init() 
FONT = pygame.font.SysFont('Impact', 40)
WINNER_FONT = pygame.font.SysFont('Impact', 150)
WHITE = (255, 255, 255)

#Définition des Sons et musiques
pygame.mixer.init() 
MUSIC = pygame.mixer.music.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Music.wav')
LASER_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\laser1.wav')
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\explosion.wav')
LIVELOSS_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Live Loss.wav')
YOU_LOSE = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\You lose.mp3')
YOU_WIN = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\You Win.mp3')
WINNER_MUSIC = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Winner music.wav')

FPS = 60 # Constante nombre d'images par seconde

#Constantes de vitesse
SPACESHIP_SPEED = 8
LASER_SPEED = 8
ALIEN_FIRE_SPEED = 1000

#Taille des aliens
WIDTH_ALIEN1 = 40
HEIGHT_ALIEN1 = 40
WIDTH_ALIEN2 = 50
HEIGHT_ALIEN2 = 50
WIDTH_ALIEN3 = 60
HEIGHT_ALIEN3 = 60

#Taille du vaisseau
WIDTH_SPACESHIP = 50
HEIGHT_SPACESHIP = 50

#Taille projectile
WIDTH_LASER = 20
HEIGHT_LASER = 40

#Taille des explosions
WIDTH_EXPLOSION = 100
HEIGHT_EXPLOSION = 100

# Définition des évènements
ALIEN_HIT = pygame.USEREVENT + 1 #Alien détruit
LIVES = pygame.USEREVENT + 2 #Vie Perdue
ALIEN_FIRE = pygame.USEREVENT + 3
INVASION = pygame.USEREVENT + 4

# Image d'arrière plan
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Fond.jpg'), (WIDTH, HEIGHT))

# Images des aliens + redimension
ALIEN_1 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Alien1.png'), (WIDTH_ALIEN1, HEIGHT_ALIEN1))
ALIEN_2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Alien2.png'), (WIDTH_ALIEN2, HEIGHT_ALIEN2))
ALIEN_3 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Alien3.png'), (WIDTH_ALIEN3, HEIGHT_ALIEN3))
LIST_ALIEN_WIDTH = [WIDTH_ALIEN1, WIDTH_ALIEN2, WIDTH_ALIEN3]
LIST_ALIEN_HEIGHT = [HEIGHT_ALIEN1, HEIGHT_ALIEN2, HEIGHT_ALIEN3]

ALIEN_LASER_1 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\LaserAlien1.png'), (WIDTH_ALIEN1, HEIGHT_ALIEN1))
ALIEN_LASER_2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\LaserAlien2.png'), (WIDTH_ALIEN2, HEIGHT_ALIEN2))
ALIEN_LASER_3 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\LaserAlien3.png'), (WIDTH_ALIEN3, HEIGHT_ALIEN3))


#Images des Explosions + redimension
E_1 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\E1.png'), (WIDTH_EXPLOSION, HEIGHT_EXPLOSION))
E_2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\E2.png'), (WIDTH_EXPLOSION, HEIGHT_EXPLOSION))
E_3 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\E3.png'), (WIDTH_EXPLOSION, HEIGHT_EXPLOSION))
E_4 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\E4.png'), (WIDTH_EXPLOSION, HEIGHT_EXPLOSION))
E_5 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\E5.png'), (WIDTH_EXPLOSION, HEIGHT_EXPLOSION))
E_6 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\E6.png'), (WIDTH_EXPLOSION, HEIGHT_EXPLOSION))
E_7 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\E7.png'), (WIDTH_EXPLOSION, HEIGHT_EXPLOSION))
E_8 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\E8.png'), (WIDTH_EXPLOSION, HEIGHT_EXPLOSION))
E_9 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\E9.png'), (WIDTH_EXPLOSION, HEIGHT_EXPLOSION))
LIST_EXPLOSION = [E_1, E_1, E_2, E_2, E_3, E_3, E_4, E_4, E_5, E_5, E_6, E_6, E_7, E_7, E_8, E_8, E_9, E_9]

# Image du vaisseau + redimension
SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Spaceship.png'), (WIDTH_SPACESHIP, HEIGHT_SPACESHIP))

# Image des laser + redimension
LASER = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Laser.png'), (WIDTH_LASER, HEIGHT_LASER))

reload_speed = 0
move_left = 0

#---------Fonction regroupant les affichages---------
def draw_window(liveNumber, score, space_ship, aliens, lasers, alien_lasers, explosions, level):# Cette fonction gère l'affichage
    WIN.blit(BACKGROUND, (0,0))#Affichage arrière-plan

    WIN.blit(SPACESHIP, (space_ship.x, space_ship.y))#Affichage du vaisseau

    #Affichage des Aliens
    for alien in aliens:
        if alien.w == 40:
            WIN.blit(ALIEN_1, (alien.x, alien.y))
        elif alien.w == 50:
            WIN.blit(ALIEN_2, (alien.x, alien.y))
        elif alien.w == 60:
            WIN.blit(ALIEN_3, (alien.x, alien.y))

    for laser in alien_lasers:
        if laser.w == 40:
            WIN.blit(ALIEN_LASER_1, (laser.x, laser.y))
        elif laser.w == 50:
            WIN.blit(ALIEN_LASER_2, (laser.x, laser.y))
        elif laser.w == 60:
            WIN.blit(ALIEN_LASER_3, (laser.x, laser.y))

    for laser in lasers:
        WIN.blit(LASER, (laser.x, laser.y))#Affichage du laser

    #Affichage des Explosions
    for explosion in explosions:
        WIN.blit(LIST_EXPLOSION[explosion[1]], (explosion[0][0] - 30, explosion[0][1] - 30))

    pygame.draw.rect(WIN,  "black", (0, 0, WIDTH, 45))

#Affichage texte score
    scoreText = FONT.render("Score: " + str(score), 1, WHITE)
    WIN.blit(scoreText, (0, 0))

    levelText = FONT.render(f"Level: {level}", 1, "white")
    WIN.blit(levelText, (WIDTH / 2 - levelText.get_width() / 2, 0))

    for i in range (1, liveNumber+1):#Affichage des vies
        WIN.blit(SPACESHIP, (WIDTH-WIDTH_SPACESHIP*i,0))

    pygame.display.update()# Actualisation de l'écran

#------Gestion des mouvements du vaisseau---------
def space_ship_movement(keys_pressed, space_ship):
    if keys_pressed[pygame.K_LEFT] and space_ship.x > 0: # Aller à gauche
        space_ship.x -= SPACESHIP_SPEED
    if keys_pressed[pygame.K_RIGHT]and space_ship.x < WIDTH-WIDTH_SPACESHIP: # Aller à droite
        space_ship.x += SPACESHIP_SPEED

#---------Gestion des projectiles------------
def collision_laser(aliens, lasers, explosions):
    border_up = pygame.Rect(0, 50, WIDTH, 1) #Bordure du haut de l'écran
    #Collision entre le laser du joueur et les ennemies 
    for alien in aliens: #Pour la première rangée d'aliens
        for laser in lasers:
            if alien.colliderect(laser): 
                explosions.append([[alien.x, alien.y], 0]) # On stocke les coordonnées de l'alien pour créer une explosion dessus
                pygame.event.post(pygame.event.Event(ALIEN_HIT)) #Evènement alien touché: score +1
                EXPLOSION_SOUND.play() #Son d'un ennemie détruit
                aliens.remove(alien) #Suppression de l'ennemi détruit
                lasers.remove(laser)  # Le laser du joueur est supprimé

            if border_up.colliderect(laser): #collision du laser avec la bordure
                lasers.remove(laser)  # Le laser du joueur est supprimé

def collision_alien_laser(space_ship, alien_lasers):
    border_bottom = pygame.Rect(0, HEIGHT, WIDTH, 1) #Bordure du bas de l'écran
    # Collision entre les laser des ennemies et le joueur
    for laser in alien_lasers:
        if laser.colliderect(space_ship):
            pygame.event.post(pygame.event.Event(LIVES))#Évènement perte d'une vie
            alien_lasers.remove(laser) #Suppression du laser ennemie
        if laser.colliderect(border_bottom):#Suppression du laser ennemie après avoir franchi la bordure inférieur
            alien_lasers.remove(laser)

def lasers_movements(lasers, alien_lasers):
    for laser in lasers:
        laser.y -= LASER_SPEED
        
    for laser in alien_lasers:
        if laser.w == 40:
            laser.y += 4
        elif laser.w == 50:
            laser.y += 6
        elif laser.w == 60:
            laser.y += 8

def manage_explosions(explosions):
#Gestion des explosions
    for explosion in explosions:
        explosion[1] += 1 #On change d'image à chaque frame
        if explosion[1] >= 18: #Quand on arrive à l'image finale, on stop l'explosion et on réinitialise
            explosions.remove(explosion)

def create_laser(lasers, keys_pressed, space_ship, level):
    global reload_speed
    if keys_pressed[pygame.K_SPACE] and len(lasers) < level:
        if reload_speed == 0:
            lasers.append(pygame.Rect(space_ship.x + WIDTH_SPACESHIP // 2 - WIDTH_LASER // 2, space_ship.y, WIDTH_LASER, HEIGHT_LASER))
            LASER_SOUND.play()
            reload_speed = 10
        else:
            reload_speed -= 1
    return(reload_speed)

def create_alien_laser(level, aliens, alien_lasers):
    number_of_lasers = 1 + level
    chosen = []
    for _ in range(number_of_lasers):
        chosen.append(random.choice(aliens))

    for choice in chosen:
        alien_lasers.append(pygame.Rect(choice.x, choice.y, choice.w, choice.h))

def aliens_movement(aliens, to_kill):
    global move_left
    border_left = pygame.Rect(0, 0, 1, HEIGHT) #Bordure gauche de l'écran
    border_right = pygame.Rect(WIDTH, 0, 1, HEIGHT) #Bordure droite de l'écran
   
    if len(aliens) <= ((to_kill // 4) * 3) and len(aliens) > (to_kill // 2):
        speed_up = 1
    elif len(aliens) <= (to_kill // 2) and len(aliens) > (to_kill // 4):
        speed_up = 2
    elif len(aliens) <= (to_kill // 4):
        speed_up = 3
    else:
        speed_up = 0

    if border_right.collidelist(aliens) > -1:
        move_left = True
        for alien in aliens:
            alien.y += 5 + speed_up
    elif border_left.collidelist(aliens) > -1:
        move_left = False
        for alien in aliens:
            alien.y += 5 + speed_up
        
    if move_left:
        for alien in aliens:
            alien.x -= 2 + speed_up
    elif not move_left: 
        for alien in aliens:
            alien.x += 2 + speed_up
    return(move_left)
    
#-----Si on a gagné-------
def draw_win():
    pygame.time.set_timer(ALIEN_FIRE, 0)
    #Gestion Sons: on arête la musique et on joue les sons de victoire
    pygame.mixer.music.stop()
    YOU_WIN.play()
    WINNER_MUSIC.play()
    #Affichage du texte de victoire
    text = WINNER_FONT.render('VICTOIRE', 1, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()

    pygame.time.wait(5000)#On affiche tout ca pendant 5 secondes avant le redémarrage du jeu

#-----Si on a perdu-----
def draw_loss():
    pygame.time.set_timer(ALIEN_FIRE, 0)
    #Gestion Sons: on arête la musique et on joue les sons de défaite
    pygame.mixer.music.stop()
    YOU_LOSE.play()
    #Affichage du texte de défaite
    text = WINNER_FONT.render('GAME OVER', 1, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.wait(5000)#On affiche tout ca pendant 5 secondes avant le redémarrage du jeu

def draw_level_cleared(level):
    pygame.time.set_timer(ALIEN_FIRE, 0)
    # Affichage du texte de niveau suivant
    text = WINNER_FONT.render(f'Level {level}', 1, "white")
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    pygame.display.update() # On rafraîchît l'écran

    pygame.time.delay(3000) # On affiche tout ca pendant 3 secondes avant le passage au niveau suivant

def main():
    clock = pygame.time.Clock() #variable horloge
    pygame.time.set_timer(ALIEN_FIRE, ALIEN_FIRE_SPEED) #Timer déclenchement d'un tir ennemie
    liveNumber = 3 # Nombre de vies
    score = 0 # On établit le score à 0
    lasers = [] #Laser du joueur mit à 0
    alien_lasers = [] #Liste des lasers ennemie
    level = 1
    explosions = []

    pygame.mixer.music.play(-1) #On lance la musique, elle se répète à l'infinie
    
    #Déclaration des différentes Hitboxs 
    space_ship = pygame.Rect((WIDTH//2)-(WIDTH_SPACESHIP//2), HEIGHT-50, WIDTH_SPACESHIP, HEIGHT_SPACESHIP) #Vaisseau Joueur
    with open(os.path.dirname(os.path.abspath(__file__)) + f'\Assets\Level {level}.txt', 'r') as file:
        liste = list(file)
        aliens = []
        for line in liste:
            l = []
            for value in list(line):
                if value != '\n':
                    l.append(value)
            aliens.append(l)
    for i, row in enumerate(aliens):
        y = i * WIDTH_ALIEN3
        for j, value in enumerate(row):
            x = j * WIDTH_ALIEN3
            if value == '1':
                aliens[i][j]=(pygame.Rect(x, 100 + y, WIDTH_ALIEN1, HEIGHT_ALIEN1))
                
            elif value == '2':
                aliens[i][j]=(pygame.Rect(x, 100 + y, WIDTH_ALIEN2, HEIGHT_ALIEN2))
                
            elif value == '3':
                aliens[i][j]=(pygame.Rect(x, 100 + y, WIDTH_ALIEN3, HEIGHT_ALIEN3))

    aliens = reduce(lambda x,y: x+y, aliens)

    for i in range(aliens.count('0')):
        aliens.remove('0')

    to_kill = len(aliens)
    


    while True: # Boucle principale du jeu, se répète à l'infinie tant qu'on appuie pas sur la croix
        clock.tick(FPS) #La fenêtre tourne à 60 images par secondes

    #Définition des évènements
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #"quitter le jeu": on quitte la boucle
                pygame.quit()
                break
            if event.type == LIVES: #Perte d'une vie
                LIVELOSS_SOUND.play()
                liveNumber -=1
            if event.type == INVASION: #Les ennemies sont à un certain seuil
                liveNumber = 0
            if event.type == ALIEN_HIT : #Évènement alien touché
                score += 1 #Incrémentation score si alien détruit
               
            #Gestion des tirs ennemies grâce au timer
            if event.type == ALIEN_FIRE:
                create_alien_laser(level, aliens, alien_lasers)
            
        keys_pressed = pygame.key.get_pressed() #Vérification de quelles touches sont appuyées
        create_laser(lasers, keys_pressed, space_ship, level)
        space_ship_movement(keys_pressed, space_ship)#Appelle fonction qui déplace le vaisseau
        aliens_movement(aliens, to_kill)

        p1 = t.Thread(target = manage_explosions(explosions))
        p2 = t.Thread(target = lasers_movements(lasers, alien_lasers))
        p3 = t.Thread(target = collision_laser(aliens, lasers, explosions))
        p4 = t.Thread(target = collision_alien_laser(space_ship, alien_lasers))
        p5 = t.Thread(target = draw_window(liveNumber, score, space_ship, aliens, lasers, alien_lasers, explosions, level))#Appelle fonction qui affiche les divers éléments
      
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
 
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
  
        if liveNumber <= 0: #Quand on n'a plus de vies
            draw_loss() #Appelle fonction perdu
            break #On quitte la boucle principale du jeu
        if len(aliens) == 0:#Quand on a détruit tous les aliens
            if level < 4:
                level += 1
                draw_level_cleared(level)
                pygame.time.set_timer(ALIEN_FIRE, ALIEN_FIRE_SPEED) #Timer déclenchement d'un tir ennemie
                liveNumber = 3 # Nombre de vies
                lasers = [] #Laser du joueur mit à 0
                alien_lasers = [] #Liste des lasers ennemie
                explosions = []
    
                with open(os.path.dirname(os.path.abspath(__file__)) + f'\Assets\Level {level}.txt', 'r') as file:
                    liste = list(file)
                    aliens = []
                    for line in liste:
                        l = []
                        for value in list(line):
                            if value != '\n':
                                l.append(value)
                        aliens.append(l)
                for i, row in enumerate(aliens):
                    y = i * WIDTH_ALIEN3
                    for j, value in enumerate(row):
                        x = j * WIDTH_ALIEN3
            
                        if value == '1':
                            aliens[i][j]=(pygame.Rect(x, 100 + y, WIDTH_ALIEN1, HEIGHT_ALIEN1))
                            
                        elif value == '2':
                            aliens[i][j]=(pygame.Rect(x, 100 + y, WIDTH_ALIEN2, HEIGHT_ALIEN2))
                            
                        elif value == '3':
                            aliens[i][j]=(pygame.Rect(x, 100 + y, WIDTH_ALIEN3, HEIGHT_ALIEN3))
                            

                aliens = reduce(lambda x,y: x+y, aliens)
                for i in range(aliens.count('0')):
                    aliens.remove('0')
                to_kill = len(aliens)
                

            else:
                draw_win() #Appelle fonction gagné
                break #On quitte la boucle principale du jeu

# Lancement du jeu
while True:
    main()