import pygame
import random
from dataclasses import dataclass
from pygame._sdl2.touch import *

def paws():
    get_paws = lambda: [get_finger(10,fnum) for fnum in range(5)]

    @dataclass
    class paws:
        id: int
        x: int
        y: int
        pressure: int
        radius: int = 20

        def __post_init__(self):
            self.x = self.x * size[0] - self.radius
            self.y = self.y * size[1] - self.radius
            self.rect = pygame.rect.Rect(self.x,self.y,self.radius,self.radius)

    return  [paws(*p.values()) for p in get_paws() if p is not None]


colors = ['red','orange','yellow','green','blue','indigo','violet']


class Ball(pygame.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.curr_color = "white"

        self.BALL = 75
        self.radius = self.BALL
        self.image = pygame.Surface([self.BALL * 2, self.BALL * 2], pygame.SRCALPHA)

        self.draw_()
        self.move_delta = (5,5)

        self.rect = self.image.get_rect()
        self.area = screen.get_rect()

    def draw_(self):
        pygame.draw.circle(self.image, self.curr_color, (self.BALL, self.BALL), self.BALL)

    def clean(self):
        pygame.draw.circle(self.image, pygame.SRCALPHA, (self.BALL, self.BALL), self.BALL)

    def update(self):
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

        self.rect = self.rect.move(self.move_delta)

    def collide(self,event):
        for p in paws():
            if pygame.sprite.collide_circle(p,self):
                if self.rect.x > event.pos[0] and self.rect.y < event.pos[1]:
                    self.move_delta = (self.move_delta[0], -self.move_delta[1])


class Paw(pygame.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.index = kwargs.get('index',None)

        self.curr_color = colors.pop(0)
        colors.append(self.curr_color)

        self.RING = 20
        self.radius = self.RING
        self.image = pygame.Surface([self.RING * 2, self.RING * 2], pygame.SRCALPHA)

        self.clean()

        self.rect = self.image.get_rect()

    def draw_(self):
        pygame.draw.circle(self.image,
                           self.curr_color,
                           (self.RING, self.RING),
                           self.RING)

    def clean(self):
        pygame.draw.circle(self.image,
                           pygame.SRCALPHA,
                           (self.RING, self.RING),
                           self.RING)

    def update(self):
        try:
            paw = paws()[self.index]
            self.draw_()
            self.rect.x = paw.x
            self.rect.y = paw.y

        except (TypeError, IndexError) as e:
            self.clean()

    def collide(self, event):
        pygame.draw.circle(
                self.image,
                self.curr_color,
                (self.RING,self.RING),
                self.RING)



pygame.init()
size = (720,512)
#screen = pygame.display.set_mode(size)
#size = (1920,1080)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
bg = pygame.Surface(screen.get_size())
pygame.mouse.set_visible(False)
bg.fill("black")
screen.blit(bg, (0,0))

pygame.display.flip()


cokes = [Paw(index=x) for x in range(5)]
balls = [Ball() for _ in range(1)]
all_sprites = pygame.sprite.Group(cokes, balls)
clock = pygame.Clock()
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN: all_sprites.add(Paw())
        if event.type == pygame.MOUSEBUTTONUP: all_sprites.remove(Paw())
        if event.type == pygame.MOUSEMOTION or \
                event.type == pygame.MOUSEBUTTONDOWN: 
                    [p.collide(event) for p in all_sprites]


    all_sprites.update()

    screen.blit(bg, (0,0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
