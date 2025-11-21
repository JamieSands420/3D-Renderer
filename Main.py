import pygame
import numpy as np
from pynput import mouse

width = 900
height = 800
scr = pygame.display.set_mode((width, height))
mousePos = [0, 0]

root = __file__[:-7]
Resources = f"{root}\\Resources\\"

opened_scene = ""
def read_scene():
    global opened_scene
    
    with open(f"{root}\\Config.txt", 'r') as file:
        for line in file:
            if line.startswith('Scene; '):
                parts = line.strip().split()

        if opened_scene == parts[1]:
            return "same"
        else:
            opened_scene = parts[1]
            return parts[1]
        
        

# obj parse
def load_obj(filename, xx=0, yy=0, zz=10, size = 1):
    vertices = []
    triangles = []
    filename = f"{Resources}{filename}.obj"

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                x, y, z = float(parts[1])/size, 0 - float(parts[2])/size, float(parts[3])/size
                vertices.append((x, y, z))
            elif line.startswith('f '):
                parts = line.strip().split()
                face_indices = [int(p.split('/')[0]) - 1 for p in parts[1:4]]
                v1, v2, v3 = vertices[face_indices[0]], vertices[face_indices[1]], vertices[face_indices[2]]
                tri = triangle(x=xx, y=yy, z=zz, L=v1, T=v2, R=v3)
                triangles.append(tri)

    return triangles

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
        #Translate vertex
        tempX = obj.vertexes[i][0] + obj.x - playerCor[0]
        tempY = obj.vertexes[i][1] + obj.y - playerCor[1]
        tempZ = obj.vertexes[i][2] + obj.z - playerCor[2]

        #Rotate vertex
        cords = rotate(obj.yRot+playerRot[1], "y", tempX, tempY, tempZ)
        cords = rotate(obj.xRot+playerRot[0], "x", cords[0], cords[1], cords[2])
        cords = rotate(obj.zRot+playerRot[2], "z", cords[0], cords[1], cords[2])

        #Prevent divide by zero or flipping of rendering
        if cords[2] <= 0.0000001:
            cords[2] = 0.0000001

        obj.projected_vertexes[i][0] = (cords[0] * focal_length) / cords[2] + width / 2
        obj.projected_vertexes[i][1] = (cords[1] * focal_length) / cords[2] + height / 2

        
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
            pygame.draw.line(scr, (0, 0, 0), (self.projected_vertexes[self.constructor[i]][0], self.projected_vertexes[self.constructor[i]][1]), (self.projected_vertexes[self.constructor[i+1]][0], self.projected_vertexes[self.constructor[i+1]][1]), 5)

scene = []
def load_scene(sceneinput):
    global scene

    if sceneinput != "same":
        scene = []
        if sceneinput == "Untitled":
            print("loaded untitled")
            scene.append(load_obj("tree", 0, 0, 0))
            scene.append(load_obj("crate", 0, 5, 0))
        elif sceneinput == "Cube":
            print("loaded cube")
            scene.append(load_obj("cube", 0, 0, 10))
            

playerCor = [0, 0, 0]
playerRot = [0, 0, 0]

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
pygame.mouse.get_rel()
pygame.init()
run = True
while run:

    load_scene(read_scene())

    #movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerCor[2] += 0.15
    if keys[pygame.K_a]:
        playerCor[0] -= 0.4
    if keys[pygame.K_s]:
        playerCor[2] -= 0.15
    if keys[pygame.K_d]:
        playerCor[0] += 0.4
    if keys[pygame.K_LSHIFT]:
        playerCor[1] += 1
    if keys[pygame.K_SPACE]:
        playerCor[1] -= 1

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #drawing section, clear screen
    scr.fill((200, 200, 255))

    keys = pygame.key.get_pressed()

    # drawing the loaded scene
    for i in range(len(scene)):
        for ii in range(len(scene[i])):
            scene[i][ii].draw()
        
    pygame.display.flip()

    dx, dy = pygame.mouse.get_rel()
    playerRot[1] -= dx * 0.2 
    playerRot[0] += dy * 0.2 

pygame.quit()
