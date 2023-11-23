import pygame
import random
from sys import exit

height = 1920
width = 1000

pygame.init()
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption("PSEMO's Game")

clock = pygame.time.Clock()

circleSize = 20

circleSizeSqrd = circleSize * circleSize * 4

framerate = 150

#---------------------------------
class Circle:
    def __init__(self):
        self.pos = [0, 0]
        self.pos[0] = random.uniform(0.3, 0.7) * 800
        self.pos[1] = random.uniform(0.3, 0.7) * 600

        self.velocity = [random.uniform(0, 10) - 5, random.uniform(0, 10) - 5]
#---------------------------------
def onCollision():
    global circles
    circles.append(createCircle())
    len(circles)
#---------------------------------
def createCircle():
    circle = Circle()
    return circle
#---------------------------------
def moveNDraw(obj, objSize):
    obj.pos[0] = obj.pos[0] + obj.velocity[0] * (60 / framerate)
    obj.pos[1] = obj.pos[1] + obj.velocity[1] * (60 / framerate)
    pygame.draw.circle(screen, (200, 0, 0), obj.pos, objSize)
    
    if obj.pos[0] + objSize > height:
        obj.pos[0] = height - objSize
        obj.velocity[0] = -obj.velocity[0] * 1.1
        onCollision()
        #do something about velocity
    elif obj.pos[0] - objSize < 0:
        obj.pos[0] = 0 + objSize
        obj.velocity[0] = -obj.velocity[0] * 1.1
        onCollision()
        #do something about velocity
    
    if obj.pos[1] + objSize > width:
        obj.pos[1] = width - objSize
        obj.velocity[1] = -obj.velocity[1] * 1.1
        onCollision()
        #do something about velocity
    elif obj.pos[1] - objSize < 0:
        obj.pos[1] = 0 + objSize
        obj.velocity[1] = -obj.velocity[1] * 1.1
        onCollision()
        #do something about velocity
#---------------------------------

circles = []
circles.append(createCircle())

while 1:
    screen.fill((50, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                    circles.append(createCircle())
            if event.key == pygame.K_0:
                    for circle in circles:
                        circles.remove(circle)

    for circle in circles:
        moveNDraw(circle, circleSize)
            
    pygame.display.flip()
    clock.tick(framerate)
    
    for circle in circles:
        for circle2 in circles:
            if circle != circle2:
                x = circle.pos[0] - circle2.pos[0]
                y = circle.pos[1] - circle2.pos[1]
                lenghtSqrd = x * x + y * y
                if circleSizeSqrd >= lenghtSqrd:
                    circles.remove(circle)
                    circles.remove(circle2)
                    if(len(circles) == 0):
                        circles.append(createCircle())