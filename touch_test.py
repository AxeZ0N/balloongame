import pygame
import random
from dataclasses import dataclass
from pygame._sdl2.touch import *
from pygame.math import Vector2 as Vec

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
        self.vel = Vec(5,5)
        self.move_delta = (self.vel.x,self.vel.y)

        self.curr_color = "white"

        self.BALL = 75
        self.radius = self.BALL
        self.image = pygame.Surface([self.BALL * 2, self.BALL * 2], pygame.SRCALPHA)

        self.draw_()

        self.rect = self.image.get_rect()
        self.area = screen.get_rect()

    def draw_(self):
        pygame.draw.circle(self.image,
                           self.curr_color,
                           (self.BALL,
                            self.BALL),
                           self.BALL)

        pygame.draw.rect(self.image,
                         'black',
                         pygame.Rect(self.BALL,-self.BALL-3, 3, self.BALL*4))

        pygame.draw.rect(self.image,
                         'black',
                         pygame.Rect(-self.BALL-3,self.BALL, self.BALL*4, 3))

    def clean(self):
        pygame.draw.circle(self.image, pygame.SRCALPHA, (self.BALL, self.BALL), self.BALL)

    def update(self):
        ### bound check bottom ###
        ### bound check top ###
        if self.rect.bottom > self.area.bottom or self.rect.top < self.area.top:
            self.vel = self.vel.reflect(Vec(0,1))

        ### bound check left ###
        ### bound check right ###
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.vel = self.vel.reflect(Vec(1,0))
    
        self.collide()

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

    def move_ball(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

    def collide(self,event=False):
        for p in paws():
            if pygame.sprite.collide_circle(p,self):
                if p.rect.x - self.rect.x > 0 and p.rect.y - self.rect.y > 0:
                    self.vel = self.vel.reflect(Vec(0,0))

                if p.rect.x - self.rect.x > 0 and p.rect.y - self.rect.y < 0:
                    self.vel = self.vel.reflect(Vec(1,1))

                if p.rect.x - self.rect.x > 0 and p.rect.y - self.rect.y > 0:
                    self.vel = self.vel.reflect(Vec(1,1))

                if p.rect.x - self.rect.x > 0 and p.rect.y - self.rect.y < 0:
                    self.vel = self.vel.reflect(Vec(1,1))

                self.rect.x *= 1.1
                self.rect.y *= 1.1


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
screen = pygame.display.set_mode(size)
#size = (1920,1080)
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.add(Paw())
        if event.type == pygame.MOUSEBUTTONUP:
            all_sprites.remove(Paw())

        [s.collide(pygame.mouse.get_pos()) for s in all_sprites]


    all_sprites.update()

    screen.blit(bg, (0,0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
