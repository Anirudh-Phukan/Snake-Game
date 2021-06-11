import pygame
from pygame.locals import *
from collections import deque
import random

pygame.init()

clock = pygame.time.Clock()
fps = 30

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colors
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)

#define game variables
score = 0
game_over = True

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
	
def reset_game():
	snake.head = (((Boundary.point1[0] + Boundary.point3[0]) // 2, (Boundary.point1[1] + Boundary.point2[1]) // 2), snake.size)
	snake.body = deque([])
	power.rect = ((random.randint(Boundary.point1[0] + 20,Boundary.point3[0] - 20), random.randint(Boundary.point1[1] + 20,Boundary.point4[1] - 20)), power.size)
	score = 0
	return score

class Boundary():

	
	color = white
	width = 11
	point1 = (20, 100) 	#top left
	point2 = (20, 800) 	#bottom left
	point3 = (800, 100) #top right
	point4 = (800, 800) #bottom right


	def draw(self):
		#pygame.draw.rect(screen, black, (0, 0, screen_width, screen_height)) 
		screen.fill(black)
		pygame.draw.line(screen, self.color, self.point1, self.point3, self.width)
		pygame.draw.line(screen, self.color, self.point2, self.point4, self.width)
		pygame.draw.line(screen, self.color, self.point1, self.point2, self.width)
		pygame.draw.line(screen, self.color, self.point3, self.point4, self.width)
		
class Snake():
	
	color = green
	
	size = (15, 15)
	
	head = (((Boundary.point1[0] + Boundary.point3[0]) // 2, (Boundary.point1[1] + Boundary.point2[1]) // 2), size)
	body = deque([])
	
	direction = 'UP'
	
	def draw(self):
		pygame.draw.rect(screen, self.color, self.head)
		for i in range(0,len(self.body)):
			pygame.draw.rect(screen, self.color, self.body[i])
		
	def move(self):
		if self.direction == 'UP':
			if len(self.body) > 0:
				self.body.pop()
				self.body.appendleft(self.head)
			self.head = ((self.head[0][0],self.head[0][1] - self.size[1]),self.size)
		elif self.direction == 'LEFT':
			if len(self.body) > 0:
				self.body.pop()
				self.body.appendleft(self.head)
			self.head = ((self.head[0][0] - self.size[0],self.head[0][1]),self.size)
		elif self.direction == 'RIGHT':
			if len(self.body) > 0:
				self.body.pop()
				self.body.appendleft(self.head)
			self.head = ((self.head[0][0] + self.size[0],self.head[0][1]),self.size)
		elif self.direction == 'DOWN':
			if len(self.body) > 0:
				self.body.pop()
				self.body.appendleft(self.head)
			self.head = ((self.head[0][0],self.head[0][1] + self.size[1]),self.size)
			
	def change_direction(self):
		if pygame.key.get_pressed()[K_UP] == 1 and self.direction != 'DOWN':
			self.direction = 'UP'
		elif pygame.key.get_pressed()[K_DOWN] == 1 and self.direction != 'UP':
			self.direction = 'DOWN'
		elif pygame.key.get_pressed()[K_LEFT] == 1 and self.direction != 'RIGHT':
			self.direction = 'LEFT'
		elif pygame.key.get_pressed()[K_RIGHT] == 1 and self.direction != 'LEFT':
			self.direction = 'RIGHT'
			
	def add(self):
		if not self.body:
			self.body.append(self.head)
		else:
			self.body.append(self.body[-1])
			
	def collision(self):
		rect1 = pygame.Rect(self.head)
		rectList = []
		for b in self.body:
			rectList.append(b)
		if rect1.collidelist(rectList) != -1:
			return True
		if self.head[0][1] <= Boundary.point1[1] + Boundary.width // 2 \
			or self.head[0][1] + self.size[1] >= Boundary.point2[1] - Boundary.width // 2\
				or self.head[0][0] <= Boundary.point1[0] + Boundary.width // 2\
			 		or self.head[0][0] + self.size[0] >= Boundary.point3[0] - Boundary.width // 2:
			return True
		return False
		
		
class Power():
	
	color = red
	size = (15, 15)
	rect = ((random.randint(Boundary.point1[0] + 20,Boundary.point3[0] - 20), random.randint(Boundary.point1[1] + 20,Boundary.point4[1] - 20)), size)
	
	def draw(self):
		pygame.draw.rect(screen, self.color, self.rect)
		
	def change(self,head,score):
		rect1 = pygame.Rect(head)
		rect2 = pygame.Rect(self.rect)
		flag = False
		if rect1.colliderect(rect2) == True:
			self.rect = ((random.randint(Boundary.point1[0] + 20,Boundary.point3[0] - 20), random.randint(Boundary.point1[1] + 20,Boundary.point4[1] - 20)), self.size)
			score += 1
			flag = True
		return score,flag
	
	
	
		
boundary =  Boundary()

snake = Snake()

power = Power()

run = True

while run:
	clock.tick(fps)
	
	boundary.draw()
	
	draw_text(str(score), font, white, int(screen_width / 2), 20)
	
	snake.draw()
	
	power.draw()
	
	if game_over == False:
	
		snake.change_direction()
		
		snake.move()
		
		game_over = snake.collision()
		
		score,flag = power.change(snake.head,score)
		
		if flag == True:
			snake.add()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and game_over == True:
			score = reset_game()
			game_over = False
			
	pygame.display.update()

pygame.quit()
