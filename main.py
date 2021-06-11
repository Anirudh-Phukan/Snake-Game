import pygame
from pygame.locals import *
from collections import deque
import random

pygame.init()

clock = pygame.time.Clock()

fps = 30	# controls both the frame rate of the game and the speed of the snake

screen_width = 800
screen_height = 800

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
min_distance = 50 # controls the minimum distance of the power from boundary

# controls the animation of the score board
def draw_text(text, font, text_col, x, y, boundary):
	pygame.draw.rect(screen, black, (0, 0, screen_width, boundary.point3[1] - boundary.width)) 
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
	
def reset_game(boundary):
	boundary.draw()
	snake.head = (((Boundary.point1[0] + Boundary.point3[0]) // 2, (Boundary.point1[1] + Boundary.point2[1]) // 2), snake.size)
	snake.body = deque([])
	power.rect = ((random.randint(Boundary.point1[0] + min_distance,Boundary.point3[0] - min_distance), random.randint(Boundary.point1[1] + min_distance,Boundary.point4[1] - min_distance)), power.size)
	score = 0
	return score

class Boundary():

	
	color = white
	width = 11

	# dimensions of the playing area
	point1 = (50, 100) 	#top left
	point2 = (50, screen_height - 100) 	#bottom left
	point3 = (screen_width - 50, 100) #top right
	point4 = (screen_width - 50, screen_height - 100) #bottom right


	def draw(self):
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
	tail = ((0,0),size)
	
	direction = 'UP'
	
	def draw(self):
		pygame.draw.rect(screen, self.color, self.head) # draw the head
		pygame.draw.rect(screen, black, self.tail) # remove the tail
		
	def move(self):
		if self.direction == 'UP':
			if len(self.body) > 0:
				self.tail = self.body.pop()
				self.body.appendleft(self.head)
			else:
				self.tail = self.head
			self.head = ((self.head[0][0],self.head[0][1] - self.size[1]),self.size)
		elif self.direction == 'LEFT':
			if len(self.body) > 0:
				self.tail = self.body.pop()
				self.body.appendleft(self.head)
			else:
				self.tail = self.head
			self.head = ((self.head[0][0] - self.size[0],self.head[0][1]),self.size)
		elif self.direction == 'RIGHT':
			if len(self.body) > 0:
				self.tail = self.body.pop()
				self.body.appendleft(self.head)
			else:
				self.tail = self.head
			self.head = ((self.head[0][0] + self.size[0],self.head[0][1]),self.size)
		elif self.direction == 'DOWN':
			if len(self.body) > 0:
				self.tail = self.body.pop()
				self.body.appendleft(self.head)
			else:
				self.tail = self.head
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

		#check collision with itself
		rect1 = pygame.Rect(self.head)
		rectList = []
		for b in self.body:
			rectList.append(b)
		if rect1.collidelist(rectList) != -1:
			return True

		#check collision with boundary
		if self.head[0][1] <= Boundary.point1[1] + Boundary.width // 2 \
			or self.head[0][1] + self.size[1] >= Boundary.point2[1] - Boundary.width // 2\
				or self.head[0][0] <= Boundary.point1[0] + Boundary.width // 2\
			 		or self.head[0][0] + self.size[0] >= Boundary.point3[0] - Boundary.width // 2:
			return True
		return False
		
		
class Power():
	
	color = red
	size = (15, 15)
	rect = ((random.randint(Boundary.point1[0] + min_distance,Boundary.point3[0] - min_distance), random.randint(Boundary.point1[1] + min_distance,Boundary.point4[1] - min_distance)), size)
	
	def draw(self):
		pygame.draw.rect(screen, self.color, self.rect)
		
	def change(self,head,score):
		rect1 = pygame.Rect(head) # postion of snake head
		rect2 = pygame.Rect(self.rect) # position of power
		flag = False
		if rect1.colliderect(rect2) == True:
			pygame.draw.rect(screen, black, self.rect)
			self.rect = ((random.randint(Boundary.point1[0] + min_distance,Boundary.point3[0] - min_distance), random.randint(Boundary.point1[1] + min_distance,Boundary.point4[1] - min_distance)), self.size)
			score += 1
			flag = True
		return score,flag
	
	
	
		
boundary =  Boundary()

snake = Snake()

power = Power()

run = True

boundary.draw()

while run:
	clock.tick(fps)
	
	draw_text(str(score), font, white, int(screen_width / 2), 20,boundary) # draw the score board
	
	snake.draw()
	
	power.draw()
	
	if game_over == False:
	
		snake.change_direction()
		
		snake.move()
		
		game_over = snake.collision() # check for collision of snake with itself and boundary
		
		score,flag = power.change(snake.head,score) # check if postion of apple needs to be changed and apply the changes
		
		if flag == True:
			snake.add() #increase length of snake
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and game_over == True:
			score = reset_game(boundary)
			game_over = False
			
	pygame.display.update()

pygame.quit()
