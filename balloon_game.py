import sys, pygame
import random

pygame.init()

size = width, height = 1920, 1080
speed = [1,1]

ball_r = 35

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

run_main = True

class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([ball_r*2 for _ in range(2)])
        screen = pygame.display.get_surface()
        pygame.draw.circle(self.image, center=(ball_r//2,ball_r//2))

        self.area = screen.get_rect()
        self.vector = vector

    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        self.rect = newpos

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
        return rect.move(dx,dy)

ball = Ball((1,1))

updates = [ball]

while run_main:

    pygame.time.delay(6)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run_main=False

    if event.type == pygame.MOUSEBUTTONDOWN:
        pass

    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    [x.update for x in updates]

    screen.fill("black")
    screen.blit(ball, ballrect)
    pygame.display.flip()
