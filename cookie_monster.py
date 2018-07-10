import pygame, sys, random

class Falling_Object(object):
    def __init__(self, screen_width, screen_height, item_type):
        self.size = 30
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.type = item_type
        self.x_pos = random.randint(0, self.screen_width - self.size) 
        self.y_pos = (0 - self.size)
        self.item_drop_speed = random.randint(1, 8)

    def update_y_position(self):
        self.y_pos += self.item_drop_speed

    def get_image(self):
        if self.type == 'cookie':
            return pygame.image.load('images/cookie3.png').convert_alpha()
        elif self.type == 'bomb':
            return pygame.image.load('images/bomb.png').convert_alpha()

    def render_image(self, screen):
        image = self.get_image()
        transformed_image = pygame.transform.scale(image, (self.size, self.size))
        image_rect = pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)
        screen.blit(transformed_image, image_rect)


def main():
    # declare the size of the canvas
    screen_width = 900
    screen_height = 700
    
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    game_clock = pygame.time.Clock()
    pygame.display.set_caption('Cookie Monster')

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


        screen.fill((gray))

        for item in falling_objects:
            item.render_image(screen)

        pygame.display.update()
        game_clock.tick(60)

    pygame.quit()
        
main()
