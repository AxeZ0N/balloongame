import sys, pygame
import random

pygame.init()

size = width, height = 1920, 1080
speed = [10, 10]
gray = 0,0,0

running = True
ball_r = 25

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

#ball = pygame.image.load("intro_ball.gif")

ball = pygame.Surface((ball_r*2, ball_r*2), pygame.SRCALPHA)
pygame.draw.circle(ball, (255,255,255), (ball.width // 2, ball.height // 2), ball_r)
ballrect = ball.get_rect()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    pygame.time.delay(10)

    ballrect = ballrect.move(speed)
    s = random.randint(0,1) * 100
    print(s)
    if ballrect.left < 0 or ballrect.right > width:
        #speed[0] = -speed[0]
        speed[0] = -s
    s = random.randint(0,1) * 100
    if ballrect.top < 0 or ballrect.bottom > height:
        #speed[1] = -speed[1]
        speed[0] = -s

    screen.fill(gray)
    screen.blit(ball, ballrect)
    pygame.display.flip()
