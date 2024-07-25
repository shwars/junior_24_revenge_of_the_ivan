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

# State of the game
qstate = 0

# Main character class
class MainCharacter(pygame.sprite.Sprite):
    def __init__(self,base='ivanus',x=50,y=SCREEN_HEIGHT - SPRITE_HEIGHT - 10):
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
        self.rect.x = x
        self.rect.y = y
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

    def throw_gun(self):
        gun = Gun(self.rect.x + self.rect.width, self.rect.y + self.rect.height / 1.5)
        all_sprites.add(gun)

class MainCharacterFinal(pygame.sprite.Sprite):
    def __init__(self,x=50,y=SCREEN_HEIGHT - SPRITE_HEIGHT - 10):
        super().__init__()
        self.image = pygame.image.load(f'ivanus_scared.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    def shoot(self):
        pass

    def throw_gun(self):
        gun = Gun(self.rect.x + self.rect.width, self.rect.y + self.rect.height / 1.5)
        all_sprites.add(gun)


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [
            pygame.image.load(f'pacmitya1.png').convert_alpha(),
            pygame.image.load(f'pacmitya2.png').convert_alpha(),
            ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - SPRITE_HEIGHT + 100 + random.randint(-10,10)
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

class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('gun.png').convert_alpha()  # Load the gun image
        self.original_image = pygame.transform.scale(self.original_image, (150, 100))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0  # Initial angle for rotation

    def update(self):
        self.rect.x += 10
        self.rect.y -= 5
        if self.rect.x > SCREEN_WIDTH:
            self.kill()
        else:
            self.angle -= 10  # Rotate counter-clockwise
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)


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
                if qstate == 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('background.mp3')  # Load the background music
                    pygame.mixer.music.play(-1)  # Play the music infinitely
                    all_sprites.remove(main_character)
                    main_character = MainCharacter('ivanus_star',x=main_character.rect.x,y=main_character.rect.y)
                    all_sprites.add(main_character)
                    qstate += 1
                elif qstate == 1:
                    all_sprites.remove(main_character)
                    main_character = MainCharacter(x=main_character.rect.x,y=main_character.rect.y)
                    all_sprites.add(main_character)
                    qstate += 1
                elif qstate == 2:
                    all_sprites.remove(main_character)
                    main_character = MainCharacterFinal(x=main_character.rect.x,y=main_character.rect.y)
                    all_sprites.add(main_character)
                    qstate += 1
                elif qstate == 3:
                    main_character.throw_gun()
                    qstate += 1
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        main_character.shoot()
    if keys[pygame.K_LEFT]:
        main_character.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        main_character.rect.x += 5
    # Update
    all_sprites.update()
    #enemies.update()
    #bullets.update()

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
