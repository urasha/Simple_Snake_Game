import pygame
import random
import sys
from numpy.random import choice
import shelve

pygame.init()
pygame.font.init()

# Constants
SIZE = (600, 500)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (4, 150, 180)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 30

clock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Mac game')

font = pygame.font.SysFont('Comic Sans', 24)
font_1 = pygame.font.SysFont('Arial', 64)

# snake metrics
snake_pos = {
    'x': 300,
    'y': 250
}

x_change = 10
y_change = 0

snake_speed = 10

snake_tails = [[snake_pos['x'] - 10, snake_pos['y']],
               [snake_pos['x'] - 20, snake_pos['y']]]

# food metrics
food = {
    'x': 0,
    'y': 0,
    'type': 'apple',
    'color': RED
}

food_types = ['apple', 'blueberry']
probability = [0.75, 0.25]

possible_x = range(30, SIZE[0] - 19, 10)
possible_y = range(30, SIZE[1] - 19, 10)

is_eaten = False

score = 0


def game_over():
    screen.fill(BLACK)
    end_message = font_1.render('GAME OVER', 1, WHITE)
    screen.blit(end_message, (110, 190))
    pygame.display.update()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()


def check_top_score():
    file = shelve.open('score.txt')
    if file:
        if int(file['score']) < score:
            file['score'] = score
    else:
        file['score'] = score


def terminate():
    pygame.quit()
    sys.exit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and x_change != -snake_speed:
                x_change = snake_speed
                y_change = 0
            if event.key == pygame.K_LEFT and x_change != snake_speed:
                x_change = -snake_speed
                y_change = 0
            if event.key == pygame.K_UP and y_change != snake_speed:
                x_change = 0
                y_change = -snake_speed
            if event.key == pygame.K_DOWN and y_change != -snake_speed:
                x_change = 0
                y_change = snake_speed

    screen.fill(BLACK)

    # is eaten?
    if not is_eaten:
        food['x'] = random.choice(possible_x)
        food['y'] = random.choice(possible_y)
        food['type'] = choice(food_types, p=probability)
        is_eaten = True

    # check apple and snake position
    if snake_pos['x'] in range(food['x'], food['x'] + 11) \
            and snake_pos['y'] in range(food['y'], food['y'] + 11):

        snake_tails.append([food['x'], food['y']])

        if food['type'] == 'apple':
            score += 1
        elif food['type'] == 'blueberry':
            score += 2

        is_eaten = False

    # change coordinates
    lx = snake_pos['x']
    ly = snake_pos['y']

    for i in range(len(snake_tails)):
        _lx = snake_tails[i][0]
        _ly = snake_tails[i][1]

        snake_tails[i][0] = lx
        snake_tails[i][1] = ly

        lx = _lx
        ly = _ly

    snake_pos['x'] += x_change
    snake_pos['y'] += y_change

    # teleport snake
    if snake_pos['x'] > 600:
        snake_pos['x'] = 0
    elif snake_pos['x'] < 0:
        snake_pos['x'] = 600
    elif snake_pos['y'] > 500:
        snake_pos['y'] = 0
    elif snake_pos['y'] < 0:
        snake_pos['y'] = 500

    # check tail's break
    for i in snake_tails:
        if snake_pos['x'] == i[0] and snake_pos['y'] == i[1]:
            game_over()

    # draw snake
    pygame.draw.rect(screen, GREEN, (snake_pos['x'], snake_pos['y'], 10, 10))

    for i in range(len(snake_tails)):
        pygame.draw.rect(screen, GREEN, (snake_tails[i][0], snake_tails[i][1], 10, 10))

    # draw apple
    if food['type'] == 'apple':
        food['color'] = RED
    elif food['type'] == 'blueberry':
        food['color'] = BLUE

    pygame.draw.rect(screen, food['color'], (food['x'], food['y'], 10, 10))

    # show score
    if shelve.open('score.txt'):
        top_score_text = font.render(f'Top score: {shelve.open("score.txt")["score"]}', 1, WHITE)
    else:
        top_score_text = font.render(f'Top score: {score}', 1, WHITE)

    score_text = font.render(f'Score: {score}', 1, WHITE)

    screen.blit(top_score_text, (10, 10))
    screen.blit(score_text, (10, 30))

    check_top_score()

    pygame.display.update()
    clock.tick(FPS)
