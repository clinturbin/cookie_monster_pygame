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
FPS = 60
pygame.display.set_caption('Cookie Monster')

# Set up sounds
bomb_sound = pygame.mixer.Sound('images/bomb.wav')
eat_cookie_sound = pygame.mixer.Sound('images/cookie1.wav')
start_game_sound = pygame.mixer.Sound('images/cookies.wav')
hello_sound = pygame.mixer.Sound('images/hello.wav')
bye_sound = pygame.mixer.Sound('images/thank_you_bye.wav')
pygame.mixer.music.load('images/c_is_for_cookie_3.wav')

cookie_monster_player_img = pygame.image.load('images/cookie_monster.png').convert_alpha()
cookie_monster_start_img = pygame.image.load('images/cm1.png').convert_alpha()

font = pygame.font.Font('freesansbold.ttf', 20)
message_font = pygame.font.Font('freesansbold.ttf', 40)

LEVELS = {
            1:{'cookie_drop_rate': 50,
               'min_drop_speed': 1,
               'max_drop_speed': 6,
               'new_item_load_rate': 10,
               'next_level_score': 10},

            2:{'cookie_drop_rate': 40,
               'min_drop_speed': 3,
               'max_drop_speed': 12,
               'new_item_load_rate': 6,
               'next_level_score': 15},
            
            3:{'cookie_drop_rate': 30,
               'min_drop_speed': 6,
               'max_drop_speed': 14,
               'new_item_load_rate': 4,
               'next_level_score': 20}
}


class Falling_Object(object):
    def __init__(self, item_type, item_drop_speed):
        self.item_type = item_type
        self.item_drop_speed = item_drop_speed
        self.size = 30
        self.x_pos = random.randint(0, SCREEN_WIDTH - self.size)
        self.y_pos = (0 - self.size)

    def update_y_position(self):
        self.y_pos += self.item_drop_speed

    def get_image(self):
        if self.item_type == 'cookie':
            return pygame.image.load('images/cookie.png').convert_alpha()
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
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
        self.score = 0
        self.lives = 5
        self.level = 1

    def update_score(self, falling_item_hit):
        self.play_sound_effect(falling_item_hit)
        if falling_item_hit.item_type == 'cookie':
            self.score += 1
        else:
            self.score = 0
            self.decrease_lives()
        self.update_game_level()
        
    def play_sound_effect(self, falling_item_hit):
        if falling_item_hit.item_type == 'cookie':
            eat_cookie_sound.play()
        else:
            bomb_sound.play()

    def decrease_lives(self):
        self.lives -= 1
        if self.lives == 0:
            game_over("GAME OVER")

    def update_game_level(self):
        if self.score >=0 and self.score < LEVELS[1]['next_level_score']:
            self.level = 1
        if self.score >= LEVELS[1]['next_level_score'] and self.score < LEVELS[2]['next_level_score']:
            self.level = 2
        if self.score >= LEVELS[2]['next_level_score'] and self.score < LEVELS[3]['next_level_score']:
            self.level = 3
        if self.score >= LEVELS[3]['next_level_score']:
            game_over("YOU WIN!!!")

def quit_game():
    pygame.quit()
    sys.exit()    

def add_score_text(text, font, surface, x, y, color):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topright = (x, y)
    surface.blit(text_obj, text_rect)     

def load_screen():
    hello_sound.play()

    image = cookie_monster_start_img
    image_rect = image.get_rect()
    image_rect.bottom = (SCREEN_HEIGHT / 10) * 7
    image_rect.centerx = (SCREEN_WIDTH / 2)

    button = pygame.Rect(150, (SCREEN_HEIGHT / 10) * 7, (SCREEN_WIDTH / 10) * 6, 50)
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
                    start_game_sound.play()
                    sound_delay_counter = 0
                    while sound_delay_counter < (FPS * 2):
                        sound_delay_counter += 1
                        game_clock.tick(60)
                    done = True

        screen.fill((BLACK))
        screen.blit(image, image_rect)
        pygame.draw.rect(screen, BLUE, button)
        screen.blit(text_obj, text_rect)
        pygame.display.update()
        game_clock.tick(FPS)

def play_game():
    pygame.mixer.music.play(-1, 0.0)
    pygame.mouse.set_visible(False)

    player = Player(cookie_monster_player_img)
    falling_objects = []

    new_item_load_counter = 0

    level = 1

    done = False
    while not done:
        # current_level = player.level
        new_item_load_rate = LEVELS[player.level]['new_item_load_rate']
        new_item_load_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quit_game()

            if event.type == MOUSEMOTION:
                player.rect.move_ip(event.pos[0] - player.rect.centerx, event.pos[1] - player.rect.centery)

        if new_item_load_counter == new_item_load_rate:
            new_item_load_counter = 0
            item_drop_speed = random.randint(LEVELS[player.level]['min_drop_speed'], LEVELS[player.level]['max_drop_speed'])
            item_type = 'bomb'
            if random.randint(1, 100) <= LEVELS[player.level]['cookie_drop_rate']:
                item_type = 'cookie'
            falling_objects.append(Falling_Object(item_type, item_drop_speed))

        for falling_object in falling_objects[:]:
            falling_object.update_y_position()
            if falling_object.y_pos > SCREEN_HEIGHT:
                falling_objects.remove(falling_object)

            if player.rect.colliderect(falling_object.image_rectangle()):
                player.update_score(falling_object)
                falling_objects.remove(falling_object)

        # move the mouse cursor to match the player
        pygame.mouse.set_pos(player.rect.centerx, player.rect.centery)
        
        screen.fill((GRAY))
        
        # Draw the player's rectangle
        screen.blit(player.image, player.rect)
        
        # draw falling objects to screen
        for item in falling_objects:
            item.render_image(screen)
        
        # Add score and top score to the screen.
        add_score_text('Level: %s' % (player.level), font, screen, SCREEN_WIDTH - 30, 20, BLUE)
        add_score_text('Score: %s' % (player.score), font, screen, SCREEN_WIDTH - 30, 70, BLUE)
        add_score_text('Lives: %s' % (player.lives), font, screen, SCREEN_WIDTH - 30, 120, BLUE)

        pygame.display.update()
        game_clock.tick(FPS)

def game_over(message):
    pygame.mixer.music.stop()
    pygame.mouse.set_visible(True)

    game_over_message = message_font.render(message, 1, WHITE)
    game_over_message_rect = game_over_message.get_rect()
    game_over_message_rect.centerx = SCREEN_WIDTH / 2
    game_over_message_rect.top = 100

    btn_width = 200
    btn_height = 100
    
    play_again_btn = pygame.Rect((SCREEN_WIDTH/4) - (btn_width/2), (SCREEN_HEIGHT/2) - (btn_height/2), btn_width, btn_height)
    play_again_text_obj = font.render("PLAY AGAIN", 1, WHITE)
    play_again_text_rect = play_again_text_obj.get_rect()
    play_again_text_rect.center = play_again_btn.center

    quit_btn = pygame.Rect((SCREEN_WIDTH/4)*3 - (btn_width/2), (SCREEN_HEIGHT/2) - (btn_height/2), btn_width, btn_height)
    quit_text_obj = font.render("QUIT GAME", 1, WHITE)
    quit_text_rect = quit_text_obj.get_rect()
    quit_text_rect.center = quit_btn.center

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
                if play_again_btn.collidepoint(x, y):
                    play_game()
                if quit_btn.collidepoint(x, y):
                    bye_sound.play()
                    sound_delay_counter = 0
                    while sound_delay_counter < (FPS * 2):
                        sound_delay_counter += 1
                        game_clock.tick(60)
                    quit_game()

        screen.fill((BLUE))
        screen.blit(game_over_message, game_over_message_rect)
        pygame.draw.rect(screen, BLACK, play_again_btn)
        screen.blit(play_again_text_obj, play_again_text_rect)
        pygame.draw.rect(screen, BLACK, quit_btn)
        screen.blit(quit_text_obj, quit_text_rect)
        pygame.display.update()

def main():
    load_screen()
    play_game()

main()