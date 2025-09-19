import pygame
import numpy as np

width = 900
height = 900
scr = pygame.display.set_mode((width, height))

def rotate(theta, axis, x, y, z):
    theta = np.radians(theta)
    cords = ([x, y, z])

    if axis == "x":
        xRot = ([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta), np.cos(theta)]
            ])

        cords = np.dot(xRot, cords)

    elif axis == 'y':
        yRot = ([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
            ])

        cords = np.dot(yRot, cords)

    elif axis == 'z':
        zRot = ([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
            ])   

        cords = np.dot(zRot, cords)

    return cords

def projection(obj):
    focal_length = 600
    
    for i in range(len(obj.vertexes)):
        tempX = obj.vertexes[i][0] 
        tempY = obj.vertexes[i][1]
        tempZ = obj.vertexes[i][2]

        cords = rotate(obj.xRot, "x", tempX, tempY, tempZ)
        cords = rotate(obj.yRot, "y", cords[0], cords[1], cords[2])
        cords = rotate(obj.zRot, "z", cords[0], cords[1], cords[2])

        tempX = cords[0] - playerCor[0] + obj.x
        tempY = cords[1] - playerCor[1] + obj.y
        tempZ = cords[2] - playerCor[2] + obj.z
        
        #avoids division by 0 and flipping of rendering
        if tempZ <= 0.0000000000000000000000001:
            tempZ = 0.0000000000000000000000001

        obj.projected_vertexes[i][0] = (tempX*focal_length)/tempZ + width/2
        obj.projected_vertexes[i][1] = (tempY*focal_length)/tempZ + height/2
        
class triangle():

    def __init__(self, x=0, y=0, z=0, L = (-1, 0, 0), T = (-1, -2, 0), R = (1, 0, 0)):

        self.x = x
        self.y = y
        self.z = z

        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        
        size = 10

        self.vertexes = [
            [L[0], L[1], L[2]], #left vertex
            [T[0], T[1], T[2]], #middle vertex
            [R[0], R[1], R[2]]  #right vertex
            ]

        self.projected_vertexes = [
            [0, 0],
            [0, 0], 
            [0, 0]
            ]

        self.constructor = [0, 1, 2, 0]
        #constructor tells program what verts are connected

    def draw(self):

        # go through each constructor and draw the lines together
        projection(self)
        for i in range(3):
            pygame.draw.line(scr, (255, 0, 0), (self.projected_vertexes[self.constructor[i]][0], self.projected_vertexes[self.constructor[i]][1]), (self.projected_vertexes[self.constructor[i+1]][0], self.projected_vertexes[self.constructor[i+1]][1]), 5)


playerCor = [0, 0, 0]


cube = [
    triangle(z=10, L=(-5, -5, -5), T=(5, 5, -5), R=(5, -5, -5)),
    triangle(z=10, L=(-5, -5, -5), T=(-5, 5, -5), R=(5, 5, -5)),
    triangle(z=10, L=(-5, -5, 5), T=(5, -5, 5), R=(5, 5, 5)),
    triangle(z=10, L=(-5, -5, 5), T=(5, 5, 5), R=(-5, 5, 5)),
    triangle(z=10, L=(-5, -5, -5), T=(-5, -5, 5), R=(-5, 5, 5)),
    triangle(z=10, L=(-5, -5, -5), T=(-5, 5, 5), R=(-5, 5, -5)),
    triangle(z=10, L=(5, -5, -5), T=(5, 5, -5), R=(5, 5, 5)),
    triangle(z=10, L=(5, -5, -5), T=(5, 5, 5), R=(5, -5, 5)),
    triangle(z=10, L=(-5, 5, -5), T=(-5, 5, 5), R=(5, 5, 5)),
    triangle(z=10, L=(-5, 5, -5), T=(5, 5, 5), R=(5, 5, -5)),
    triangle(z=10, L=(-5, -5, -5), T=(5, -5, -5), R=(5, -5, 5)),
    triangle(z=10, L=(-5, -5, -5), T=(5, -5, 5), R=(-5, -5, 5)),
]

pygame.init()
run = True
while run:

    #movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerCor[2] += 0.05
    if keys[pygame.K_a]:
        playerCor[0] -= 0.1
    if keys[pygame.K_s]:
        playerCor[2] -= 0.05
    if keys[pygame.K_d]:
        playerCor[0] += 0.1
    if keys[pygame.K_LSHIFT]:
        playerCor[1] += 0.1
    if keys[pygame.K_SPACE]:
        playerCor[1] -= 0.1

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #drawing section, clear screen
    scr.fill((0, 0, 0))

    for i in range(len(cube)):
        cube[i].draw()
        cube[i].xRot += 0.4
        cube[i].yRot += 0.4
        cube[i].zRot += 0.4

    pygame.display.flip()

    #drawing section, update screen

pygame.quit()
