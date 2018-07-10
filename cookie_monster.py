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


class Player(object):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load('images/cookie_monster.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width / 2, screen_height - 100)
        self.score = 0
        self.top_score = 0

    def update_score(self, falling_item_hit):
        if falling_item_hit.item_type == 'cookie':
            self.score += 1
        else:
            if self.score > self.top_score:
                self.top_score = self.score
            self.score = 0
            

def main():
    # declare the size of the canvas
    screen_width = 900
    screen_height = 700
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    game_clock = pygame.time.Clock()
    pygame.display.set_caption('Cookie Monster')
    pygame.mouse.set_visible(False)

    # Set up colors
    blue = (0, 0, 255)
    gray = (128, 128, 128)

    cookie_monster = Player(screen_width, screen_height)
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
                cookie_monster.rect.move_ip(event.pos[0] - cookie_monster.rect.centerx, event.pos[1] - cookie_monster.rect.centery)


        if item_drop_counter == item_drop_rate:
            item_drop_counter = 0
            item_type = 'bomb'
            if random.randint(1, 3) == 1:
                item_type = 'cookie'
            falling_objects.append(Falling_Object(screen_width, screen_height, item_type))

        for falling_object in falling_objects[:]:
            falling_object.update_y_position()
            if falling_object.y_pos > screen_height:
                falling_objects.remove(falling_object)

            if cookie_monster.rect.colliderect(falling_object.image_rectangle()):
                # update score
                falling_objects.remove(falling_object)


        screen.fill((gray))
        
        # Draw the player's rectangle
        screen.blit(cookie_monster.image, cookie_monster.rect)
        
        # draw falling objects to screen
        for item in falling_objects:
            item.render_image(screen)
        
        pygame.display.update()
        game_clock.tick(60)

    pygame.quit()
        
main()
