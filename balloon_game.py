import pygame
import random
from collections import namedtuple as nt

from pygame._sdl2.touch import *
global BALL_R
BALL_R = 50
BALL_TIMER = 750
SURFACE_R = BALL_R*4
WIDTH, HEIGHT = 1920, 1080

class Ball(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([SURFACE_R,SURFACE_R], pygame.SRCALPHA)
        pygame.draw.circle(self.image, "white", (SURFACE_R/2,SURFACE_R/2), BALL_R)
        self.rect = self.image.get_rect()
        self.move_delta = [8,8]
        self.base_speed = 8
        self.pos = [self.rect.x, self.rect.y]
        self.area = screen.get_rect()

        self.boost = 1.00
        self.timer = False

    def update(self):
        self.bounce_off_wall()

        self.rect = self.rect.move(self.move_delta)
        self.pos = (self.rect.x, self.rect.y)

    def bounce_off_wall(self):
        md = self.move_delta
        WB = nt('WallBounceFlags', ['top','bottom','left','right'])
        did_bounce = []
        ### bound check bottom ###
        if self.rect.bottom > self.area.bottom:
            self.move_delta = (self.move_delta[0], -self.move_delta[1])

        ### bound check top ###
        if self.rect.top < self.area.top:
            self.move_delta = (self.move_delta[0], -self.move_delta[1])

        ### bound check left ###
        if self.rect.left < self.area.left:
            self.move_delta = (-self.move_delta[0], self.move_delta[1])

        ### bound check right ###
        if self.rect.right > self.area.right:
            self.move_delta = (-self.move_delta[0], self.move_delta[1])

        return True if self.move_delta != md else False

    def on_click(self, pos):
        if self.rect.collidepoint(pos): self.on_hit(pos)
        #else: self.on_miss(pos)

    def on_hit(self, *args):
        if self.timer: return
        pygame.mouse.set_pos((0,0))
        self.image.fill("black")
        pygame.time.set_timer(MY_EVENT, BALL_TIMER)

        self.move_delta = (100, 100)
        self.timer=True

    def on_miss(self, *args):
        if self.timer: return
        global BALL_R
        if random.randint(0,3) % 3 == 0: BALL_R+=1
        self.image.fill("black")
        pygame.draw.circle(self.image, "white", (SURFACE_R/2,SURFACE_R/2), BALL_R)


    def on_timer_up(self):
        self.timer=False
        self.move_delta = (random.randint(-8,9), random.randint(-8,9))
        global BALL_R
        if random.randint(0,1): BALL_R -= 1
        else:
            self.boost += 0.08
            self.move_delta = (self.move_delta[0]*self.boost, self.move_delta[1]*self.boost)

        pygame.time.set_timer(MY_EVENT, 0)
        pygame.draw.circle(self.image, "white", (SURFACE_R/2,SURFACE_R/2), BALL_R)

running = True


pygame.init()
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
bg = pygame.Surface(screen.get_size())
pygame.mouse.set_visible(False)
#bg = bg.convert()
bg.fill("black")
screen.blit(bg, (0,0))

pygame.display.flip()

ball = Ball()
all_sprites = pygame.sprite.Group(ball, )
clock = pygame.Clock()

MY_EVENT = pygame.event.custom_type()

BALL_TIMER_BASE = 1
counter = BALL_TIMER_BASE


while running:

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            [c.on_click(event.pos) for c in all_sprites]

        if event.type == MY_EVENT:
            counter -= 1
            if counter <= 0:
                [c.on_timer_up() for c in all_sprites]
                counter = BALL_TIMER_BASE


    all_sprites.update()

    screen.blit(bg, (0,0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
