import pygame
import random
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
PLAYER_SIZE = (50, 50)
FONT = pygame.font.SysFont('Verdana', 20)

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

IMAGE_PATH = "animate"
PLAYER_IMG = os.listdir(IMAGE_PATH)

player = pygame.image.load('player.png').convert_alpha()  # pygame.Surface(PLAYER_SIZE)
# player.fill(COLOR_WHITE)
# player_rect = player.get_rect()
player_rect = pygame.Rect(0, HEIGHT/2, *PLAYER_SIZE)
player_move_down = [0, 6]
player_move_up = [0, -8]
player_move_right = [6, 0]
player_move_left = [-6, 0]

def create_enemy():
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_size = enemy.get_size()
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, HEIGHT-100), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_size= bonus.get_size()
    bonus_rect = pygame.Rect(random.randint(100, WIDTH-100), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
bonuses = []

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 200)

playing = True
score = 0
img_index = 0

while playing:
    FPS.tick(200)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            player = pygame.image.load(os.path.join(IMAGE_PATH ,PLAYER_IMG[img_index]))
            img_index += 1
            if img_index >= len(PLAYER_IMG):
                img_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 =bg.get_width()
    if bg_X2 < -bg.get_width():
        bg_X2 =bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.top < WIDTH:
        player_rect = player_rect.move(player_move_right)
    
    if keys[K_LEFT] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
    
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))