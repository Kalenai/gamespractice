import pygame
import random
import sys
from pygame import *

# Color and Size Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60
RESOLUTION = WINDOW_WIDTH, WINDOW_HEIGHT = (600, 600)
CENTER_WIDTH = 20
CENTER = ((WINDOW_WIDTH / 2) - CENTER_WIDTH / 2, (WINDOW_HEIGHT / 2) - CENTER_WIDTH / 2)

# Initializations
pygame.init()
FPS_CLOCK = pygame.time.Clock()
DISPLAY_SURF = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Spear Defense!")
font = pygame.font.Font(None, 28)
shield_sound = pygame.mixer.Sound("assets/shieldhit.wav")
hit_sound = pygame.mixer.Sound("assets/playerhit.wav")
SPEAR_EVENT = pygame.USEREVENT + 1


# Sprite Classes
class Player(pygame.sprite.Sprite):
    """ The class for the player """

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([CENTER_WIDTH, CENTER_WIDTH])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()


class Shield(pygame.sprite.Sprite):
    """ The class for the player's shield. """

    def __init__(self, direction):
        super().__init__()
        self.direction = direction

        self.image = None
        self.set_image()
        self.rect = None
        self.set_rect()

    def set_image(self):
        if self.direction == 'right' or self.direction == 'left':
            self.image = pygame.Surface([CENTER_WIDTH / 2, CENTER_WIDTH])
        elif self.direction == 'up' or self.direction == 'down':
            self.image = pygame.Surface([CENTER_WIDTH, CENTER_WIDTH / 2])
        self.image.fill(WHITE)

    def set_rect(self):
        self.rect = self.image.get_rect()

    def set_direction(self, direction):
        self.direction = direction

    def update(self):
        self.set_image()
        self.set_rect()

        if self.direction == 'right':
            self.rect.x, self.rect.y = CENTER[0] + 30, CENTER[1]
        elif self.direction == 'left':
            self.rect.x, self.rect.y = CENTER[0] - 20, CENTER[1]
        elif self.direction == 'up':
            self.rect.x, self.rect.y = CENTER[1], CENTER[0] - 20
        elif self.direction == 'down':
            self.rect.x, self.rect.y = CENTER[1], CENTER[0] + 30


class Spear(pygame.sprite.Sprite):
    """ The class for the incoming spears. """

    def __init__(self, origin):
        super().__init__()

        self.origin = origin
        if origin == 'left' or origin == 'right':
            self.image = pygame.Surface([30, 10])
        elif origin == 'up' or origin == 'down':
            self.image = pygame.Surface([10, 30])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        if self.origin == 'left':
            self.rect.x += 5
        elif self.origin == 'up':
            self.rect.y += 5
        elif self.origin == 'right':
            self.rect.x -= 5
        elif self.origin == 'down':
            self.rect.y -= 5

# Direction Constants
RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'

# Lists of sprites
all_sprites_list = pygame.sprite.Group()
spear_list = pygame.sprite.Group()


def main():
    global FPS, DISPLAY_SURF
    start_screen()


def start_screen():
    """ Shows the player a 'start' splash screen with an option to start the game """
    title_font = pygame.font.Font(None, 124)
    info_font = pygame.font.Font(None, 28)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    all_sprites_list.empty()
                    spear_list.empty()
                    play_game()
                elif event.key == K_ESCAPE:
                    exit_game()

        title_str = ["Spear", "Defense!"]
        info_str = "Press 'Space' to start"

        DISPLAY_SURF.fill(BLACK)

        title_text = title_font.render(title_str[0], True, WHITE)
        DISPLAY_SURF.blit(title_text, [80, title_font.size(title_str[0])[1]])

        title_text = title_font.render(title_str[1], True, WHITE)
        DISPLAY_SURF.blit(title_text, [160, title_font.size(title_str[1])[1] * 2.2])

        info_text = info_font.render(info_str, True, WHITE)
        DISPLAY_SURF.blit(info_text, [(WINDOW_WIDTH / 2) - (info_font.size(info_str)[0] / 2), WINDOW_HEIGHT - info_font.size(info_str)[1] * 6])

        pygame.display.flip()
        FPS_CLOCK.tick(FPS)


def play_game():
    """ Initializes and runs the main gameplay """
    # Initialize the player class
    player = Player()
    player.rect.x = (WINDOW_WIDTH / 2) - (CENTER_WIDTH / 2)
    player.rect.y = (WINDOW_HEIGHT / 2) - (CENTER_WIDTH / 2)
    all_sprites_list.add(player)

    # Initialize the player's shield class, score, life total, and the spear timer
    shield = Shield(RIGHT)
    all_sprites_list.add(shield)

    direction = RIGHT
    score = 0
    life = 3

    fire_spear = False
    spear_timing = 300
    pygame.time.set_timer(SPEAR_EVENT, spear_timing)

    # Main game loop
    while True:
        # Listen for events
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            elif event.type == KEYDOWN:
                if (event.key == K_RIGHT or event.key == K_d) and direction != RIGHT:
                    direction = RIGHT
                elif (event.key == K_LEFT or event.key == K_a) and direction != LEFT:
                    direction = LEFT
                elif (event.key == K_UP or event.key == K_w) and direction != UP:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != DOWN:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    exit_game()
            if event.type == SPEAR_EVENT:
                fire_spear = True

        # Change the shield direction and update sprites
        shield.set_direction(direction)
        all_sprites_list.update()

        # Count spears blocked and increment the score
        spears_blocked_list = pygame.sprite.spritecollide(shield, spear_list, True)
        if spears_blocked_list:
            shield_sound.play()
        for block in spears_blocked_list:
            score += 1

        # Count player hits and decrement life total
        player_hit_list = pygame.sprite.spritecollide(player, spear_list, True)
        if player_hit_list:
            hit_sound.play()
        for hit in player_hit_list:
            life -= 1

        # Check if the player's life is zero
        if life <= 0:
            game_over_screen(score)

        # Set up text to render
        score_text = "Score: {0}".format(score)
        life_text = "Life: {0}/3".format(life)
        text_height = 15

        # Update the screen and draw new sprites as needed
        DISPLAY_SURF.fill(BLACK)

        text = font.render(score_text, True, WHITE)
        DISPLAY_SURF.blit(text, [15, text_height])

        text = font.render(life_text, True, WHITE)
        DISPLAY_SURF.blit(text, [WINDOW_WIDTH - font.size(life_text)[0] - 15, text_height])

        if fire_spear:
            create_spear()
            fire_spear = False
            spear_timing = random.randrange(200, 500)
            pygame.time.set_timer(SPEAR_EVENT, spear_timing)

        all_sprites_list.draw(DISPLAY_SURF)

        pygame.display.flip()
        FPS_CLOCK.tick(FPS)


def game_over_screen(score):
    """ Shows the player a 'game over' screen, with options to quit or restart """
    # Screen loop
    while True:
        # Event Loop
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    all_sprites_list.empty()
                    spear_list.empty()
                    play_game()
                elif event.key == K_ESCAPE:
                    exit_game()

        # Draw text and update the screen
        output_str = [
            "Game over.",
            "Your score was: {0}".format(score),
            "Press 'Space' to play again.",
            "Press 'Esc' to exit."
        ]
        text_height = WINDOW_HEIGHT / 2.5
        DISPLAY_SURF.fill(BLACK)
        for line in output_str:
            text = font.render(line, True, WHITE)
            DISPLAY_SURF.blit(text, [(WINDOW_WIDTH / 2) - (font.size(line)[0] / 2), text_height])
            text_height += 30
        pygame.display.flip()
        FPS_CLOCK.tick(FPS)


def create_spear():
    """ Fire a spear from a random direction. """
    chance = random.random()
    if 0 <= chance < 0.25:
        spear = Spear('left')
        spear.rect.x = 0
        spear.rect.y = WINDOW_HEIGHT / 2 - 5
    elif 0.25 <= chance < 0.5:
        spear = Spear('up')
        spear.rect.x = WINDOW_WIDTH / 2 - 5
        spear.rect.y = 0
    elif 0.5 <= chance < 0.75:
        spear = Spear('right')
        spear.rect.x = WINDOW_WIDTH - 30
        spear.rect.y = WINDOW_HEIGHT / 2 - 5
    else:
        spear = Spear('down')
        spear.rect.x = WINDOW_WIDTH / 2 - 5
        spear.rect.y = WINDOW_HEIGHT - 30
    all_sprites_list.add(spear)
    spear_list.add(spear)


def exit_game():
    """ Exits the game. """
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
