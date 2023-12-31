import pygame
import random
import math
from sys import exit

height = 1900
width = 1030

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((height, width))
pygame.display.set_caption("PSEMO's Game")

clock = pygame.time.Clock()

circleSize = 10
circleSizeSqrd = circleSize * circleSize * 4

framerate = 150

particles = []

boomSound = pygame.mixer.Sound("boom.mp3")

#---------------------------------
def playSong():
    pygame.mixer.music.load("song.mp3")
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)
#---------------------------------
def playBoom(loudness):
    boomSound.set_volume(loudness)
    pygame.mixer.Sound.play(boomSound)
#---------------------------------
class Particle:
    def __init__(self):
        self.pos = [0, 0]
        self.velocity = [0, 0]
        self.duration = 0
        self.timer = 0
        self.R = 0
        self.G = 0
        self.B = 0
#---------------------------------
def createCorpse(corpsePos, corpseVelo, projectileVelo):
    x = 0
    while x < circleSize * 3:
        x += 1
        temp = Particle()
        temp.pos = list(givePosInCircle(list(corpsePos), circleSize))
        temp.velocity = [_random(projectileVelo[0], corpseVelo[0] + projectileVelo[0]),
                         _random(projectileVelo[1], corpseVelo[1] + projectileVelo[1])]
        temp.duration = _random(500, 1250)
        temp.R = _random(0, 255)
        temp.G = _random(0, 255)
        temp.B = _random(0, 255)

        particles.append(temp)
#---------------------------------
class Circle:
    def __init__(self):
        self.pos = [0, 0]
        self.pos[0] = _random(0.3, 0.7) * height
        self.pos[1] = _random(0.3, 0.7) * width

        self.velocity = [_random(0, 10) - 5, _random(0, 10) - 5]
#---------------------------------
def onCollision():
    global circles
    for x in range(1):
        circles.append(createCircle())
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
def particleMover(obj, objSize, ms):
    obj.timer = obj.timer + ms
    obj.pos[0] = obj.pos[0] + (obj.velocity[0] * (60 / framerate)) * ((obj.duration - obj.timer) / obj.duration)
    obj.pos[1] = obj.pos[1] + (obj.velocity[1] * (60 / framerate)) * ((obj.duration - obj.timer) / obj.duration)
    pygame.draw.circle(screen, (obj.R, obj.G, obj.B), obj.pos, objSize)
    if(obj.timer > obj.duration):
        particles.remove(obj)
#---------------------------------
def _random(x, y):
    return random.uniform(x, y)
#---------------------------------
def givePosInCircle(pos, R):
    r = R * math.sqrt(_random(0, 1))
    theta = _random(0, 1) * 2 * math.pi
    x = pos[0] + r * math.cos(theta)
    y = pos[1] + r * math.sin(theta)
    return[x, y]
#---------------------------------
def draw_text(surface, text, size, color, x, y, relative):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surf = font.render(str(text), True, color)
    text_rect = text_surf.get_rect()

    if(relative == 'center'):
        text_rect.center = (x, y)
    
    surface.blit(text_surf, text_rect)
#---------------------------------

circles = []
maxCount = 0

playSong()

#Update()
while 1:
    #count the time frame took and assign it to ms
    ms = clock.tick(framerate)

    #detect collisions, delete collided circles, play sound effect and create corpse
    for circle in circles:
        for circle2 in circles:
            if circle != circle2:
                x = circle.pos[0] - circle2.pos[0]
                y = circle.pos[1] - circle2.pos[1]
                lenghtSqrd = x * x + y * y
                if circleSizeSqrd >= lenghtSqrd:
                    createCorpse(circle.pos, circle.velocity, circle2.velocity)
                    createCorpse(circle2.pos, circle2.velocity, circle.velocity)

                    speedRatio = ((circle.velocity[0] - circle2.velocity[0]) + (circle.velocity[1] - circle2.velocity[1])) / 25
                    speedRatio = speedRatio + 0.2 #max speed dif is 20 therefor code in the upper maxes out at 0.8.
                    #I do that to make sound between 0.2 - 1.0
                    if speedRatio < 0: speedRatio = speedRatio * -1
                    playBoom(speedRatio)

                    if circles.__contains__(circle):
                        circles.remove(circle)
                    if circles.__contains__(circle2):
                        circles.remove(circle2)

                    if(len(circles) == 0):
                        circles.append(createCircle())
    
    #resets screen
    screen.fill((50, 50, 50))
    
    #detect events including inputs
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
    
    #move and draw every circle
    for circle in circles:
        moveNDraw(circle, circleSize)
    
    #move and draw every particle
    for particle in particles:
        particleMover(particle, 2, ms)
    
    #renders text
    if True:
        maxCount = max(maxCount, len(circles))
        draw_text(screen, 'Max: ' + str(maxCount), 32, (255, 255, 255), height / 2, width / 2 - 16, 'center')
        draw_text(screen, 'Count: ' + str(len(circles)), 32, (255, 255, 255), height / 2, width / 2 + 16, 'center')

    pygame.display.flip()