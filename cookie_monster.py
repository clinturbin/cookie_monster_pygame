import pygame, sys, random
from pygame.locals import *

class Cookie(object):
    def __init__(self, screen_width, screen_height):
        self.size = 30
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x_pos = random.randint(0, self.screen_width - self.size) 
        self.y_pos = (0 - self.size)
        self.item_drop_speed = random.randint(1, 8)

    def update_y_position(self):
        self.y_pos += self.item_drop_speed

    def render_image(self, screen):
        image = pygame.image.load('images/cookie3.png').convert_alpha()
        transformed_image = pygame.transform.scale(image, (self.size, self.size))
        image_rect = pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)
        screen.blit(transformed_image, image_rect)


def main():
    # declare the size of the canvas
    screen_width = 900
    screen_height = 700
    
    # Set up colors
    blue = (0, 0, 255)
    gray = (128, 128, 128)

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    game_clock = pygame.time.Clock()
    pygame.display.set_caption('Cookie Monster')

    cookies = []

    item_drop_rate = 10
    item_drop_counter = 0

    done = False
    while not done:
        item_drop_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if item_drop_counter == item_drop_rate:
            item_drop_counter = 0
            cookies.append(Cookie(screen_width, screen_height))

        for cookie in cookies[:]:
            cookie.update_y_position()
            if cookie.y_pos > screen_height:
                cookies.remove(cookie)


        screen.fill((gray))

        for cookie in cookies:
            cookie.render_image(screen)

        pygame.display.update()
        game_clock.tick(60)

    pygame.quit()
        
main()
