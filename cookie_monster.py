import pygame, sys, random
from pygame.locals import *

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_clock = pygame.time.Clock()
pygame.display.set_caption('Cookie Monster')
# pygame.mouse.set_visible(False)

font = pygame.font.Font('freesansbold.ttf', 20)

class Falling_Object(object):
    def __init__(self, item_type):
        self.size = 30
        self.item_type = item_type
        self.x_pos = random.randint(0, SCREEN_WIDTH - self.size) 
        self.y_pos = (0 - self.size)
        self.item_drop_speed = random.randint(1, 8)

    def update_y_position(self):
        self.y_pos += self.item_drop_speed

    def get_image(self):
        if self.item_type == 'cookie':
            return pygame.image.load('images/cookie3.png').convert_alpha()
        elif self.item_type == 'bomb':
            return pygame.image.load('images/bomb.png').convert_alpha()

    def transform_image_size(self):
        image = self.get_image()
        transformed_image = pygame.transform.scale(image, (self.size, self.size))
        return transformed_image

    def image_rectangle(self):
        return pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)

    def render_image(self, screen):
        image = self.get_image()
        transformed_image = self.transform_image_size()
        image_rect = self.image_rectangle()
        screen.blit(transformed_image, image_rect)

class Player(object):
    def __init__(self):
        self.image = pygame.image.load('images/cookie_monster.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
        self.score = 0
        self.top_score = 0

    def update_score(self, falling_item_hit):
        if falling_item_hit.item_type == 'cookie':
            self.increase_score()
        else:
            self.reset_score()
    
    def increase_score(self):
        self.score += 1
    
    def reset_score(self):
        if self.score > self.top_score:
            self.top_score = self.score
        self.score = 0
    

def quit_game():
    pygame.quit()
    sys.exit()    

def add_text(text, font, surface, x, y, color):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topright = (x, y)
    surface.blit(text_obj, text_rect)     

def load_screen():
    button = pygame.draw.rect(screen, BLUE, (350, SCREEN_HEIGHT / 2, 100, 50))
    text_obj = font.render("PLAY!!", 1, WHITE)
    text_rect = text_obj.get_rect()
    text_rect.center = button.center

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button.collidepoint(x, y):
                    done = True

        screen.fill((BLACK))
        pygame.draw.rect(screen, BLUE, button)
        screen.blit(text_obj, text_rect)
        pygame.display.update()


def play_game():
    pygame.mouse.set_visible(False)
    cookie_monster = Player()
    falling_objects = []

    item_drop_rate = 10
    item_drop_counter = 0

    done = False
    while not done:
        item_drop_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quit_game()

            if event.type == MOUSEMOTION:
                cookie_monster.rect.move_ip(event.pos[0] - cookie_monster.rect.centerx, event.pos[1] - cookie_monster.rect.centery)


        if item_drop_counter == item_drop_rate:
            item_drop_counter = 0
            item_type = 'bomb'
            if random.randint(1, 3) == 1:
                item_type = 'cookie'
            falling_objects.append(Falling_Object(item_type))

        for falling_object in falling_objects[:]:
            falling_object.update_y_position()
            if falling_object.y_pos > SCREEN_HEIGHT:
                falling_objects.remove(falling_object)

            if cookie_monster.rect.colliderect(falling_object.image_rectangle()):
                cookie_monster.update_score(falling_object)
                falling_objects.remove(falling_object)


        screen.fill((GRAY))
        
        # Draw the player's rectangle
        screen.blit(cookie_monster.image, cookie_monster.rect)
        
        # draw falling objects to screen
        for item in falling_objects:
            item.render_image(screen)
        
        # Add score and top score to the screen.
        add_text('Top Score: %s' % (cookie_monster.top_score), font, screen, SCREEN_WIDTH - 30, 20, BLUE)
        add_text('Score: %s' % (cookie_monster.score), font, screen, SCREEN_WIDTH - 30, 70, BLUE)

        pygame.display.update()
        game_clock.tick(60)


def main():
    load_screen()
    play_game()

main()
