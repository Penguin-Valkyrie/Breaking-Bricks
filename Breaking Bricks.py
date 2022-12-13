import math
import pygame
import random
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 640))
pygame.display.set_caption("Bricks Breaker")

# Universal Variables
speed_multiplier = 1.075
hits = 0
score = 0
font = pygame.font.SysFont('Arial', 56)
begin = False
win_time = 0
hit_location = (screen.get_width() - 200, screen.get_height() - 75)
message_location = (screen.get_width() / 2, screen.get_height() - 250)
time_location = (25, screen.get_height() - 75)
hit_color = [255, 255, 255]

# Assets
bat = pygame.image.load('./images/bat.png')
bat = bat.convert_alpha()
bat_rect = bat.get_rect()
bat_rect[1] = screen.get_height() - 100

ball = pygame.image.load('./images/ball.png')
ball = ball.convert_alpha()
ball_rect = ball.get_rect()
ball_start = (random.randint(100, screen.get_width() - 100), 250)
ball_speed = ((random.randint(-1, 1) * 3.0 * speed_multiplier) + 1, 3.0 * speed_multiplier)
ball_served = False
sx, sy = ball_speed
ball_rect.topleft = ball_start

brick = pygame.image.load('./images/brick.jpg')
brick = brick.convert_alpha()
brick_rect = brick.get_rect()

bricks = []
brick_rows = 5
brick_gap = 10
brick_cols = screen.get_width() // (brick_rect[2] + brick_gap)
side_gap = (screen.get_width() - (brick_rect[2] + brick_gap) * brick_cols + brick_gap) // 2

for y in range(brick_rows):
    brickY = y * (brick_rect[3] + brick_gap)
    for x in range(brick_cols):
        brickX = x * (brick_rect[2] + brick_gap) + side_gap
        bricks.append((brickX, brickY))

x, y = (0, 0)

clock = pygame.time.Clock()

game_over = False

while not game_over:
    dt = clock.tick(50)

    # Draw screen
    screen.fill((0, 0, 0))

    # Check for start
    if not begin:
        message = font.render('Press SPACE to Start', True, (0, 255, 0))
        message_rect = message.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(message, message_rect)

    # Check for win
    if not bricks:
        if win_time == 0:
            win_time = (pygame.time.get_ticks() / 1000)

        score = (hits * 1000 / win_time)
        message = font.render('You Win! Score: ' + str(math.floor(score)), True, (0, 255, 0))
        message_rect = message.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(message, message_rect)
        sx, sy = (0, 0)

    # Draw Time
    if begin:
        time = font.render('time: ' + str(math.floor(pygame.time.get_ticks() / 1000)), True, (255, 255, 255))
        screen.blit(time, time_location)

    # Draw hits
    screen.blit(font.render('hits: ' + str(hits), True, tuple(hit_color)), hit_location)

    for b in bricks:
        screen.blit(brick, b)

    screen.blit(bat, bat_rect)

    screen.blit(ball, ball_rect)

    pygame.display.update()

    # Check for input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    pressed = pygame.key.get_pressed()

    if pressed[K_LEFT]:
        x -= 0.5 * speed_multiplier * dt
    if pressed[K_RIGHT]:
        x += 0.5 * speed_multiplier * dt
    if pressed[K_SPACE]:
        ball_served = True
        if not begin:
            begin = True

    # Ball and paddle collision
    if bat_rect[1] + bat_rect.height >= ball_rect[1] + ball_rect.height >= bat_rect[1] and \
            bat_rect[0] + bat_rect.width >= ball_rect[0] >= bat_rect[0] and \
            sy > 0:
        hits += 1
        hit_color = [0, 200, 0]
        sx *= speed_multiplier
        sy *= -speed_multiplier
        continue

    # Paddle and edge loop
    if x < -50:
        x = screen.get_width() - 50

    if x > screen.get_width() - 50:
        x = -50

    # Ball and brick collision
    delete_brick = None

    for b in bricks:
        bx, by = b
        # Clockwise from top left corner of ball
        if (bx + 2 <= ball_rect.x <= bx + brick_rect.width - 2 and
                by + 2 <= ball_rect.y <= by + brick_rect.height - 2) or \
            (bx + 2 <= ball_rect.x + ball_rect.width <= bx + brick_rect.width - 2 and
                by + 2 <= ball_rect.y <= by + brick_rect.height - 2) or \
            (bx + 2 <= ball_rect.x + ball_rect.width <= bx + brick_rect.width - 2 and
                by + 2<= ball_rect.y + ball_rect.height <= by + brick_rect.height - 2) or \
            (bx + 2 <= ball_rect.x <= bx + brick_rect.width - 2 and
                by + 2 <= ball_rect.y + ball_rect.height <= by + brick_rect.height - 2):
            delete_brick = b

            if bx + brick_rect.width - 2 >= ball_rect.x >= bx + 2 or \
                    bx + brick_rect.width - 2 >= ball_rect.x + ball_rect.width >= bx + 2:
                sy *= -1
            if by + brick_rect.height - 2 <= ball_rect.y <= by + 2 or \
                    by + brick_rect.height - 2 <= ball_rect.y + ball_rect.height <= by + 2:
                sx *= -1
            break

    if delete_brick is not None:
        bricks.remove(delete_brick)
        hits += 1
        hit_color = [0, 200, 0]

    # Ball against edges
    if ball_rect[1] <= 0:
        ball_rect[1] = 0
        sy *= -1
    if ball_rect[1] >= screen.get_height() - ball_rect.height:
        ball_rect[0], ball_rect[1] = (random.randint(100, screen.get_width() - 100), 250)
        sx, sy = ((random.randint(-1, 1) * 3.0 * speed_multiplier) + 1, 3.0 * speed_multiplier)
        hits -= 5
        hit_color = [200, 0, 0]
        ball_served = False
    if ball_rect[0] <= 0:
        ball_rect[0] = 0
        sx *= -1
    if ball_rect[0] >= screen.get_width() - ball_rect.width:
        ball_rect[0] = screen.get_width() - ball_rect.width
        sx *= -1

    bat_rect[0] = x

    if ball_served:
        ball_rect[0] += sx
        ball_rect[1] += sy

    # Color update
    for c in range(0, 3):
        if hit_color[c] <= 255:
            hit_color[c] += 7
            if hit_color[c] > 255:
                hit_color[c] = 255

pygame.quit()
