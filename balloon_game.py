import sys, pygame
import random

pygame.init()

size = width, height = 1920, 1080
start_speed = 1
speed = [start_speed, start_speed]

ball_r = 35

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

ball = pygame.Surface((ball_r*2, ball_r*2), pygame.SRCALPHA)
pygame.draw.circle(ball, "white", (ball.width // 2, ball.height // 2), ball_r)
ballrect = ball.get_rect()

main_loop_running = True

running_away=False
tick=0
tick_time=4

def ball_collide():
    mouse_pos = pygame.mouse.get_pos()
return ballrect.collidepoint(mouse_pos)

while main_loop_running:

    pygame.time.delay(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: main_loop_running=False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if ball_collide(): running_away=True

        if running_away:
            print(tick)
            if tick == 0:
                speed[0] *= -10
                speed[1] *= -10
                tick=0

            elif tick >= tick_time:
                running_away=False
                tick=0 
                speed[0] *= .95
                speed[1] *= .95
            else:
                tick+=1

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill("black")
    screen.blit(ball, ballrect)
    pygame.display.flip()
