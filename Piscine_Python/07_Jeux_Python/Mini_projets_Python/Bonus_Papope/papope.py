import pygame, random, os
from firebase_admin import credentials, firestore, initialize_app
cred = credentials.Certificate(os.path.dirname(os.path.abspath(__file__)) + '\Assets\devia-f6704-firebase-adminsdk-ay7ci-26941e7999.json')
app = initialize_app(cred)

FPS = 60 
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("PAPOPE")
W_M, H_M = 150, 150
WIDTH = pygame.display.get_surface().get_width()
HEIGHT = pygame.display.get_surface().get_height()
B_E = pygame.Rect(0, 0, 1, HEIGHT)
B_W = pygame.Rect(WIDTH, 0, 1, HEIGHT)
B_N = pygame.Rect(0, 0, WIDTH, 1)
B_S = pygame.Rect(0, HEIGHT, WIDTH, 1)
MACRON = pygame.transform.scale(pygame.image.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Macron.png'), (W_M, H_M))
pygame.mixer.init() 
MUSIC = pygame.mixer.music.load(os.path.dirname(os.path.abspath(__file__)) + '\Assets\Papope.mp3')
pygame.font.init() 
FONT = pygame.font.SysFont("Impact", 100)
pygame.mixer.music.play(-1)




def draw_window(color, macrons, color_text, timer):
    WIN.fill(color)
    for macron in macrons:
        WIN.blit(MACRON, (macron.x, macron.y))

    text = FONT.render("C'EST VENDREDI", 1, color_text) # définition du texte de défaite
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT//2 - text.get_height()/2)) # On affiche le texte de défaite au milieu de la fenêtre
    scoreText = FONT.render("Score: " + str(len(macrons)), 1, color_text)
    WIN.blit(scoreText, (0, 0))
    timerText = FONT.render("Temps restant: " + timer, 1, color_text)
    WIN.blit(timerText, (WIDTH - timerText.get_width(), 0))


    pygame.display.update()


def macron_move(macrons, macrons_speed):
    for i, macron in enumerate(macrons):

        macron.x += macrons_speed[i][0]
        macron.y += macrons_speed[i][1]

        if B_S.colliderect(macron):
            macrons_speed[i][1] = random.randint(10, 15)
            macrons_speed[i][1] *= -1


        if B_N.colliderect(macron):
            macrons_speed[i][1] = random.randint(10, 15)
 
        
        if B_W.colliderect(macron):
            macrons_speed[i][0] = random.randint(10, 15)
            macrons_speed[i][0] *= -1


        if B_E.colliderect(macron):
            macrons_speed[i][0] = random.randint(10, 15)
            
    return(macrons_speed)

def end(macrons, color, color_text, clock):

    name = os.getlogin().replace('.', ' ')


    db = firestore.client()

    doc = db.collection("papope").document(name).get()

    if doc.exists:
        if doc.to_dict()['MaxScore'] < int(len(macrons)):
            db.collection("papope").document(name).set({'MaxScore' : int(len(macrons))})
    else:
        db.collection("papope").document(name).set({'MaxScore' : int(len(macrons))})

    pygame.time.set_timer(pygame.USEREVENT, 0)
    pause = True
    pygame.time.delay(500)
    i = 0
    while pause:
        clock.tick(FPS)
        i += 1
        if i % 60 == 0:
            color = [0, 0, 150]
            color_text = [150, 0, 0]
        elif i % 60 == 20:
            color = [150, 150, 150]
            color_text = [0, 0, 150]
        elif i % 60 == 40:
            color = [150, 0, 0]
            color_text = [150, 150, 150] 

        text = FONT.render('Score : ' + str(len(macrons)), 1, color_text)

        text_1 = FONT.render(f"Personnal Best Score : {doc.to_dict()['MaxScore']}", 1, color_text)

        champion = [doc.id for doc in db.collection('papope').order_by("MaxScore", direction=firestore.Query.DESCENDING).limit(1).stream()]
        best = [doc.to_dict()['MaxScore'] for doc in db.collection('papope').order_by("MaxScore", direction=firestore.Query.DESCENDING).limit(1).stream()]

        text_2 = FONT.render(f"Top 1 : {best[0]} - {champion[0]}", 1, color_text)

        WIN.fill(color)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//4 * 1 - text.get_height()//2))
        WIN.blit(text_1, (WIDTH//2 - text_1.get_width()//2, HEIGHT//4 * 2 - text.get_height()//2))
        WIN.blit(text_2, (WIDTH//2 - text_2.get_width()//2, HEIGHT//4 * 3 - text.get_height()//2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                WIN.fill(0)
                pygame.quit()
                break

            if i > 60:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pause = False
                    break

def main(nb_macron):
    pygame.event.clear()
    
    clock = pygame.time.Clock()
    counter, timer = 10, '10'.rjust(3)
    i = 0
    macrons = [pygame.Rect(random.randint(0, WIDTH - W_M), random.randint(0, HEIGHT - H_M), W_M, H_M) for _ in range(nb_macron)]
    macrons_speed = [[random.randint(10, 15), random.randint(10, 15)] for _ in range(nb_macron)]
    start = False
    color = [0, 0, 150]
    color_text = [150, 150, 150]
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                WIN.fill(0)
                pygame.quit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                start = True
                if event.button == 1:
                    for macron in macrons:
                        if macron.collidepoint((mouse_x, mouse_y)):
                            macrons.append(pygame.Rect(macron.x, macron.y, W_M, H_M))
                            macrons_speed.append([random.randint(10, 15), random.randint(10, 15)])
                            break
            if event.type == pygame.USEREVENT:
                if start:
                    counter -= 1
                    timer = str(counter).rjust(3)
        if counter == 0:
            end(macrons, color, color_text, clock)
            main(1)

        i += 1
        if i % 60 == 0:
            color = [0, 0, 150]
            color_text = [150, 0, 0]
        elif i % 60 == 20:
            color = [150, 150, 150]
            color_text = [0, 0, 150]
        elif i % 60 == 40:
            color = [150, 0, 0]
            color_text = [150, 150, 150]  
        
        if start:
            macrons_speed = macron_move(macrons, macrons_speed)
        draw_window(color, macrons, color_text, timer)

while True:
    main(1)