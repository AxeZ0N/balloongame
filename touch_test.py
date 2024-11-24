import pygame
import random
from pygame._sdl2.touch import *

paws = lambda: [get_finger(10,fnum) for fnum in range(5)]
colors = ['red','orange','yellow','green','blue','indigo','violet']
print(colors)

class Paw(pygame.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.index = kwargs.get('index',None)

        self.curr_color = colors.pop(0)
        colors.append(self.curr_color)

        self.RING = 20
        self.image = pygame.Surface([self.RING * 2, self.RING * 2], pygame.SRCALPHA)

        self.draw_()

        self.rect = self.image.get_rect()

    def draw_(self):
        pygame.draw.circle(self.image, self.curr_color, (self.RING, self.RING), self.RING)


    def clean(self):
        pygame.draw.circle(self.image, pygame.SRCALPHA, (self.RING, self.RING), self.RING)


    def update(self):
        try:
            paw = paws()[self.index]
            self.draw_()
            self.rect.x = paw['x'] * size[0] - self.RING * 1.6
            self.rect.y = paw['y'] * size[1] - self.RING * 2

        except TypeError as e:
            self.clean()



pygame.init()
size = (720,512)
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
bg = pygame.Surface(screen.get_size())
pygame.mouse.set_visible(False)
bg.fill("black")
screen.blit(bg, (0,0))

pygame.display.flip()


cokes = [Paw(index=_) for _ in range(5)]
all_sprites = pygame.sprite.Group(cokes)
clock = pygame.Clock()
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN: all_sprites.add(Paw())
        if event.type == pygame.MOUSEBUTTONUP: all_sprites.remove(Paw())

    all_sprites.update()

    screen.blit(bg, (0,0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
