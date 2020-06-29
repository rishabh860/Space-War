import pygame
from pygame import mixer
import random
import math
pygame.init()

# game screem

screen = pygame.display.set_mode((800, 600))

# title and icone setup
pygame.display.set_caption("Space War's")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# bg
background = pygame.image.load("space_bg2.png")
mixer.music.load('background.wav')
mixer.music.play(-1)

# player
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 500
playerX_changes = 0

# enemy̥
enemyimg = []
enemyX = []
enemyY = []
enemyX_changes = []
enemyY_changes = []
no_of_en = 25

for i in range(no_of_en):
    enemyimg.append(pygame.image.load('space1.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(10, 200))
    enemyX_changes.append(6)
    enemyY_changes.append(35)

# bullet

bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_changes = 0
bulletY_changes = 10
bullet_state = "ready"

def player(x, y):
    screen.blit(playerimg, (x, y))

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
gameover = pygame.font.Font('freesansbold.ttf', 62)
textX = 10
textY = 10

def show_score(x ,y):
    score_n = font.render("Score : " + str(score), True, (255,255,255))
    screen.blit(score_n, (x, y))

def gameOver():
    over = gameover.render("GAME OVER " ,  True, (255,255,255))
    screen.blit(over, (200, 250))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16 , y + 10))

def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY , 2)))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:
    
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("left")
                playerX_changes = -5
            elif event.key == pygame.K_RIGHT:
                # print("right")
                playerX_changes = 5
            elif event.key == pygame.K_SPACE:
                # print("right")
               if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX,  bulletY)
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Key is been released")
                playerX_changes = 0

    playerX += playerX_changes

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(no_of_en):

        #  game over
        if enemyY[i] > 475:
            for j in range(no_of_en):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyX_changes[i]
        if enemyX[i] <= 0:
            enemyX_changes[i] = 6
            enemyY[i] += enemyY_changes[i]
        elif enemyX[i] >= 736:
            enemyX_changes[i] = -6
            enemyY[i] += enemyY_changes[i]

        collisionhappend = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collisionhappend:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score += 1
            # print(score)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(10, 200)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"


    if bullet_state is "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_changes

    

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()