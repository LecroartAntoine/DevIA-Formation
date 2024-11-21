import pygame
from pygame import gfxdraw
import os
import random
pygame.init()

WIDTH, HEIGHT = 700, 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #On définit la fenetre
pygame.display.set_caption("Mastermind") #Nom de la fenetre

BACKGROUND = pygame.image.load(os.path.dirname(os.path.abspath(__file__)) +'\Assets\Fond.jpg')

pygame.font.init() 
END_FONT = pygame.font.SysFont("Impact", 100 )
MENU_FONT = pygame.font.SysFont("Impact", 50)

CIRCLE_COLOR = (22, 155, 155)
WHITE = (255, 255, 255)
RED = (180, 0, 0)
BLUE = (0, 0, 180)
GREEN = (0, 180, 0)
YELLOW = (180, 180, 0)
PURPLE = (200, 0, 200)
BROWN = (102, 50, 0)
LIST_COLOR = [RED, BLUE, GREEN, YELLOW, PURPLE, BROWN, WHITE]
LIST_RESULT_COLOR = [RED, WHITE]

RECT_WIDTH, RECT_HEIGHT = 200, 60

ROUND_SIZE = 25

FPS = 60

try_number = 0

def draw_window(combi, result):
    WIN.blit(BACKGROUND, (0, 0))
    for i in range(try_number + 1):
        for j in range(4):
            gfxdraw.filled_circle(WIN, j * ROUND_SIZE * 3 + 100, i * 85 + 70, ROUND_SIZE, LIST_COLOR[combi[i][j]])
            gfxdraw.aacircle(WIN, j * ROUND_SIZE * 3 + 100, i * 85 + 70, ROUND_SIZE - 1, CIRCLE_COLOR)
            gfxdraw.aacircle(WIN, j * ROUND_SIZE * 3 + 100, i * 85 + 70, ROUND_SIZE, CIRCLE_COLOR)
            gfxdraw.aacircle(WIN, j * ROUND_SIZE * 3 + 100, i * 85 + 70, ROUND_SIZE + 1, CIRCLE_COLOR)
    
    for i in range(try_number + 1):
        if len(result[i]) != 0:
            for j in range(len(result[i])):
                gfxdraw.filled_circle(WIN, j * ROUND_SIZE * 3 + 400, i * 85 + 70, 5, LIST_RESULT_COLOR[result[i][j]])
    
    pygame.display.update()

def generate_code(difficulty):
    code = []
    for _ in range (4):
        code.append(random.randrange(4 + difficulty))
    return(code)
    
def cycle_color(mouse_x, mouse_y, circles, combi, difficulty):
    for i in range(4):
        if circles[try_number][i].collidepoint(mouse_x, mouse_y):
            if combi[try_number][i] < 3 + difficulty:
                combi[try_number][i] += 1
            elif combi[try_number][i] == 3 + difficulty: 
                combi[try_number][i] = 0

def check_combi(code, combi, result):
    global try_number
    temp = combi[try_number][:]

    for i, number in enumerate(code):
        
        if number == temp[i]:
            result[try_number].append(0)
            temp[i] = -1
        elif number == temp[0] and temp[0] != code[0]:
            result[try_number].append(1)
            temp[0] = -1
            continue
        elif number == temp[1] and temp[1] != code[1]:
            result[try_number].append(1)
            temp[1] = -1
            continue
        elif number == temp[2] and temp[2] != code[2] :
            result[try_number].append(1)
            temp[2] = -1
            continue
        elif number == temp[3] and temp[3] != code[3]:
            result[try_number].append(1)
            temp[3] = -1
            continue
    

    result[try_number].sort()
    result.append([])
    combi.append([-1, -1, -1, -1])
    try_number += 1
    

def create_hitbox(circles):
    line = []
    for j in range(4):
        line.append(pygame.Rect(j * ROUND_SIZE * 3 + 75, try_number * 85 + 45, 50, 50))
    circles.append(line)

#-----Gestion de la défaite-----
def draw_lose(code):
    WIN.blit(BACKGROUND, (0, 0))
    #Affichage du texte de défaite
    text = END_FONT.render("GAME OVER", 1, "white") # définition du texte de défaite
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT//3 - text.get_height()/2)) # On affiche le texte de défaite au milieu de la fenêtre
    text_password = END_FONT.render("Password was:", 1, "white") # définition du texte de défaite
    WIN.blit(text_password, (WIDTH/2 - text_password.get_width()/2, HEIGHT//2 - text_password.get_height()/2)) # On affiche le texte de défaite au milieu de la fenêtre
    for j in range(4):
            gfxdraw.filled_circle(WIN, j * ROUND_SIZE * 3 + 225, 600, ROUND_SIZE, LIST_COLOR[code[j]])
            gfxdraw.aacircle(WIN, j * ROUND_SIZE * 3 + 225, 600, ROUND_SIZE - 1, CIRCLE_COLOR)
            gfxdraw.aacircle(WIN, j * ROUND_SIZE * 3 + 225, 600, ROUND_SIZE, CIRCLE_COLOR)
            gfxdraw.aacircle(WIN, j * ROUND_SIZE * 3 + 225, 600, ROUND_SIZE + 1, CIRCLE_COLOR)

    pygame.display.update() # on actualise l'affichage de la fenêtre
    pygame.time.delay(5000) # On met le jeu en pause 5 secs avant de redémarrer

#-----Gestion de la victoire-----
def draw_win():
    WIN.blit(BACKGROUND, (0, 0))
    #Affichage du texte de victoire
    text = END_FONT.render("YOU WIN", 1, "white") # définition du texte de victoire 
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2)) # On affiche le texte de victoire au milieu de la fenêtre
    pygame.display.update() # on actualise l'affichage de la fenêtre
    pygame.time.delay(5000) # On met le jeu en pause 5 secs avant de redémarrer

def main(difficulty):
    global try_number
    try_number = 0
 
    clock = pygame.time.Clock()
    combi = [[-1, -1, -1, -1]]
    circles = []
    result = [[]]
    code = generate_code(difficulty)
    create_hitbox(circles)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:#Quitter la fenetre en appuyant sur la croix
                pygame.quit() 
                break
            if event.type == pygame.MOUSEBUTTONDOWN: #Quand on appuie sur un boutton de la souris
                mouse_x, mouse_y = pygame.mouse.get_pos() #On traduit la position de la souris en indice d'une case grâce à la fonction get_grid_pos
                if mouse_x >= WIDTH or mouse_y >= HEIGHT: #Si la souris est en dehors de la fenetre, on recommence
                    continue
                cycle_color(mouse_x, mouse_y, circles, combi, difficulty)
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    check_combi(code, combi, result)
                    create_hitbox(circles)

        draw_window(combi, result)

        if result[try_number - 1] == [0,0,0,0]:
            draw_win()
            break
        if try_number == 10:
            draw_lose(code)
            break

def draw_menu(outline_size, difficulty_select):
    WIN.blit(BACKGROUND, (0, 0))

    if not difficulty_select:
        option_1 = MENU_FONT.render("Start", 1, "white")
        WIN.blit(option_1, (WIDTH/2 - option_1.get_width()/2, (HEIGHT//4) - option_1.get_height()/2))
        pygame.draw.rect(WIN, CIRCLE_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size[0])
        option_2 = MENU_FONT.render("Difficulty", 1, "white")
        WIN.blit(option_2, (WIDTH/2 - option_2.get_width()/2, (HEIGHT//4) * 2 - option_2.get_height()/2))
        pygame.draw.rect(WIN, CIRCLE_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) * 2 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size[1])
        option_3 = MENU_FONT.render("Quit", 1, "white")
        WIN.blit(option_3, (WIDTH/2 - option_3.get_width()/2, (HEIGHT//4) * 3 - option_3.get_height()/2))
        pygame.draw.rect(WIN, CIRCLE_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) * 3 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size[2])
    else:
        dif_1 = MENU_FONT.render("Easy", 1, "white") 
        WIN.blit(dif_1, (WIDTH/2 - dif_1.get_width()/2, (HEIGHT//4) - dif_1.get_height()/2))
        pygame.draw.rect(WIN, CIRCLE_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size[0])
        dif_2 = MENU_FONT.render("Medium", 1, "white")
        WIN.blit(dif_2, (WIDTH/2 - dif_2.get_width()/2, (HEIGHT//4) * 2 - dif_2.get_height()/2))
        pygame.draw.rect(WIN, CIRCLE_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) * 2 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size[1])
        dif_3 = MENU_FONT.render("Hard", 1, "white")
        WIN.blit(dif_3, (WIDTH/2 - dif_3.get_width()/2, (HEIGHT//4) * 3 - dif_3.get_height()/2))
        pygame.draw.rect(WIN, CIRCLE_COLOR, (WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) * 3 - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT), outline_size[2])

    pygame.display.update() 

def menu():
    clock = pygame.time.Clock()
    options_rect = []
    difficulty_select = False
    difficulty = 0
    outline_size = [2, 2, 2]
    for i in range(1, 4):
        options_rect.append(pygame.Rect(WIDTH/2 - RECT_WIDTH/2, (HEIGHT//4) * i - RECT_HEIGHT/2, RECT_WIDTH, RECT_HEIGHT))

    while True:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#Quitter la fenetre en appuyant sur la croix
                pygame.quit() 
        if event.type == pygame.MOUSEBUTTONDOWN: #Quand on appuie sur un boutton de la souris
            if mouse_x >= WIDTH or mouse_y >= HEIGHT: #Si la souris est en dehors de la fenetre, on recommence
               continue
            if options_rect[0].collidepoint(mouse_x, mouse_y) and not difficulty_select:
                main(difficulty)
            elif options_rect[1].collidepoint(mouse_x, mouse_y) and not difficulty_select:
                difficulty_select = True
            elif options_rect[2].collidepoint(mouse_x, mouse_y) and not difficulty_select:
                pygame.quit()
                break
            elif options_rect[0].collidepoint(mouse_x, mouse_y) and difficulty_select:
                difficulty = 0
                difficulty_select = False
            elif options_rect[1].collidepoint(mouse_x, mouse_y) and difficulty_select:
                difficulty = 1
                difficulty_select = False
            elif options_rect[2].collidepoint(mouse_x, mouse_y) and difficulty_select:
                difficulty = 2
                difficulty_select = False
            pygame.time.delay(100)
        
        for i in range(3):
            if options_rect[i].collidepoint(mouse_x, mouse_y):
                outline_size[i] = 5
            else:
                outline_size[i] = 2

        draw_menu(outline_size, difficulty_select)

if __name__ == '__main__':
    while True:
        menu()