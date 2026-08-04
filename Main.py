import pygame
import numpy as np
import math
from pynput import mouse

#-- INIT VARIABLES --#
width, height = 900, 800
fps = 0
render_distance = 1000
mousePos = [0, 0]
details = False
sceneName = ""
scene = np.array([])
playerCor = [0, 0, 0]
playerRot = [0, 0, 0]
draw = False
grab = False #window mouse lock
vertsX = []
vertsY = []

#directory variables
root = __file__[:-7]
Resources = f"{root}Resources/"

#-- INIT PYGAME --#
scr = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 36)
pygame.mouse.set_visible(True)
pygame.event.set_grab(grab)
pygame.mouse.get_rel()
pygame.init()

#-- Read config file --#
def read_config():
    global sceneName
    global details

    with open(f"{root}Config.txt", 'r') as file:
        for line in file:
            parts = line.strip().split()
            
            #scene loading
            if line.startswith("Scene; "):
    
                if sceneName == parts[1]:
                    return "same"
                else:
                    sceneName = parts[1]
                
            #details loading
            elif line.startswith('Details; '):
                if parts[1] == "False":
                    details = False
                else:
                    details = True

        

#-- reads obj file and parse --#
def read_obj(filename, xx=0, yy=0, zz=0, size=1):
    verts = []
    obj = []
    filename = f"{Resources}{filename}.obj"

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()

            #verts
            if line.startswith("v "):
                x = float(parts[1])*size
                y = 0 - float(parts[2])*size
                z = float(parts[3])*size
                verts.append((x, y, z))

            #faces
            elif line.startswith("f "):

                #access data
                face = [int(p.split('/')[0]) - 1 for p in parts[1:4]]
                v1, v2, v3 = verts[face[0]], verts[face[1]], verts[face[2]]

                #triangle object
                tri = [xx, yy, zz,
                       v1[0], v1[1], v1[2],
                       v2[0], v2[1], v2[2],
                       v3[0], v3[1], v3[2],
                       0,0,0,10]  # face can be dropped or flattened too
                
                obj.append(tri)

    obj = np.array(obj)

    return obj

#-- ROTATE A GIVEN OBJ --#
def rotate(xt, yt, zt, x, y, z):

    verts = np.column_stack((x, y, z))
    
    #theta rotations of each axis
    xt, yt, zt = np.radians(xt), np.radians(yt), np.radians(zt)

    xRot = ([
        [1, 0, 0],
        [0, np.cos(xt), -np.sin(xt)],
        [0, np.sin(xt), np.cos(xt)]
        ])

    yRot = ([
        [np.cos(yt), 0, np.sin(yt)],
        [0, 1, 0],
        [-np.sin(yt), 0, np.cos(yt)]
        ])

    zRot = ([
        [np.cos(zt), -np.sin(zt), 0],
        [np.sin(zt), np.cos(zt), 0],
        [0, 0, 1]
        ])   

    #apply rotations
    verts = np.dot(yRot, verts.T)
    verts = np.dot(xRot, verts)
    verts = np.dot(zRot, verts)

    verts = verts.T

    x = verts[:, 0]
    y = verts[:, 1]
    z = verts[:, 2]

    return x, y, z

#-- projection math --#
def projection():
    global draw
    global projVerts
    focal_length = 600
    projectedVerts = []
    global vertsX
    global vertsY
    global scene

    #print("Projection start:")
    #print(scene[:16])

    xyzall = scene

    #xyzall as verts verts are values [3 4 5] global location is [0 1 2] rot is [6 7 8] and size is [9] BUT MAKE WORK WITH NTH TERM so INDEX NUMBER + LENGTH OF DATA INSIDE TRI
    
    #translation
    #print("After translation:")
    #print(scene[:16])
    xyzall[3::16] = xyzall[3::16] + xyzall[0::16] - playerCor[0]#x
    xyzall[4::16] = xyzall[4::16] + xyzall[1::16] - playerCor[1]#y
    xyzall[5::16] = xyzall[5::16] + xyzall[2::16] - playerCor[2]#z

    xyzall[6::16] = xyzall[6::16] + xyzall[0::16] - playerCor[0]
    xyzall[7::16] = xyzall[7::16] + xyzall[1::16] - playerCor[1]
    xyzall[8::16] = xyzall[8::16] + xyzall[2::16] - playerCor[2]

    # v3
    xyzall[9::16]  = xyzall[9::16]  + xyzall[0::16] - playerCor[0]
    xyzall[10::16] = xyzall[10::16] + xyzall[1::16] - playerCor[1]
    xyzall[11::16] = xyzall[11::16] + xyzall[2::16] - playerCor[2]

    #render distance
    if np.any(xyzall - playerCor[0] > render_distance) or np.any(xyzall - playerCor[1] > render_distance) or np.any(xyzall - playerCor[0] > render_distance) or np.any(playerCor[0] - xyzall > render_distance) or np.any(playerCor[1] - xyzall > render_distance) or np.any(playerCor[0] - xyzall > render_distance):
        draw = False
        return

    xyzall[3::16], xyzall[4::16], xyzall[5::16] = rotate(playerRot[0], playerRot[1], playerRot[2], xyzall[3::16], xyzall[4::16], xyzall[5::16]) #v1
    xyzall[6::16], xyzall[7::16], xyzall[8::16] = rotate(playerRot[0], playerRot[1], playerRot[2], xyzall[6::16], xyzall[7::16], xyzall[8::16]) #v2
    xyzall[9::16], xyzall[10::16], xyzall[11::16] = rotate(playerRot[0], playerRot[1], playerRot[2], xyzall[9::16], xyzall[10::16], xyzall[11::16]) #v3

    #project v

    v1x = xyzall[3::16] * focal_length / xyzall[5::16] + width / 2
    v1y = xyzall[4::16] * focal_length / xyzall[5::16] + height / 2
 
    v2x = xyzall[6::16] * focal_length / xyzall[8::16] + width / 2
    v2y = xyzall[7::16] * focal_length / xyzall[8::16] + height / 2

    v3x = xyzall[9::16] * focal_length / xyzall[11::16] + width / 2
    v3y = xyzall[10::16] * focal_length / xyzall[11::16] + height / 2

    # Then draw lines between them
    for i in range(len(v1x)):
        if xyzall[i*16+5] > 0 and xyzall[i*16+8] > 0 and xyzall[i*16+11] > 0: 
            pygame.draw.line(scr, (255,255,255), (v1x[i], v1y[i]), (v2x[i], v2y[i]), 2)
            pygame.draw.line(scr, (255,255,255), (v2x[i], v2y[i]), (v3x[i], v3y[i]), 2)
            pygame.draw.line(scr, (255,255,255), (v3x[i], v3y[i]), (v1x[i], v1y[i]), 2)
                             
#-- populte scene --#
def load_scene(sceneName):
    global scene

    #check if the scene is the same
    if sceneName != "same":
        scene = []

        #loads untitled 
        if sceneName == "Untitled":
            scene = np.append(scene, read_obj("tree", 0, 0, 0, 1))
            scene = np.append(scene, read_obj("crate", 0, 5, 0, 0.5))

        #loads cube
        elif sceneName == "Cube":
            scene = np.append(scene, read_obj("cube", 0, 0, 10))

        elif sceneName == "Car":
            scene = np.append(scene, read_obj("car", 0, 0, 10))

        elif sceneName == "Bigcube":
            for i in range(5):
                for ii in range(5):
                    for iii in range(5):
                        scene = np.append(scene, read_obj("cube", 20*i, 20*iii, 20*ii))

    else:
        return
            
        print(f"Loaded {sceneName}")
        print(scene[:16])

run = True
while run:
    
    #update text variables
    fpstext = font.render(str(math.ceil(fps)), True, (255, 255, 255))
    xyztext = font.render(
        f"x;{math.ceil(playerCor[0])} y;{math.ceil(playerCor[1])} z;{math.ceil(playerCor[2])} xr;{math.ceil(playerRot[0])} yr;{math.ceil(playerRot[1])}",
        True,
        (255, 255, 255)
    )

    #load scene and config data
    read_config()
    load_scene(sceneName)

    #read key inputs
    keys = pygame.key.get_pressed()

    #misc controls
    if keys[pygame.K_ESCAPE]:
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
        grab = False

    #movement keys
    if keys[pygame.K_w]:
        playerCor[2] += 50 * dt
    if keys[pygame.K_a]:
        playerCor[0] -= 50 * dt
    if keys[pygame.K_s]:
        playerCor[2] -= 50 * dt
    if keys[pygame.K_d]:
        playerCor[0] += 50 * dt
    if keys[pygame.K_LSHIFT]:
        playerCor[1] += 50 * dt 
    if keys[pygame.K_SPACE]:
        playerCor[1] -= 50 * dt
    
    #event handler
    for event in pygame.event.get():

        #close out of window
        if event.type == pygame.QUIT:
            run = False

        #focus the window
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
            grab = True

    #draw section
    scr.fill((0, 0, 0))

    #print("Before projection:")
    #print(scene[:16])
    
    projection()

    if details == True:
        scr.blit(fpstext, (0, 0))
        scr.blit(xyztext, (0, 20))

    pygame.display.flip()

    # turn mouse pos into player rot theta
    dx, dy = pygame.mouse.get_rel()
    if grab == True:
        playerRot[1] -= dx * 0.2
        playerRot[0] += dy * 0.2
        if playerRot[0] >= 90 or playerRot[0] <= -90:
            playerRot[0] -= dy * 0.2
            
    #get delta time and fps
    dt = clock.tick(120) / 1000
    fps = clock.get_fps()

    #print(scene[3:6], scene[6:9], scene[9:12])
    #print(len(scene) % 16 == 0, scene.dtype)

pygame.quit()
