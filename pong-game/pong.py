import pygame
import random
from pygame.locals import *

pygame.init()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, first_paddle: bool, width, height, pos_x, pos_y, speed, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.first_paddle = first_paddle
        self.speed = speed

    def update(self):
        keys = pygame.key.get_pressed()

        if self.first_paddle:
            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= self.speed
            elif keys[pygame.K_s] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed
        else:
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
            elif keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed

# Setting Screen sizes
WIDTH = 600
HEIGHT = 400

# Color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle variables
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 120
PADDLE_SPEED = 10

# Ball variables
BALL_SIZE = 20
BALL_SPEED = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()
pygame.display.set_caption("Pong Game!")

FONT_PATH = r"C:\Users\VELİ CİHAN\Downloads\press-start-2p-font\PressStart2P-vaV7.ttf"
font = pygame.font.Font(FONT_PATH, 64)

score1 = 0
score2 = 0

def random_speed(min_speed, max_speed):
    speed = [0, 0]
    speed[0] = random.randint(min_speed, max_speed)
    speed[1] = random.randint(min_speed, max_speed)
    return speed

speed = [0, 0]
speed = random_speed(5, BALL_SPEED)

first_paddle = Paddle(
    first_paddle=True,
    width=PADDLE_WIDTH,
    height=PADDLE_HEIGHT,
    pos_x=20,
    pos_y=0,
    speed=PADDLE_SPEED,
    color=WHITE
)
first_paddle.rect.centery = screen_rect.centery

second_paddle = Paddle(
    first_paddle=False,
    width=PADDLE_WIDTH,
    height=PADDLE_HEIGHT,
    pos_x=WIDTH - 20,
    pos_y=0,
    speed=PADDLE_SPEED,
    color=WHITE
)
second_paddle.rect.centery = screen_rect.centery

ball = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
ball.center = screen_rect.center

items = pygame.sprite.Group()
items.add(first_paddle)
items.add(second_paddle)

run = True

def reset_ball():
    speed = random_speed(5, BALL_SPEED)
    ball.center = screen_rect.center

def draw_window():
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT), 2)
    pygame.draw.circle(screen, WHITE, screen_rect.center, 100, 2)
    pygame.draw.circle(screen, WHITE, screen_rect.center, 5, 0)
    items.draw(screen)
    pygame.draw.rect(screen, WHITE, ball)
    screen.blit(score1_font, score1_rect)
    screen.blit(score2_font, score2_rect)
    items.update()  
    pygame.display.flip()

while run:
    pygame.time.delay(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    score1_font = font.render(str(score1), True, WHITE)
    score1_rect = score1_font.get_rect()
    score1_rect.center = (WIDTH/4, screen_rect.centery)

    score2_font = font.render(str(score2), True, WHITE)
    score2_rect = score1_font.get_rect()
    score2_rect.center = (WIDTH/4 * 3, screen_rect.centery)  

    ball = ball.move(speed)

    if ball.left < 0:
        reset_ball()
        score2 += 1

    if ball.right > WIDTH:
        reset_ball()
        score1 += 1

    if ball.top < 0 or ball.bottom > HEIGHT:
        speed[1] = -speed[1]
    
    if ball.colliderect(first_paddle.rect) or ball.colliderect(second_paddle.rect):
        speed[0] = -speed[0]

    draw_window()

pygame.quit()