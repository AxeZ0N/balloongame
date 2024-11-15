import sys, pygame
pygame.init()

size = width, height = 1920, 1080
speed = [2, 2]
gray = 100, 100, 100

screen = pygame.display.set_mode(size)

#ball = pygame.image.load("intro_ball.gif")


player_pos = (500,500)

ball = pygame.Surface((10,10), pygame.SRCALPHA)
pygame.draw.circle(ball, "maroon", (ball.width // 2, ball.height // 2), 10)
ballrect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    pygame.time.delay(10)

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(gray)
    screen.blit(ball, ballrect)
    pygame.display.flip()
