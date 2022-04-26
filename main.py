from random import random
import pygame
import math
import springmath
import boardstate

pygame.init()

movementDAS = 143
movementARR = 10
softdropSpeed = 20

level = 1

screen = pygame.display.set_mode((800,600),flags=pygame.RESIZABLE)

icon = pygame.image.load('doggy_icon.png')
pygame.display.set_caption("Yo wassup")
pygame.display.set_icon(icon)

angle = math.pi/2
angleVel = 0

boardPos_x,boardPos_y = 1,2
boardVel_x,boardVel_y = 5,-5

dead = False
lastTime = pygame.time.get_ticks()/10000

def updateBoardPosAndRotation():
    global angle, angleVel, boardPos_x, boardPos_y, boardVel_x, boardVel_y, lastTime
    dt = pygame.time.get_ticks()/1000-lastTime
    lastTime += dt

    angle0 = angle
    angleVel0 = angleVel
    bp_x0,bp_y0 = boardPos_x, boardPos_y
    bv_x0,bv_y0 = boardVel_x ,boardVel_y

    if (not dead):
        aa,aw,wa,ww = springmath.getSpringMatrix(8,.3,dt)
        pp,pv,vp,vv = springmath.getSpringMatrix(6,.5,dt)

        angle = angle0*aa + angleVel0*aw
        angleVel = angle0*wa + angleVel0*ww
        boardPos_x = bp_x0*pp + bv_x0*pv
        boardVel_x = bp_x0*vp + bv_x0*vv
        boardPos_y = bp_y0*pp + bv_y0*pv
        boardVel_y = bp_y0*vp + bv_y0*vv
    else:
        angle += angleVel*dt
        boardPos_x += boardVel_x*dt

        boardPos_y += dt*dt + boardVel_y*dt
        boardVel_y += 2*dt

def update_board():
    updateBoardPosAndRotation()
    size_x,size_y = screen.get_size()

    rect_surf = pygame.Surface((size_y*.4, size_y*1.6),flags=pygame.SRCALPHA)
    
    pygame.draw.rect(rect_surf,"#181b20",pygame.Rect(0,size_y*.8,size_y*.4,size_y*.8))

    for i in range(1,10):
        pygame.draw.line(
            rect_surf,"#1f2428",(i*.4/10*size_y,size_y*.8),(i*.4/10*size_y,size_y*1.6),width=2)
    for i in range(1,20):
        pygame.draw.line(rect_surf,"#1f2428",(0,(i/20+1)*.8*size_y),(size_y*.4,(i/20+1)*.8*size_y),width=2)

    
    for j, row in enumerate(boardstate.boardState):
        for i, minoColor in enumerate(row):
            if minoColor is not None:
                pygame.draw.rect(rect_surf, minoColor, pygame.Rect(i*size_y*.04,size_y*1.6-(j+1)*size_y*.04,size_y*.04,size_y*.04))
    
    currentPiece = boardstate.pieces[boardstate.pieceIndex]
    pos = boardstate.piecePos
    drop = boardstate.pieceDropPos
    rotCos, rotSin = boardstate.rotCosSin[boardstate.pieceRot]
    for i in currentPiece[1]:
        pygame.draw.rect(rect_surf, currentPiece[0]+"20", pygame.Rect((drop[0]+i[0]*rotCos+i[1]*rotSin)*size_y*.04,size_y*1.6-(drop[1]-i[0]*rotSin+i[1]*rotCos+1)*size_y*.04,size_y*.04,size_y*.04))
    for i in currentPiece[1]:
        pygame.draw.rect(rect_surf, currentPiece[0], pygame.Rect((pos[0]+i[0]*rotCos+i[1]*rotSin)*size_y*.04,size_y*1.6-(pos[1]-i[0]*rotSin+i[1]*rotCos+1)*size_y*.04,size_y*.04,size_y*.04))


    rect_surf = pygame.transform.rotate(rect_surf,math.degrees(angle))
    offset_x,offset_y = rect_surf.get_size()
    offset_x = -0.5*offset_x+size_x/2 - .4*size_y*math.sin(angle) + boardPos_x*size_y
    offset_y = -0.5*offset_y+size_y/2 - .4*size_y*math.cos(angle) + boardPos_y*size_y

    screen.blit(rect_surf,(offset_x,offset_y))

holdingLeft = False
holdingRight = False
holdingDown = False

DASOver = False
gravityTimer = pygame.time.get_ticks()/1000
movementDASTimer = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                holdingRight = True
                boardstate.translate((1,0))
            elif event.key == pygame.K_LEFT:

                holdingLeft = True
                boardstate.translate((-1,0))
            elif event.key == pygame.K_DOWN:
                holdingDown = True
                currentTime = pygame.time.get_ticks()/1000
                moveDownAmount = int(softdropSpeed*(currentTime-gravityTimer)/(0.8-((level-1)*0.007))**(level-1))
                gravityTimer += moveDownAmount*(0.8-((level-1)*0.007))**(level-1)/softdropSpeed
            elif event.key == pygame.K_UP:
                rotInfo = boardstate.rotate(1)
                if rotInfo[1] > 0:
                    size_x,size_y = screen.get_size()
                    angleVel -= .75
                    pos = boardstate.piecePos

                    boardcos, boardsin = math.cos(angle),math.sin(angle)
                    boardVel_x -= .75*(-.4+(pos[1]+.5)*.04)*math.cos(angle)
                    boardVel_y += .75*(-.2+(pos[0]+.5)*.04)*math.sin(angle)
            elif event.key == pygame.K_z:
                rotInfo = boardstate.rotate(-1)
                if rotInfo[1] > 0:
                    size_x,size_y = screen.get_size()
                    angleVel += .75
                    pos = boardstate.piecePos

                    boardcos, boardsin = math.cos(angle),math.sin(angle)
                    boardVel_x += .75*(-.42+(pos[1]+.5)*.04)*math.cos(angle)
                    boardVel_y -= .75*(-.22+(pos[0]+.5)*.04)*math.sin(angle)
            elif event.key == pygame.K_c:
                boardstate.nextPiece(True)
            elif event.key == pygame.K_SPACE:
                dead = boardstate.lockPiece()[0]
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                holdingRight = False
            elif event.key == pygame.K_LEFT:
                holdingLeft = False
            elif event.key == pygame.K_DOWN:
                holdingDown = False

    currentTime = pygame.time.get_ticks()/1000
    if holdingDown:
        moveDownAmount = int(softdropSpeed*(currentTime-gravityTimer)/(0.8-((level-1)*0.007))**(level-1))
        gravityTimer += moveDownAmount*(0.8-((level-1)*0.007))**(level-1)/softdropSpeed
    else:
        moveDownAmount = int((currentTime-gravityTimer)/(0.8-((level-1)*0.007))**(level-1))
        gravityTimer += moveDownAmount*(0.8-((level-1)*0.007))**(level-1)

    for i in range(moveDownAmount):
        boardstate.translate((0,-1))

    screen.fill("#24292e")
    update_board()

    pygame.display.update()