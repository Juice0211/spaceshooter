import pygame
import sys
from pygame.locals import *
from random import randint, choice


def drawenemy():
	for enemy in enemies:
		enemy['rect'].x -= 3
		screen.blit(enemy['image'], enemy['rect'])
		if enemy['rect'].right < 0:
			enemies.remove(enemy)

def loading():
	global gaming
	while gaming == 'Opening':
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and event.key == K_SPACE:
				gaming = 'Gaming'
		screen.blit(start_img, (0,0))
		pygame.display.update()


def restarting():
	global gaming
	global hpbar
	global score
	global text
	while gaming == 'Dead':
		score = 0
		text = font.render(str(score), True, (255, 255, 255))
		hpbar.width = 200
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN and event.key == K_r:
				gaming = 'Gaming'
		screen.blit(dead_img, (0,0))
		pygame.display.update()

pygame.init()

width = 700
height = 500
screen = pygame.display.set_mode((width, height))

# 배경
bgImage = pygame.image.load('background.jpg')
bgImage = pygame.transform.scale(bgImage, (width, height))
backX = 0
backX2 = width-10

# 주인공
img = pygame.image.load('spaceship.png')
spaceship = {'rect': pygame.Rect(30, 215, 70, 70),
			 'image': pygame.transform.scale(img, (70, 70))}

# 총알
bullets = []
bulletImage = pygame.image.load('bullet1.png')
bulletImage = pygame.transform.scale(bulletImage, (20, 10))

#운석들
enemies = []
cnt = 0
imgList = [pygame.image.load('stone1.png'), pygame.image.load('stone2.png')]

#점수
score = 0
font = pygame.font.SysFont(pygame.font.get_default_font(), 45)
text = font.render(str(score), True, (255, 255, 255))

#HP
hpbar = pygame.Rect(10, 10, 200, 20)
outline = pygame.Rect(10, 10, 200, 20)

#start and gameover
start_img = pygame.image.load('start.jpg')
start_img = pygame.transform.scale(start_img, (width, height))
dead_img = pygame.image.load('gameover.jpg')
dead_img = pygame.transform.scale(dead_img, (width, height))

clock = pygame.time.Clock()
gaming = 'Opening'
loading()
while True:
	cnt += randint(0, 10)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		# if event.type == KEYDOWN and event.key == K_SPACE:
		# 	bullet = pygame.Rect(spaceship['rect'].centerx - 10,
		# 						 spaceship['rect'].centery - 5,
		# 						 20, 10)
		# 	bullets.append(bullet)

	# 키보드 이벤트
	keyInput = pygame.key.get_pressed()
	if keyInput[K_SPACE]:
		bullet = pygame.Rect(spaceship['rect'].centerx - 10,
		                     spaceship['rect'].centery - 5,
		                     20, 10)
		bullets.append(bullet)
	if keyInput[K_RIGHT]:
		backX -= 3
		backX2 -= 3
		drawenemy()

	if keyInput[K_UP]:
		if spaceship['rect'].bottom < 0:
			spaceship['rect'].top = height
		spaceship['rect'].top -= 4
	elif keyInput[K_DOWN]:
		if spaceship['rect'].top > height:
			spaceship['rect'].bottom = 0
		spaceship['rect'].bottom += 4

	#운석 추가
	if cnt >= 120:
		cnt = 0
		size = randint(10, 30)
		enemy = {'rect':pygame.Rect(width, randint(0, height-size), size, size),
		         'image':pygame.transform.scale(choice(imgList), (size, size))}
		enemies.append(enemy)

	#운석, 총알 충돌
	for bullet in bullets:
		for enemy in enemies:
			if bullet.colliderect(enemy['rect']):
				enemies.remove(enemy)
				score += 1
				text = font.render(str(score), True, (255, 255, 255))

	#운석, 우주선 충둘
	for enemy in enemies:
		if spaceship['rect'].colliderect(enemy['rect']):
			enemies.remove(enemy)
			hpbar.width -= 10
			if hpbar.width <= 0:
				gaming = 'Dead'
				restarting()

	# 배경 움직임
	if backX <= width * -1:
		backX = width-10

	if backX2 <= width * -1:
		backX2 = width-10

	if backX >= 0:
		backX -= width-10
		backX2 -= width-10



	screen.blit(bgImage, (backX, 0))
	screen.blit(bgImage, (backX2, 0))
	drawenemy()
	for bullet in bullets:
		bullet.x += 5
		screen.blit(bulletImage, bullet)
		if bullet.right >= width:
			bullets.remove(bullet)

	screen.blit(spaceship['image'], spaceship['rect'])
	screen.blit(text, ((width - text.get_width())/ 2, 10))
	pygame.draw.rect(screen, (255, 0, 0), hpbar)
	pygame.draw.rect(screen, (255, 255, 255), outline, 2)
	pygame.display.update()
	clock.tick(240)