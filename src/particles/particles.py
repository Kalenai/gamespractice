"""

Much of the code here is heavily referenced from Peter Collingridge's tutorial on Pygame physics.
His tutorial can be at http://www.petercollingridge.co.uk/pygame-physics-simulation

"""

import sys
import math
import pygame
import random

# Color and Size Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
COLOR_KEY = (255, 0, 255)

FPS = 60
RESOLUTION = WINDOW_WIDTH, WINDOW_HEIGHT = (800, 600)

GRAVITY = (math.pi, 0.2)
DRAG = 0.999
ELASTICITY = 0.75


class Particle(pygame.sprite.Sprite):
    def __init__(self, size, x, y, speed, angle):
        super().__init__()
        self.size = size
        self.image = pygame.Surface([self.size * 2, self.size * 2])
        self.image.fill(COLOR_KEY)
        self.image.set_colorkey(COLOR_KEY)
        pygame.draw.circle(self.image, BLUE, (self.size, self.size), self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.angle = angle

    def reflect(self, axis):
        if axis == 'x':
            self.angle = - self.angle
        elif axis == 'y':
            self.angle = math.pi - self.angle
        self.speed *= ELASTICITY

    def add_vectors(self, angle2, speed2):
        x = math.sin(self.angle) * self.speed + math.sin(angle2) * speed2
        y = math.cos(self.angle) * self.speed + math.cos(angle2) * speed2
        speed = math.hypot(x, y)
        angle = math.pi / 2 - math.atan2(y, x)
        return angle, speed

    def update(self):
        self.angle, self.speed = self.add_vectors(GRAVITY[0], GRAVITY[1])
        self.speed *= DRAG

        self.rect.x += math.sin(self.angle) * self.speed
        self.rect.y -= math.cos(self.angle) * self.speed

        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.reflect('x')
        elif self.rect.left < 0:
            self.rect.left = 0
            self.reflect('x')

        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.reflect('y')
        elif self.rect.top < 0:
            self.rect.top = 0
            self.reflect('y')


pygame.init()
CLOCK = pygame.time.Clock()
DISPLAY_SURF = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Particles")


def main():
    all_sprites_list = pygame.sprite.Group()
    for n in range(1, 10):
        size = random.randint(10, 15)
        x = random.randint(0, WINDOW_WIDTH - size * 2)
        y = random.randint(0, WINDOW_HEIGHT - size * 2)
        speed = random.randint(3, 10)
        angle = random.uniform(0, 2 * math.pi)
        particle = Particle(size, x, y, speed, angle)
        all_sprites_list.add(particle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()

        DISPLAY_SURF.fill(WHITE)
        all_sprites_list.update()
        all_sprites_list.draw(DISPLAY_SURF)
        pygame.display.flip()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
