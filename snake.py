import pygame
import random
import sys

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

# apple metrics
apple = {
    'x': 0,
    'y': 0,
}

possible_x = range(10, SIZE[0] - 19, 10)
possible_y = range(10, SIZE[1] - 19, 10)

is_eaten = False

score = 0


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
        apple['x'] = random.choice(possible_x)
        apple['y'] = random.choice(possible_y)
        is_eaten = True

    # check apple and snake position
    if snake_pos['x'] in range(apple['x'], apple['x'] + 11) \
            and snake_pos['y'] in range(apple['y'], apple['y'] + 11):

        snake_tails.append([apple['x'], apple['y']])
        score += 1
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
            terminate()

    # draw snake
    pygame.draw.rect(screen, GREEN, (snake_pos['x'], snake_pos['y'], 10, 10))

    for i in range(len(snake_tails)):
        pygame.draw.rect(screen, GREEN, (snake_tails[i][0], snake_tails[i][1], 10, 10))

    # draw apple
    pygame.draw.rect(screen, RED, (apple['x'], apple['y'], 10, 10))

    # show score
    render = font.render(f'Score: {score}', 1, WHITE)
    screen.blit(render, (10, 10))

    pygame.display.update()
    clock.tick(FPS)
