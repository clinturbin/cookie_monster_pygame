import pygame, sys, random
from pygame.locals import *

class Falling_Object(object):
    def __init__(self, screen_width, screen_height, item_type):
        self.size = 30
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.item_type = item_type
        self.x_pos = random.randint(0, self.screen_width - self.size) 
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


def main():
    # declare the size of the canvas
    screen_width = 900
    screen_height = 700
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    game_clock = pygame.time.Clock()
    pygame.display.set_caption('Cookie Monster')
    pygame.mouse.set_visible(False)

    # set up the player image
    player_image = pygame.image.load('images/cookie_monster.png').convert_alpha()
    player_rect = player_image.get_rect()
    player_rect.topleft = (screen_width / 2, screen_height - 100)

    # Set up colors
    blue = (0, 0, 255)
    gray = (128, 128, 128)

    falling_objects = []

    item_drop_rate = 10
    item_drop_counter = 0

    done = False
    while not done:
        item_drop_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    done = True

            if event.type == MOUSEMOTION:
                player_rect.move_ip(event.pos[0] - player_rect.centerx, event.pos[1] - player_rect.centery)


        if item_drop_counter == item_drop_rate:
            item_drop_counter = 0
            item_type = 'bomb'
            if random.randint(1, 3) == 1:
                item_type = 'cookie'
            falling_objects.append(Falling_Object(screen_width, screen_height, item_type))

        for item in falling_objects[:]:
            item.update_y_position()
            if item.y_pos > screen_height:
                falling_objects.remove(item)

            if player_rect.colliderect(item.image_rectangle()):
                falling_objects.remove(item)


        screen.fill((gray))
        # Draw the player's rectangle
        screen.blit(player_image, player_rect)
        # draw falling objects to screen
        for item in falling_objects:
            item.render_image(screen)
        pygame.display.update()
        game_clock.tick(60)

    pygame.quit()
        
main()
