import pygame
from pygame.locals import *
from sys import exit
import numpy as np
import GravitySimulator as GS

size = 1000
ww = 1920
wh = 1080
pathsize = 100
scale = 3.0

dt = 0.5
g = 10


# super parameters
Create_mode = False
add_flag = False

# used to adding body
C_x = 0
C_y = 0
C_vx =0
C_vy = 0
C_M = 10.0

# some parameters used for display and trace
show_abs_path = True
max_index = -1
TraceMax = True

selectIndex = 0
LastSelectX = ww/2
LastSelectY = wh/2
TraceSelect = False

cursorX = ww/2
cursorY = wh/2

STOP = False

# init bodies
X = (np.random.rand(size)*0.8 + 0.1)*ww/scale
Y = (np.random.rand(size)*0.8 + 0.1)*wh/scale
M = (np.random.rand(size)+0.2)*10
VX = (np.random.rand(size) - 0.5)*10
VY = (np.random.rand(size) - 0.5)*10

pathX = np.zeros((size,pathsize))
pathY = np.zeros((size,pathsize))

for i in range(size):
    for j in range(pathsize):
        pathX[i][j] = X[i]
        pathY[i][j] = Y[i]

# Transfer coordinate from game to screen
def Transfer(x,y):
    if TraceMax:
        return (x - X[max_index])*scale + cursorX , (y-Y[max_index])*scale + cursorY
    if TraceSelect:
        return (x - X[selectIndex])*scale + cursorX , (y-Y[selectIndex])*scale + cursorY
    return (x - LastSelectX)*scale + cursorX , (y-LastSelectY)*scale + cursorY

# Transfer screen from game to screen coordinate
def TransferBack(x,y):
    if TraceMax:
        return (x - cursorX)/scale + X[max_index]  , (y - cursorY)/scale + Y[max_index]
    if TraceSelect:
        return (x - cursorX)/scale + X[selectIndex]  , (y - cursorY)/scale + Y[selectIndex]
    return (x - cursorX)/scale + LastSelectX , (y - cursorY)/scale + LastSelectY

# Predict the orbit of a body
def PredictPath(screen,x,y,vx,vy,m,size = 500):
    DT = dt / scale ** 0.5
    SIZE = len(M)
    ans = []
    xx = x
    yy = y
    vxx = vx
    vyy = vy
    for k in range(size):
        for i in range(SIZE):
            dx = X[i] - x
            dy = Y[i] - y
            sqL1 = dx * dx + dy * dy
            L = sqL1**0.5
            alpha = L * L * L
            dx /= alpha
            dy /= alpha
            accx = g * dx
            accy = g * dy
            vx += (M[i] * accx) * DT * 0.5
            vy += (M[i] * accy) * DT * 0.5
        x += vx * DT
        y += vy * DT
        ans.append([x,y])
    a, b = Transfer(xx,yy)
    pygame.draw.circle(screen, (255, 255, 255), (int(a), int(b)), int(scale *0.5* m ** 0.5))
    pygame.draw.line(screen,(255, 255, 255),(int(a),int(b)),(int(a+vxx*10*scale**0.5),int(b+vyy*10*scale**0.5)))
    for i,p in enumerate(ans):
        a,b = Transfer(p[0],p[1])
        screen.set_at([int(a), int(b)], [int(i*155.0/size + 100), 200, 175])

# get id of the body which is being traced
def getTraceId():
    if TraceMax:
        return max_index
    if TraceSelect:
        return selectIndex
    return -1

# show path of the body
def showpath(path_iter,screen,i):
    for j in range(pathsize):
        if show_abs_path:
            x , y  = Transfer(pathX[i][j],pathY[i][j])
            screen.set_at([int(x), int(y)], [185, 200, 165])
        else:
            # show relative_path
            if TraceMax:
                x = (pathX[i][j] - pathX[max_index][j]) * scale + cursorX
                y = (pathY[i][j] - pathY[max_index][j]) * scale + cursorY
            elif TraceSelect:
                x = (pathX[i][j] - pathX[selectIndex][j]) * scale + cursorX
                y = (pathY[i][j] - pathY[selectIndex][j]) * scale + cursorY
            else:
                x =(pathX[i][j] - LastSelectX) * scale + cursorX
                y =(pathY[i][j] - LastSelectY) * scale + cursorY

            screen.set_at([int(x), int(y)], [200, 255, 255])

def move():
    Size = len(M)
    for i in range(Size):
        X[i] += VX[i]*dt
        Y[i] += VY[i]*dt

        pathX[i][path_iter] = X[i]
        pathY[i][path_iter] = Y[i]

def draw(screen,path_iter):
    Size = len(M)
    for i in range(Size):
        x = X[i]
        y = Y[i]
        x, y = Transfer(x, y)
        pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), int(0.5 * scale * M[i] ** 0.5))
        showpath(path_iter,screen,i)

# init pygame
pygame.init()

screen = pygame.display.set_mode((ww, wh), flags = FULLSCREEN,depth=32)

pygame.display.set_caption("simulation")
path_iter = 0

# the main loop of the game
while True:
    # event handler
    for event in pygame.event.get():
        if Create_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    add_flag = False
                    Create_mode = False
                    STOP = False
                if event.key == pygame.K_y and add_flag:
                    index = getTraceId()
                    a = 0
                    b = 0
                    if index>0:
                        a = VX[index]
                        b = VY[index]
                    X = np.append(X, C_x)
                    Y = np.append(Y, C_y)
                    VX = np.append(VX, C_vx + a)
                    VY = np.append(VY, C_vy + b)
                    M = np.append(M,C_M)
                    C_pathX = np.zeros((1,pathsize))
                    C_pathY = np.zeros((1,pathsize))
                    pathX = np.append(pathX, C_pathX, axis=0)
                    pathY = np.append(pathY, C_pathY, axis=0)
                    C_x = 0
                    C_y = 0
                    C_vx = 0
                    C_vy = 0
                    C_M = 10
                    add_flag = False
                    Create_mode = False
                    STOP = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    C_vx = 0
                    C_vy = 0
                    add_flag = True
                    C_x , C_y = TransferBack(event.pos[0],event.pos[1])
                elif add_flag and event.button == 4:
                    C_M *=1.1
                elif add_flag and event.button == 5:
                    C_M /=1.1
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:
                    C_vx += event.rel[0] / (10.0 *scale**0.5)
                    C_vy += event.rel[1] / (10.0 *scale**0.5)
        else:
            if event.type == QUIT:
                # 接收到退出时间后退出程序
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pygame.K_SPACE:
                    if TraceMax:
                        LastSelectX = X[max_index]
                        LastSelectY = Y[max_index]
                    elif TraceSelect:
                        LastSelectX = X[selectIndex]
                        LastSelectY = Y[selectIndex]
                    TraceMax = False
                    TraceSelect = False
                elif event.key == pygame.K_s:
                    STOP = not STOP
                elif event.key == pygame.K_o:
                    show_abs_path = not show_abs_path
                elif event.key == pygame.K_a:
                    Create_mode = True
                    STOP = True
                elif event.key == pygame.K_UP:
                    dt *= 1.1
                elif event.key == pygame.K_DOWN:
                    dt /= 1.1
                elif event.key == pygame.K_m:
                    if not TraceMax:
                        cursorX, cursorY = Transfer(X[max_index],Y[max_index])
                        TraceMax = True
                        TraceSelect = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    scale /=1.2
                elif event.button == 4:
                    scale *=1.2
                elif event.button == 3:
                    x = event.pos[0]
                    y = event.pos[1]
                    if TraceMax:
                        x = (x - cursorX) / scale + X[max_index]
                        y = (y - cursorY) / scale + Y[max_index]
                    elif TraceSelect:
                        x = (x - cursorX) / scale + X[selectIndex]
                        y = (y - cursorY) / scale + Y[selectIndex]
                    else:
                        x = (x - cursorX) / scale + LastSelectX
                        y = (y - cursorY) / scale + LastSelectY
                    len_M = len(M)
                    for i in range(len_M):
                        dx = X[i] - x
                        dy = Y[i] - y
                        if dx*dx + dy*dy <= M[max_index]/scale:
                            if selectIndex == i and TraceSelect:
                                break
                            LastSelectX = X[selectIndex]
                            LastSelectY = Y[selectIndex]
                            selectIndex = i
                            cursorX = event.pos[0]
                            cursorY = event.pos[1]
                            TraceSelect = True
                            TraceMax = False
                            break
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]==1:
                    cursorX += event.rel[0]
                    cursorY += event.rel[1]
    # event handler end

    # draw a frame
    draw(screen,path_iter)

    if add_flag:
        PredictPath(screen,C_x,C_y,C_vx,C_vy,C_M)

    if not STOP:
        path_iter+=1
        if(path_iter == pathsize):
            path_iter = 0

        # core function to simulate a step, using C to accelerate
        selectIndex = GS.next_step_2d(X,Y,VX,VY,M,dt,g,size,selectIndex)
        move()

        # remove some bodies which have been absorbed
        iter = 0
        while(iter<size):
            if M[iter] == 0.0:
                X=np.delete(X, iter)
                Y=np.delete(Y, iter)
                VX=np.delete(VX, iter)
                VY=np.delete(VY, iter)
                M=np.delete(M, iter)
                pathX = np.delete(pathX, iter,axis=0)
                pathY = np.delete(pathY, iter,axis=0)
                size -=1
                iter -=1
                if TraceSelect and selectIndex > iter:
                    selectIndex -= 1
            iter += 1

        # # this part is used for generating bodies automatically
        # if size<10:
        #     dx = np.random.random() - 0.5
        #     dy = np.random.random() - 0.5
        #     if abs(dx)<0.1:
        #         if dx > 0:
        #             dx += 0.1
        #         else:
        #             dx -= 0.1
        #     if abs(dy)<0.1:
        #         if dy > 0:
        #             dy += 0.1
        #         else:
        #             dy -= 0.1
        #     X = np.append(X, X[max_index] + dx*500)
        #     Y = np.append(Y, Y[max_index] + dy*500)
        #     VX = np.append(VX, -2.0/dy)
        #     VY = np.append(VY, 2.0/dx)
        #     M = np.append(M, 1)
        #     C_pathX = np.zeros((1, pathsize))
        #     C_pathY = np.zeros((1, pathsize))
        #     pathX = np.append(pathX, C_pathX, axis=0)
        #     pathY = np.append(pathY, C_pathY, axis=0)
        #     size +=1

        # select max
        max = -1
        for i in range(len(M)):
            if M[i]>max:
                max = M[i]
                max_index = i
    # update display
    pygame.display.update()
    screen.fill((0,0,0))