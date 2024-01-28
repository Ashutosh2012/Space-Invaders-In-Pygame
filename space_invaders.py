import pygame
from pygame import mixer
import random
import time

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
FPS = 60

# Game variables

score = 0
game_over = -1

# Colors


orange = (255, 72, 0)

# Font

font = pygame.font.SysFont("Ink Free", 24, True, False)

# Screen

WIDTH = 750
HEIGHT = 750
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Space Invaders by @AM2012")

# Images

bg_img = pygame.image.load("img/bg.png").convert_alpha()
player_img = pygame.image.load("img/spaceship.png").convert_alpha()
missile_img = pygame.image.load("img/missile.png").convert_alpha()
alien = pygame.image.load("img/alien.png").convert_alpha()
alien_img = pygame.transform.scale(alien, (alien.get_width() - 25,
										   alien.get_height() - 25))

# Sounds

pygame.mixer.music.load("sounds/background.wav")
pygame.mixer.music.play(-1)

# Player class

class Player:
	def __init__(self):
		self.x = WIDTH / 2
		self.y = HEIGHT / 2 + 310
		self.vel_x = 4
		self.cooldown_count = 0
		self.bullets = []
		self.image = player_img
		
	def left(self):
		self.x -= self.vel_x
	
	def right(self):
		self.x += self.vel_x

	def cooldown(self):
		if self.cooldown_count >= 30:
			self.cooldown_count = 0
		elif self.cooldown_count > 0:
			self.cooldown_count += 1

	def move(self, key):
		if key[pygame.K_LEFT] and self.x > 0:
			self.left()
			
		if key[pygame.K_RIGHT] and self.x < WIDTH - 65:
			self.right()
			
	def shoot(self, key):
		self.cooldown()
		if key[pygame.K_SPACE] and self.cooldown_count == 0:
			shoot_sound = mixer.Sound("sounds/shoot.wav")
			shoot_sound.play()
			bullet = Missile(self.x, self.y)
			self.bullets.append(bullet)
			self.cooldown_count = 1
		for bullet in self.bullets:
			bullet.move()
			if bullet.off_screen():
				self.bullets.remove(bullet)

	def collision(self, other):
		return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

	def draw(self):
		screen.blit(self.image, (self.x, self.y))
		
# Missile

class Missile:
	def __init__(self, x, y):
		self.x = x + 17
		self.y = y + 15
		self.image = missile_img
		
	def draw_bullet(self):
		screen.blit(self.image, (self.x, self.y))

	def move(self):
		self.y -= 15

	def off_screen(self):
		return not(self.y >= 0)


class Enemy():
	def __init__(self):
		self.image = alien_img
		self.x = random.randint(WIDTH / 2 - 300, WIDTH / 2 + 300)
		self.y = HEIGHT - 815
		self.vel_y = random.randint(2, 6)

	def move(self):
		self.y = self.y + self.vel_y
		
		if self.y == 685:
			self.x = random.randint(WIDTH / 2 - 300, WIDTH / 2 + 300)
			self.y = HEIGHT - 815

	def collision(self, other):
		return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
			
	def draw(self):
		screen.blit(self.image, (self.x, self.y))
		self.image.set_colorkey((255, 255, 255))

# Drawing text

def draw_text(text, font, col, x, y):
	text_img = font.render(text, True, col)
	screen.blit(text_img, (x, y))

# Instances

player = Player()
enemies = []

for _ in range(5):
	enemies.append(Enemy())

# Game loop

run = True
while run:
	pygame.display.update()
	clock.tick(60)
	
	screen.blit(bg_img, (0, 0))
	
	draw_text(f"{score}",font, orange, WIDTH - 750, HEIGHT / 2 - 375)
	
	draw_text("Press 'A' to restart the game!", font, orange,
	WIDTH - 550, HEIGHT / 2 - 375)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			
	key = pygame.key.get_pressed()
	
	# Restart the game
	
	if key[pygame.K_a]:
		game_over = -1
		score = 0
		enemies.clear()
		for _ in range(5):
			enemies.append(Enemy())
			
	# Drawing
			
	player.draw()
	
	for enemy in enemies:
		enemy.draw()

	for bullet in player.bullets:
		bullet.draw_bullet()
	
	# Shooting the projectiles

	player.shoot(key)

	# Moving the player

	player.move(key)
	for enemy in enemies:
		enemy.move()

	# Checking for collisions

	# Bullet against enemy

	for bullet in player.bullets:
		for e in enemies:
			if e.collision(bullet) < 32:
				explosion_sound = mixer.Sound("sounds/explosion.wav")
				explosion_sound.play()
				score += 1
				enemies.remove(e)
				player.bullets.remove(bullet)

	# Enemy against player

	for e in enemies:
		if e.collision(player) < 20 :
			game_over = 0
	
	# Game over conditions
			
	if game_over == 0:
		draw_text(f"You lost! You killed {score} aliens!",font, orange, 
		WIDTH / 2 - 175, HEIGHT / 2)
		enemies.clear()	
		
	elif score == 5:
		draw_text("You won! You killed all aliens!",font, orange, 
		WIDTH / 2 - 175, HEIGHT / 2)
		enemies.clear()	
	
pygame.quit()
