import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#,pygame.FULLSCREEN)

# Colors
WHITE = (255, 255, 255)
RED = (255,0,0)

# Score variable
score = 0
font = pygame.font.Font('thefont.ttf', 48)

pygame.mixer.music.load('background_start.mp3')  # Load the background music
pygame.mixer.music.play(-1)  # Play the music infinitely
shooting_sound = pygame.mixer.Sound('fire.mp3')  # Load the shooting sound

# Load sprite sheets (replace with your actual sprite sheet paths)
# enemy_spritesheet = pygame.image.load('pacmitya1.png').convert_alpha()
background = pygame.image.load('background.jpg').convert()

# Sprite dimensions
SPRITE_WIDTH = 287
SPRITE_HEIGHT = 477

# Background
bg_x1 = 0
bg_x2 = background.get_width()
bg_speed = 2

# Main character class
class MainCharacter(pygame.sprite.Sprite):
    def __init__(self,base='ivanus'):
        super().__init__()
        self.spritesheet = pygame.image.load(f'{base}.png').convert_alpha()
        self.shoot_image = pygame.image.load(f'{base}_fire.png').convert_alpha()
        self.images = []
        self.shoot_time = 0
        for i in range(3):  # Assuming 4 frames in the sprite sheet
            img = self.spritesheet.subsurface(i*SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - SPRITE_HEIGHT - 10
        self.frame = 0
        self.shooting = False

    def update(self):
        if self.shoot_time>0:
            self.shoot_time -= 1
        else:
            self.frame += 1
            self.image = self.images[self.frame % len(self.images)]

    def shoot(self):
        shooting_sound.play()
        self.image = self.shoot_image
        self.shoot_time = 5
        bullet = Bullet(self.rect.x + self.rect.width, self.rect.y + self.rect.height / 1.5)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [
            pygame.image.load(f'pacmitya1.png').convert_alpha(),
            pygame.image.load(f'pacmitya2.png').convert_alpha(),
            pygame.image.load(f'pacmitya2.png').convert_alpha(),
            ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SPRITE_HEIGHT)
        self.frame = 0

    def update(self):
        self.frame += 1
        #print(self.frame % len(self.images))
        self.image = self.images[self.frame % len(self.images)]
        self.rect.x -= 5
        if self.rect.x < -SPRITE_WIDTH:
            self.kill()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += 10
        if self.rect.x > SCREEN_WIDTH:
            self.kill()



# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create main character
main_character = MainCharacter(base='girl')
all_sprites.add(main_character)

# Clock and game loop
clock = pygame.time.Clock()
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('background.mp3')  # Load the background music
                pygame.mixer.music.play(-1)  # Play the music infinitely
                all_sprites.remove(main_character)
                main_character = MainCharacter()
                all_sprites.add(main_character)
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        main_character.shoot()
    if keys[pygame.K_LEFT]:
        main_character.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        main_character.rect.x += 5
    # Update
    all_sprites.update()
    enemies.update()
    bullets.update()

    # Scroll background
    bg_x1 -= bg_speed
    bg_x2 -= bg_speed
    if bg_x1 <= -background.get_width():
        bg_x1 = bg_x2 + background.get_width()
    if bg_x2 <= -background.get_width():
        bg_x2 = bg_x1 + background.get_width()

    # Check for collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    if hits:
        score += len(hits)

    # Spawn enemies
    if random.random() < 0.02:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw
    screen.fill(WHITE)
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))
    all_sprites.draw(screen)
    # Render the score
    score_text = font.render(f"Score: {score}", True, (255,255,0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)

pygame.quit()
