import pygame
import math
import numpy as np

#-----------------init-------------------#
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 36)
scr = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
#----------------------------------------#

def centric(x, y, type):
    
    ax=triangle[0][0] + x_pos
    ay=triangle[0][1] + y_pos
    bx=triangle[1][0] + x_pos
    by=triangle[1][1] + y_pos
    cx=triangle[2][0] + x_pos
    cy=triangle[2][1] + y_pos

    d = (by - cy)*(ax - cx) + (cx - bx)*(ay - cy)
    a= ((by - cy)*(x - cx) + (cx - bx)*(y - cy)) / d
    b= ((cy - ay)*(x - cx) + (ax - cx)*(y - cy)) / d
    c= 1-a-b

    if type == "check":
        if a > 0 and b > 0 and c > 0:
            return True
    
theta = 0
x_pos = 275
y_pos = 475

triangle = [
    [0, 0], [250, 0], [125, -250]
    ]

#--------------Main-loop-----------------#
run = True
while run:
    
    fps = clock.get_fps()
    fpstext = font.render(str(math.ceil(fps)), True, (255, 255, 255))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT]:
        theta -= 0.02
            
    elif keys[pygame.K_LEFT]:
        theta += 0.02

    if keys[pygame.K_q]:
        print(list)


#-------------Rotating-------------------#
    for i in range(3):
        triangle[i][0] -= 125
        triangle[i][1] += 125
        
    rot = ([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)],
        ])

    triangle = np.array([
        np.dot(rot, p) for p in triangle
    ])

    for i in range(3):
        triangle[i][0] += 125
        triangle[i][1] -= 125

    theta = 0
#--------------bounding-box--------------#
    min_x = int(min(triangle[0][0], triangle[1][0], triangle[2][0])) + x_pos
    max_x = int(max(triangle[0][0], triangle[1][0], triangle[2][0])) + x_pos
    min_y = int(min(triangle[0][1], triangle[1][1], triangle[2][1])) + y_pos
    max_y = int(max(triangle[0][1], triangle[1][1], triangle[2][1])) + y_pos
#----------------------------------------#
    
#-------------Event-handler--------------#
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
#--------------Draw-loop-----------------#
    scr.fill((0, 0, 0))

    scr.blit(fpstext, (0, 0))
    
    for i in range(2):
        pygame.draw.line(scr, (255, 255, 255), (triangle[i][0]+x_pos, triangle[i][1]+y_pos), (triangle[i+1][0]+x_pos, triangle[i+1][1]+y_pos))
    pygame.draw.line(scr, (255, 255, 255), (triangle[2][0]+x_pos, triangle[2][1]+y_pos), (triangle[0][0]+x_pos, triangle[0][1]+y_pos))

    for x in range(min_x, max_x + 1):   
        for y in range(min_y, max_y + 1):
            if centric(x, y, "check"):
                scr.set_at((x, y), (255, 0, 0))
                
    pygame.draw.rect(scr, (0, 255, 0), ((min_x, min_y), (max_x- min_x, max_y-min_y)), 1)
    
    pygame.display.flip()
#----------------------------------------#
    clock.tick(120) #update fps
#----------------------------------------#
