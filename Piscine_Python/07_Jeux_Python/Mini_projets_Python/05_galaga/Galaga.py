import pygame
import os
import random
pygame.init()

WIDTH, HEIGHT = 900, 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #On définit la fenêtre
pygame.display.set_caption("Galaga") #Nom de la fenetre

FPS = 60

SPAWN_ENEMY = pygame.USEREVENT + 1
ALIEN_HIT = pygame.USEREVENT + 2
ALIEN_SHOOT = pygame.USEREVENT + 3
LIFE = pygame.USEREVENT + 4
INVINCIBLE = pygame.USEREVENT + 5
SCORE = pygame.USEREVENT + 6


pygame.mixer.init() 
pygame.mixer.music.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Music.ogg')
LASER_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\laser1.wav')
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\explosion.wav')
LIVELOSS_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Live Loss.wav')
YOU_LOSE = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\You lose.mp3')
YOU_WIN = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\You Win.mp3')
WINNER_MUSIC = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Winner music.wav')
ALIEN_LASER_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\laser2.wav')
SPECIAL_LASER_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Special launch.wav')
SPECIAL_LASER_IMPACT_SOUND = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Special Impact.wav')


#Police d'écriture  des textes (score, message victoire)
pygame.font.init() 
FONT = pygame.font.SysFont('Impact', 40)
CAP_FONT = pygame.font.SysFont('Impact', 150)

ALIEN_SPEED = 5
ALIEN_LASER_SPEED = [4, 7, 9]

WIDTH_ALIEN, HEIGHT_ALIEN = [40, 45, 50, 55, 60, 65], [40, 50, 60, 55, 120, 120]

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Fond.jpeg'), (WIDTH, HEIGHT))

ALIEN_0 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Alien1.png'), (WIDTH_ALIEN[0], HEIGHT_ALIEN[0]))
ALIEN_1 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Alien2.png'), (WIDTH_ALIEN[1], HEIGHT_ALIEN[1]))
ALIEN_2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Alien3.png'), (WIDTH_ALIEN[2], HEIGHT_ALIEN[2]))
ALIEN_3 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Alien4.png'), (WIDTH_ALIEN[3], HEIGHT_ALIEN[3]))
ALIEN_4 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Alien5.png'), (WIDTH_ALIEN[4], HEIGHT_ALIEN[4]))
ALIEN_5 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Alien6.png'), (WIDTH_ALIEN[5], HEIGHT_ALIEN[5]))
LIST_ALIEN = [ALIEN_0, ALIEN_1, ALIEN_2, ALIEN_3, ALIEN_4, ALIEN_5]

ALIEN_LASER_0 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Laser 0.png'), (WIDTH_ALIEN[0], HEIGHT_ALIEN[0]))
ALIEN_LASER_1 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Laser 1.png'), (WIDTH_ALIEN[1], HEIGHT_ALIEN[1]))
ALIEN_LASER_2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Laser 2.png'), (WIDTH_ALIEN[2], HEIGHT_ALIEN[2]))
ALIEN_LASER_3 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Laser 3.png'), (WIDTH_ALIEN[3], HEIGHT_ALIEN[3]))
ALIEN_LASER_4 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Laser 4.png'), (WIDTH_ALIEN[4], HEIGHT_ALIEN[4]))
ALIEN_LASER_5 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Laser 5.png'), (WIDTH_ALIEN[5], HEIGHT_ALIEN[5]))
LIST_LASER = [ALIEN_LASER_0, ALIEN_LASER_1, ALIEN_LASER_2, ALIEN_LASER_3, ALIEN_LASER_4, ALIEN_LASER_5]

#Images des Explosions + redimension
WIDTH_EXPLOSION, HEIGHT_EXPLOSION = 100, 100 #Taille des explosions
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

WIDTH_SPACESHIP, HEIGHT_SPACESHIP = 50, 50
SPACESHIP_SPEED = 10
SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Spaceship.png'), (WIDTH_SPACESHIP, HEIGHT_SPACESHIP))

WIDTH_LASER, HEIGHT_LASER = 50, 50
LASER_SPEED = 10
LASER = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Laser.png'), (WIDTH_LASER, HEIGHT_LASER))
SPECIAL_LASER = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Special laser.png'), (WIDTH_LASER * 2, HEIGHT_LASER * 2))

def draw_window(space_ship, lasers, spawning_enemies, enemies, explosions, enemy_lasers, life, score, level, special_laser):

    WIN.blit(BACKGROUND, (0, 0))

    WIN.blit(SPACESHIP, (space_ship.x, space_ship.y))

    
    for laser in lasers:
        WIN.blit(LASER, (laser.x, laser.y))
    
    for enemy in enemies:
        if enemy.w == 40:
            WIN.blit(ALIEN_0, (enemy.x, enemy.y))
        elif enemy.w == 45:
            WIN.blit(ALIEN_1, (enemy.x, enemy.y))
        elif enemy.w == 50:
            WIN.blit(ALIEN_2, (enemy.x, enemy.y))
        elif enemy.w == 55:
            WIN.blit(ALIEN_3, (enemy.x, enemy.y))
        elif enemy.w == 60:
            WIN.blit(ALIEN_4, (enemy.x, enemy.y))
        elif enemy.w == 65:
            WIN.blit(ALIEN_5, (enemy.x, enemy.y))
    for enemy in spawning_enemies:
        if enemy.w == 40:
            WIN.blit(ALIEN_0, (enemy.x, enemy.y))
        elif enemy.w == 45:
            WIN.blit(ALIEN_1, (enemy.x, enemy.y))
        elif enemy.w == 50:
            WIN.blit(ALIEN_2, (enemy.x, enemy.y))
        elif enemy.w == 55:
            WIN.blit(ALIEN_3, (enemy.x, enemy.y))
        elif enemy.w == 60:
            WIN.blit(ALIEN_4, (enemy.x, enemy.y))
        elif enemy.w == 65:
            WIN.blit(ALIEN_5, (enemy.x, enemy.y))

    for laser in enemy_lasers:
        if laser.w == 40:
            WIN.blit(LIST_LASER[0], (laser.x, laser.y))
        elif laser.w == 45:
            WIN.blit(LIST_LASER[1], (laser.x, laser.y))
        elif laser.w == 50:
            WIN.blit(LIST_LASER[2], (laser.x, laser.y))
        elif laser.w == 55:
            WIN.blit(LIST_LASER[3], (laser.x, laser.y))
        elif laser.w == 60:
            WIN.blit(LIST_LASER[4], (laser.x, laser.y))
        elif laser.w == 65:
            WIN.blit(LIST_LASER[5], (laser.x, laser.y))

    WIN.blit(SPECIAL_LASER, (special_laser.x, special_laser.y))
       
    for explosion in explosions:
        if explosion[0]:#Si explosion à lieu
            WIN.blit(LIST_EXPLOSION[explosion[2]], (explosion[1][0]-30, explosion[1][1]-30))
    
    pygame.draw.rect(WIN,  "black", (0, 0, WIDTH, 45))
    
    for i in range (1, life+1):#Affichage des vies
        WIN.blit(SPACESHIP, (WIDTH - WIDTH_SPACESHIP * i, 0))

    #Affichage texte score
    scoreText = FONT.render(f"Score: {score}" , 1, "white")
    WIN.blit(scoreText, (0, 0))

    #Affichage du level en cours
    levelText = FONT.render(f"Level: {level}", 1, "white")
    WIN.blit(levelText, (WIDTH / 2 - levelText.get_width() / 2, 0))

    pygame.display.update()

def laser_movement(lasers, special_laser):
    special_laser.y -= LASER_SPEED
    for laser in lasers:
        laser.y -= LASER_SPEED
        if laser.y < 0 :
            lasers.remove(laser)
        if special_laser.y < 0:
            special_laser = pygame.Rect(0, 0, 0, 0)
      
def spawn(spawning_enemies, level):
    enemy_type = random.randrange(0, level + 1)
    positionx = random.randrange(200, WIDTH-200)
    for i in range(random.randrange(6 - (enemy_type // 2) , 10 - (enemy_type // 2))):
        spawning_enemies.append(pygame.Rect(positionx , -100 - HEIGHT_ALIEN[enemy_type] * i , WIDTH_ALIEN[enemy_type], HEIGHT_ALIEN[enemy_type]))

def enemy_spawn_move(spawning_enemies, enemies):
    count = 0
    for enemy in spawning_enemies:
        count += 1
        if enemy.y <= 100:
            enemy.y += ALIEN_SPEED
        if enemy.y >= 100:
            if enemy.collidelist(enemies) == -1:
                enemies.append(enemy)
                spawning_enemies.remove(enemy)
                count += 2
                continue
        
            if enemy.collidelist(enemies) > -1  and enemy.x > 0 and count % 2 == 0:
                enemy.x -= ALIEN_SPEED
        
            elif enemy.collidelist(enemies) > -1  and enemy.x < WIDTH - 60 and count % 2 == 1:
                enemy.x += ALIEN_SPEED

            if enemy.collidelist(enemies) > -1  and count % 3 == 0:
                enemy.y += ALIEN_SPEED
                if enemy.x > WIDTH - 61:
                    enemy.x -= ALIEN_SPEED
                elif enemy.x < 1:
                    enemy.x += ALIEN_SPEED

           

def enemy_kill(lasers, enemies, spawning_enemies, explosions, special_laser):
    for enemy in enemies:
        if enemy.y > HEIGHT - 100:
            draw_loss()
        for laser in lasers:
            if laser.colliderect(enemy):
                EXPLOSION_SOUND.play()
                pygame.event.post(pygame.event.Event(SCORE)) 
                explosions.append([True, [enemy.x, enemy.y], 0])
                lasers.remove(laser)
                enemies.remove(enemy)
        if enemy.colliderect(special_laser):
            SPECIAL_LASER_IMPACT_SOUND.play()
            pygame.event.post(pygame.event.Event(SCORE)) 
            explosions.append([True, [enemy.x, enemy.y], 0])
            try:
                enemies.remove(enemy)
            except ValueError:
                pass

                
    for enemy in spawning_enemies:
        for laser in lasers:
            if laser.colliderect(enemy):
                EXPLOSION_SOUND.play()
                pygame.event.post(pygame.event.Event(SCORE))
                explosions.append([True, [enemy.x, enemy.y], 0])
                lasers.remove(laser)
                spawning_enemies.remove(enemy)

def manage_explosion(explosions):
    for explosion in explosions:
        if explosion[0]: #Si explosion en cours
            explosion[2] += 1 #On change d'image à chaque frame
        if explosion[2] >= 18: #Quand on arrive à l'image finale, on stop l'explosion et on réinitialise
            explosions.remove(explosion)

            
def enemy_laser_movement(enemy_lasers):    
    for laser in enemy_lasers:
        if laser.w == 40:
            laser.y += ALIEN_LASER_SPEED[0]  
        elif laser.w == 45:
            laser.y += ALIEN_LASER_SPEED[0]  
        elif laser.w == 50:
            laser.y += ALIEN_LASER_SPEED[1] 
        elif laser.w == 55:
            laser.y += ALIEN_LASER_SPEED[1] 
        elif laser.w == 60:
            laser.y += ALIEN_LASER_SPEED[2] 
        elif laser.w == 65:
            laser.y += ALIEN_LASER_SPEED[2] 

def space_ship_hit(space_ship, enemy_lasers, explosions, special_laser):
    for laser in enemy_lasers:
        if laser.colliderect(special_laser) and laser.w <60:
            enemy_lasers.remove(laser)
        if laser.colliderect(space_ship):
            pygame.event.post(pygame.event.Event(LIFE))
            explosions.append([True, [space_ship.x, space_ship.y], 0])
            enemy_lasers.remove(laser)


def add_enemy_laser(enemy_lasers, enemies, level):
    for _ in range (1, level+1):
        try:
            chosen_enemy = random.randrange(0, len(enemies))
            if enemies[chosen_enemy].w == 40:
                enemy_lasers.append(pygame.Rect(enemies[chosen_enemy].x, enemies[chosen_enemy].y, WIDTH_ALIEN[0], HEIGHT_ALIEN[0]))
            elif enemies[chosen_enemy].w == 45:
                enemy_lasers.append(pygame.Rect(enemies[chosen_enemy].x, enemies[chosen_enemy].y, WIDTH_ALIEN[1], HEIGHT_ALIEN[1]))
            elif enemies[chosen_enemy].w == 50:
                enemy_lasers.append(pygame.Rect(enemies[chosen_enemy].x, enemies[chosen_enemy].y, WIDTH_ALIEN[2], HEIGHT_ALIEN[2]))
            elif enemies[chosen_enemy].w == 55:
                enemy_lasers.append(pygame.Rect(enemies[chosen_enemy].x, enemies[chosen_enemy].y, WIDTH_ALIEN[3], HEIGHT_ALIEN[3]))
            elif enemies[chosen_enemy].w == 60:
                enemy_lasers.append(pygame.Rect(enemies[chosen_enemy].x, enemies[chosen_enemy].y, WIDTH_ALIEN[4], HEIGHT_ALIEN[4]))
            elif enemies[chosen_enemy].w == 65:
                enemy_lasers.append(pygame.Rect(enemies[chosen_enemy].x, enemies[chosen_enemy].y, WIDTH_ALIEN[5], HEIGHT_ALIEN[5]))
        except ValueError:
            pass


def space_ship_movement(keys_pressed, space_ship):
    if keys_pressed[pygame.K_LEFT] and space_ship.x >= 10: # Aller à gauche
        space_ship.x -= SPACESHIP_SPEED
    if keys_pressed[pygame.K_RIGHT] and space_ship.x <= WIDTH - WIDTH_SPACESHIP - 10: # Aller à droite
        space_ship.x += SPACESHIP_SPEED

def draw_win():
    pygame.time.set_timer(SPAWN_ENEMY, 0)
    pygame.time.set_timer(ALIEN_SHOOT, 0)
    pygame.mixer.music.stop()
    YOU_WIN.play()
    WINNER_MUSIC.play()
    #Affichage du texte de victoire
    text = CAP_FONT.render('VICTOIRE', 1, "white")
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()

    pygame.time.wait(5000)#On affiche tout ca pendant 5 secondes avant le redémarrage du jeu

def draw_loss():
    pygame.time.set_timer(SPAWN_ENEMY, 0)
    pygame.time.set_timer(ALIEN_SHOOT, 0)
    pygame.mixer.music.stop()
    YOU_LOSE.play()
    #Affichage du texte de défaite
    text = CAP_FONT.render('GAME OVER', 1, "white")
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.wait(5000)#On affiche tout ca pendant 5 secondes avant le redémarrage du jeu

def draw_level_cleared(level):
    pygame.time.set_timer(SPAWN_ENEMY, 0)
    pygame.time.set_timer(ALIEN_SHOOT, 0)
    # Affichage du texte de niveau suivant
    text = CAP_FONT.render(f'Level {level}', 1, "white")
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    pygame.display.update() # On rafraîchît l'écran

    pygame.time.delay(3000) # On affiche tout ca pendant 3 secondes avant le passage au niveau suivant


def main():
    clock = pygame.time.Clock() #variable horloge
    run = True
    score = 0
    level = 1
    life = 3
    lasers = []
    enemy_lasers = []
    enemies = []
    spawning_enemies = []
    explosions = []
    special_laser = pygame.Rect(0, 0, 0, 0)
    enemies_to_kill = 20 * level
    unvulnerable = False
    reload_speed = 10
    special_reload_speed = 200
    
    pygame.time.set_timer(SPAWN_ENEMY, 3000 - 250 * level)
    pygame.time.set_timer(ALIEN_SHOOT, 2000 - 200 * level)

    pygame.mixer.music.play(-1)
    
    space_ship = pygame.Rect((WIDTH // 2)-(WIDTH_SPACESHIP // 2), HEIGHT - HEIGHT_SPACESHIP - 50, WIDTH_SPACESHIP, HEIGHT_SPACESHIP) #Vaisseau Joueur

    while run:
        clock.tick(FPS) #La fenêtre tourne à 60 images par secondes

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quitter la fenêtre en appuyant sur la croix
                pygame.quit() 
                break
            if event.type == SPAWN_ENEMY:
                if enemies_to_kill > 0:
                    spawn(spawning_enemies, level)

            if event.type == ALIEN_SHOOT:
                add_enemy_laser(enemy_lasers, enemies, level)
                if len(enemy_lasers) > 0:
                    ALIEN_LASER_SOUND.play()
            if event.type == LIFE:
                if not unvulnerable:
                    life -= 1
                    LIVELOSS_SOUND.play()
                    unvulnerable = True
                    pygame.time.set_timer(INVINCIBLE, 3000)
            if event.type == SCORE:
                score += 1
                enemies_to_kill -= 1
            if event.type == INVINCIBLE:
                unvulnerable = False
                pygame.time.set_timer(INVINCIBLE, 0)

        keys_pressed = pygame.key.get_pressed() #Vérification de quelles touches sont appuyées

        if keys_pressed[pygame.K_SPACE] and len(lasers) < 1 + level:
            if reload_speed == 0:
                lasers.append(pygame.Rect(space_ship.x, space_ship.y, WIDTH_LASER, HEIGHT_LASER))
                LASER_SOUND.play()
                reload_speed = 10
            else:
                reload_speed -= 1
        if keys_pressed[pygame.K_LCTRL] and special_reload_speed == 0:
            special_laser = pygame.Rect(space_ship.x - 25, space_ship.y - 25, WIDTH_LASER * 2, HEIGHT_LASER * 2)
            SPECIAL_LASER_SOUND.play()
            special_reload_speed = 200 - level * 20
        elif special_reload_speed > 0:
            special_reload_speed -= 1


        enemy_spawn_move(spawning_enemies, enemies)
        enemy_kill(lasers, enemies, spawning_enemies, explosions, special_laser)
        manage_explosion(explosions)
        laser_movement(lasers, special_laser)
        space_ship_hit(space_ship, enemy_lasers, explosions, special_laser)
        enemy_laser_movement(enemy_lasers)
        space_ship_movement(keys_pressed, space_ship)
        draw_window(space_ship, lasers, spawning_enemies, enemies, explosions, enemy_lasers, life, score, level, special_laser)

        if life == 0:
            draw_loss()
            break
        if enemies_to_kill < 0 and len(enemies) == 0:
            level += 1
            if level == 6:
                draw_win()
                break
            else:
                draw_level_cleared(level)
                unvulnerable = False
                lasers = []
                enemy_lasers = []
                enemies = []
                spawning_enemies = []
                explosions = []
                enemies_to_kill = 40 * level
                life = 3
                special_laser = pygame.Rect(0, 0, 0, 0)
                pygame.time.set_timer(SPAWN_ENEMY, 3000 - 250 * level)
                pygame.time.set_timer(ALIEN_SHOOT, 2000 - 200 * level)



while True:
    main()