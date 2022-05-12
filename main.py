import pygame
from copy import deepcopy
from random import choice,randrange
import sys

w = 10
h = 20
Tile = 40
Res = 700, 800
FPS = 60

pygame.init()
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode(Res)
clock = pygame.time.Clock()
score = 0
lines = 0
scores_table = {0:0,1:100,2:500,3:1000,4:2000}

shrift = pygame.font.SysFont('arial', 36)
text_score = shrift.render('Score:',True,pygame.Color('white'))

grid = [pygame.Rect(x * Tile, y * Tile, Tile,Tile) for x in range(w) for y in range(h)] # Массив из клеток игрового поля

figures_pos =  [[(-1,0),(-2,0),(0,0),(1,0)],
                [(0,-1),(-1,-1),(-1,0),(0,0)],
                [(-1,0),(-1,1),(0,0),(0,-1)],
                [(0,0),(-1,0),(0,1),(-1,-1)],
                [(0,0),(0,-1),(0,1),(-1,-1)],
                [(-1,0),(-1,1),(0,-1),(-1,-1)],
                [(0,0),(0,-1),(0,1),(-1,0)]]
figures = [[pygame.Rect(x + w // 2,y + 1,1,1)for x,y in fig_pos] for fig_pos in figures_pos] # Массив экземпляров класса rect
figure_rect = pygame.Rect(0,0,Tile - 2, Tile - 2)
field = [[0 for i in range(w)] for j in range(h)]

anim_count = 0
anim_speed = 60
anim_limit = 2000
figure = deepcopy(choice(figures))# переменная для текущей фигуры
figure_next = deepcopy(choice(figures))


def check():
    if figure[i].x < 0 or figure[i].x > w - 1:
        return False
    elif figure[i].y > h - 1 or field[figure[i].y][figure[i].x]:
        return False
    else:
        return True

while True:
    screen.fill(pygame.Color('black'))
    dx = 0
    rotate = False
    # delay
    for i in range(lines):
        pygame.time.wait(200)
    # comtrol
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                dx = -1
            elif event.key == pygame.K_d:
                dx = 1
            elif event.key == pygame.K_s:
                anim_limit = 100
            elif event.key == pygame.K_w:
                rotate = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                anim_limit = 2000
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check():
            figure = deepcopy(figure_old)
            break
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check():
                for i2 in range(4):
                    field[figure_old[i2].y][figure_old[i2].x] = pygame.Color('white')
                figure = figure_next
                figure_next = deepcopy(choice(figures))
                anim_limit = 2000
                break
    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check():
                figure = deepcopy(figure_old)
                break
    # check lines
    line = h - 1
    lines = 0
    for row in range(h - 1,-1,-1):
        count = 0
        for i in range(w):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < w:
            line -= 1
        else:
            lines += 1
            anim_speed += 3
    score += scores_table[lines]
    # draw grid
    [pygame.draw.rect(screen, (40,40,40), i_rect,1) for i_rect in grid]
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * Tile
        figure_rect.y = figure[i].y * Tile
        pygame.draw.rect(screen,pygame.Color('white'), figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col, in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * Tile, y * Tile
                pygame.draw.rect(screen, col, figure_rect)
    # draw next figure
    for i in range(4):
        figure_rect.x = figure_next[i].x * Tile + 350
        figure_rect.y = figure_next[i].y * Tile + 150
        pygame.draw.rect(screen,pygame.Color('white'), figure_rect)
    screen.blit(text_score, (500, 400))
    screen.blit(shrift.render(str(score), True, pygame.Color('white')),(500, 450))
    # game over
    for i in range(w):
        if field[0][i]:
            field = [[0 for i in range(w)] for i in range(h)]
            anim_count = 0
            anim_speed = 60
            anim_limit = 2000
            score = 0
    pygame.display.flip()
    clock.tick(FPS)
