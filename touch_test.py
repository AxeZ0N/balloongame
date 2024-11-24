import pygame
from pygame._sdl2.touch import *

fingers = lambda: [x for x in [get_finger(10,fnum) for fnum in range(5)] if x is not None]

class Main:

    def main(self):
        pygame.init()
        self.screen = pygame.display.set_mode((720,512))
        self.bg = pygame.Surface(self.screen.get_size())
        pygame.mouse.set_visible(False)
        self.bg.fill("black")
        self.screen.blit(self.bg, (0,0))

        pygame.display.flip()

        self.my_cokes = [Coke() for _ in range(1)]

        self.all_sprites = pygame.sprite.Group(self.my_cokes[-1])
        self.clock = pygame.Clock()
        self.running = True

        self.last_finger = len(fingers())

        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False

                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                    if (fnum := len(fingers())) != self.last_finger:
                        self.last_finger = fnum
                        event.pos = fingers()[-1]
                    [s.on_click(event) for s in self.all_sprites]


        self.screen.blit(bg, (0,0))

        pygame.display.flip()


class Coke(pygame.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        self.COKE_RING = 25

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([self.COKE_RING,self.COKE_RING],
                                            pygame.SRCALPHA)
        pygame.draw.circle(self.image, "white", 
                           (self.COKE_RING/2,self.COKE_RING/2), self.COKE_RING/4)

        self.rect = self.image.get_rect()

    def on_click(self, event):
        print(event.pos)

if __name__=='__main__':
    Main().main()
    pygame.quit()
