import pygame
from pygame._sdl2.touch import *

fingers = lambda: [get_finger(10,fnum) for fnum in range(5)]

class Coke(pygame.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.index = kwargs.get('index',None)

        self.RING = 45
        self.R = self.RING * 2
        self.image = pygame.Surface([self.RING * 2, self.RING * 2], pygame.SRCALPHA)

        pygame.draw.circle(self.image, "white", (self.RING, self.RING), self.RING)

        self.rect = self.image.get_rect()

    def update(self):
        if self.index is not None:
            f = fingers()[self.index]
            self.rect.x = f['x'] * 720 - self.RING * 1.4
            self.rect.y = f['y'] * 512 - self.RING * 1.4 



pygame.init()
size = (720,512)
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
bg = pygame.Surface(screen.get_size())
pygame.mouse.set_visible(False)
bg.fill("black")
screen.blit(bg, (0,0))

pygame.display.flip()


cokes = [Coke() for _ in range(5)]
all_sprites = pygame.sprite.Group(cokes)
clock = pygame.Clock()
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN: all_sprites.add(Coke())
        if event.type == pygame.MOUSEBUTTONUP: all_sprites.remove(Coke())

    all_sprites.update()
    update_fingers()

    screen.blit(bg, (0,0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
