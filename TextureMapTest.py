import pygame
import math
import numpy as np

#-----------------init-------------------#
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 36)
scr = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# Load texture
texture = pygame.image.load("Resources//OIP.jpeg").convert()
texture_width, texture_height = texture.get_size()
texture = pygame.surfarray.array3d(texture)

#----------------------------------------#

theta = 0
x_pos = 200
y_pos = 200

triangle = [
    [0, 200], [200, 200], [100, 0]
    ]

uv_ = [
    [0.0, 0.0],  
    [1.0, 0.0], 
    [0.5, 1.0]  
]

def centric():
    ax= triangle[0][0] 
    ay= triangle[0][1] 
    bx= triangle[1][0] 
    by= triangle[1][1]
    cx= triangle[2][0] 
    cy= triangle[2][1] 

    d = (by - cy)*(ax - cx) + (cx - bx)*(ay - cy)
    a= ((by - cy)*(xbound[:, None] - cx) + (cx - bx)*(ybound - cy)) / d
    b= ((cy - ay)*(xbound[:, None] - cx) + (ax - cx)*(ybound - cy)) / d
    c= 1-a-b

    mask = (a >= 0) & (b >= 0) & (c >= 0)
    x_in, y_in = np.where(mask)

    u = a[mask] * uv_[0][0] + b[mask] * uv_[1][0] + c[mask] * uv_[2][0]
    v = a[mask] * uv_[0][1] + b[mask] * uv_[1][1] + c[mask] * uv_[2][1]
    tex_x = (u * (texture_width - 1)).astype(int)
    tex_y = (v * (texture_height - 1)).astype(int)
    color = texture[tex_x, tex_y]

    pixels = pygame.surfarray.pixels3d(scr)
    pixels[x_in+x_pos, y_in+y_pos] = color
    
run = True
while run:

    fps = clock.get_fps()
    fpstext = font.render(str(math.ceil(fps)), True, (255, 255, 255))

    min_x = int(min(triangle[0][0], triangle[1][0], triangle[2][0])) 
    max_x = int(max(triangle[0][0], triangle[1][0], triangle[2][0])) 
    min_y = int(min(triangle[0][1], triangle[1][1], triangle[2][1])) 
    max_y = int(max(triangle[0][1], triangle[1][1], triangle[2][1]))

    xbound = np.arange(min_x, max_x)
    ybound = np.arange(min_y, max_y)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT]:
        theta += 0.02
            
    elif keys[pygame.K_LEFT]:
        theta -= 0.02

    #all triangle changes
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

    scr.fill((0, 0, 0))

    centric()
    scr.blit(fpstext, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick() #update fps

pygame.quit()
