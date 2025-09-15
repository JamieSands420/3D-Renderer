import pygame

width = 900
height = 900
scr = pygame.display.set_mode((width, height))

def projection(obj):
    
    for i in range(len(obj.vertexes)):
        tempX = obj.vertexes[i][0] + obj.x - playerCor[0]
        tempY = obj.vertexes[i][1] + obj.y - playerCor[1]
        tempZ = obj.vertexes[i][2] + obj.z - playerCor[2]
        
        #avoids division by 0 and flipping of rendering
        if tempZ <= 0.0000000000000000000000001:
            tempZ = 0.0000000000000000000000001

        obj.projected_vertexes[i][0] = tempX/tempZ + width/2
        obj.projected_vertexes[i][1] = tempY/tempZ + height/2
        
class triangle():

    def __init__(self, x=0, y=0, z=0, L = (-1, 0, 0), T = (0, -2, 0), R = (1, 0, 0)):

        self.x = x
        self.y = y
        self.z = z
        
        size = 10

        self.vertexes = [
            [L[0]*size, L[1], L[2]], #left vertex
            [T[0], T[1]*size, T[2]], #middle vertex
            [R[0]*size, R[1], R[2]]  #right vertex
            ]

        self.projected_vertexes = [
            [0, 0],
            [0, 0], 
            [0, 0]
            ]

        self.constructor = [0, 1, 2, 0]
        #constructor tells program what verts are connected

    def draw_triangle(self):

        # go through each constructor and draw the lines together
        projection(self)
        for i in range(3):
            pygame.draw.line(scr, (255, 0, 0), (self.projected_vertexes[self.constructor[i]][0], self.projected_vertexes[self.constructor[i]][1]), (self.projected_vertexes[self.constructor[i+1]][0], self.projected_vertexes[self.constructor[i+1]][1]), 5)

tr1 = triangle(z=1)
tr2 = triangle(x=10, z=1, L = (-1, -20, 0), T = (0, 0, 0), R = (1, -20, 0))

playerCor = [0, 0, 0]

pygame.init()
run = True
while run:

    #movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerCor[2] += 0.0005
    if keys[pygame.K_a]:
        playerCor[0] -= 0.1
    if keys[pygame.K_s]:
        playerCor[2] -= 0.0005
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

    tr1.draw_triangle()
    tr2.draw_triangle()

    pygame.display.flip()
    #drawing section, update screen

pygame.quit()
