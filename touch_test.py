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

def bounce(paw, ball):
    v1 = pygame.math.Vector2(paw.rect.center)
    v2 = pygame.math.Vector2(ball.rect.center)
    r1 = paw.rect.width // 2
    r2 = ball.rect.width // 2
    d = v1.distance_to(v2)
    if d < r1 + r2 - 2:
        dnext = (v1).distance_to(v2 + ball.vel)
        nv = v2 - v1
        if dnext < d and nv.length() > 0:
            #paw.vel = paw.vel.reflect(nv)
            ball.vel = ball.vel.reflect(nv)
            ball.vel *= 1.01

        else:
            if ball.vel.magnitude() < Vec(8,8).magnitude():
                ball.vel *= 2
            else:
                ball.vel = Vec(8,8)


colors = ['red','orange','yellow','green','blue','indigo','violet']

class Ball(pygame.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.vel = Vec(5,5)
        self.move_delta = (self.vel.x,self.vel.y)
        self.SPLAT = False
        self.MAX_SPEED_VECTOR = kwargs.get("MAX_SPEED_VECTOR", Vec(8,8).magnitude())

        self.curr_color = "white"

        self.BALL_R = kwargs.get('BALL_R', None)
        self.BALL = self.BALL_R if self.BALL_R is not None else 75
        self.radius = self.BALL
        self.image = pygame.Surface([self.BALL * 2, self.BALL * 2], pygame.SRCALPHA)

        self.draw_()

        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.end_ticks = 0

    def draw_(self):
        pygame.draw.circle(self.image,
                           self.curr_color,
                           (self.BALL,
                            self.BALL),
                           self.BALL)

        pygame.draw.rect(self.image,
                         'black',
                         pygame.Rect(self.BALL,-self.BALL-5, 5, self.BALL*4))

        pygame.draw.rect(self.image,
                         'black',
                         pygame.Rect(-self.BALL-5,self.BALL, self.BALL*4, 5))

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

        self.move_ball()

    def move_ball(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        if self.vel.magnitude() > self.MAX_SPEED_VECTOR:
            self.vel *= 0.96

    def collide(self,event=None):
        for p in paws():
            if pygame.sprite.collide_circle(p,self):
                bounce(p,self)


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
#size = (720,512)
#screen = pygame.display.set_mode(size)
size = (1920,1080)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
bg = pygame.Surface(screen.get_size())
pygame.mouse.set_visible(False)
bg.fill("black")
screen.blit(bg, (0,0))

pygame.display.flip()


cokes = [Paw(index=x) for x in range(5)]
balls = [Ball(MAX_SPEED_VECTOR=Vec(7,7).magnitude(), BALL_R=150) for _ in range(1)]
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
