from random import random
import pygame
import math
import springmath
import boardstate
import particles

pygame.init()

movementDAS = 143
movementARR = 10
softdropSpeed = 20

score = 0
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

        angle = (angle0*aa + angleVel0*aw + math.pi)%(2*math.pi)-math.pi
        angleVel = angle0*wa + angleVel0*ww
        boardPos_x = bp_x0*pp + bv_x0*pv
        boardVel_x = bp_x0*vp + bv_x0*vv
        boardPos_y = bp_y0*pp + bv_y0*pv
        boardVel_y = bp_y0*vp + bv_y0*vv
    else:
        angle += (angleVel*dt + math.pi)%(2*math.pi)-math.pi
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
                pygame.draw.rect(rect_surf, pygame.Color(minoColor)+pygame.Color(122, 122, 115), pygame.Rect(i*size_y*.04,size_y*1.6-(j+1.2)*size_y*.04,size_y*.04,size_y*.04))

    currentPiece = boardstate.pieces[boardstate.pieceIndex]
    pos = boardstate.piecePos
    drop = boardstate.pieceDropPos
    rotCos, rotSin = boardstate.rotCosSin[boardstate.pieceRot]
    if not dead:
        for i in currentPiece[1]:
            pygame.draw.rect(rect_surf, pygame.Color(pygame.Color(currentPiece[0])+pygame.Color(122, 122, 115)).lerp("#FFFFFF",max(min(.25*(1-4*(pygame.time.get_ticks()/1000-autoLockTimer)*boardstate.pieceResting),1),0)).lerp("#000000",max(min(.4*(-1+4*(pygame.time.get_ticks()/1000-autoLockTimer)*boardstate.pieceResting),1),0)), pygame.Rect((pos[0]+i[0]*rotCos+i[1]*rotSin)*size_y*.04,size_y*1.6-(pos[1]-i[0]*rotSin+i[1]*rotCos+1.2)*size_y*.04,size_y*.04,size_y*.04))

    for j, row in enumerate(boardstate.boardState):
        for i, minoColor in enumerate(row):
            if minoColor is not None:
                pygame.draw.rect(rect_surf, minoColor, pygame.Rect(i*size_y*.04,size_y*1.6-(j+1)*size_y*.04,size_y*.04,size_y*.04))
    if not dead:
        for i in currentPiece[1]:
            pygame.draw.rect(rect_surf, currentPiece[0]+"20", pygame.Rect((drop[0]+i[0]*rotCos+i[1]*rotSin)*size_y*.04,size_y*1.6-(drop[1]-i[0]*rotSin+i[1]*rotCos+1)*size_y*.04,size_y*.04,size_y*.04))
        for i in currentPiece[1]:
            pygame.draw.rect(rect_surf, pygame.Color(currentPiece[0]).lerp("#FFFFFF",max(min(.25*(1-4*(pygame.time.get_ticks()/1000-autoLockTimer)*boardstate.pieceResting),1),0)).lerp("#000000",max(min(.4*(-1+4*(pygame.time.get_ticks()/1000-autoLockTimer)*boardstate.pieceResting),1),0)), pygame.Rect((pos[0]+i[0]*rotCos+i[1]*rotSin)*size_y*.04,size_y*1.6-(pos[1]-i[0]*rotSin+i[1]*rotCos+1)*size_y*.04,size_y*.04,size_y*.04))

    if len(boardstate.boardState) >= 16 and not dead:
        for i in boardstate.pieces[boardstate.pieceQueue[0]][1]:
            pygame.draw.line(rect_surf, "#ff4545", ((4+i[0]+.15)*size_y*.04,size_y*1.6-(20+i[1]+1-.15)*size_y*.04),((4+i[0]+1-.15)*size_y*.04,size_y*1.6-(20+i[1]+.15)*size_y*.04),width=6)
            pygame.draw.line(rect_surf, "#ff4545", ((4+i[0]+.15)*size_y*.04,size_y*1.6-(20+i[1]+.15)*size_y*.04),((4+i[0]+1-.15)*size_y*.04,size_y*1.6-(20+i[1]+1-.15)*size_y*.04),width=6)

    motionBlurSurf = pygame.Surface((size_y*.4, size_y*1.6),flags=pygame.SRCALPHA)

    for i in particles.getHardDropBlur():
        pygame.draw.rect(motionBlurSurf, i[0], pygame.Rect(
            size_y*0.04*i[1],
            size_y*(1.6-0.04(i[2]+1)),
            0.04,
            size_y*(1.6-0.04*(i[3]+1))
        ))

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
movementTimer = 0
autoLockTimer = pygame.time.get_ticks()/1000

running = True

def dropPiece():
    global angleVel, boardVel_x, boardVel_y, dead, autoLockTimer
    dropPosX,dropPosY = boardstate.impulseArea(boardstate.pieceDropPos,boardstate.pieceRot,(0,-1))
    dropPosY -= 9.5
    dropPosX -=4.5
    force = -5-.5*math.sqrt(boardstate.piecePos[1]-boardstate.pieceDropPos[1])
    boardcos, boardsin = math.cos(angle),math.sin(angle)
    if (dropPosX*dropPosX+dropPosY*dropPosY) != 0:
        angleVel += .04*force*(dropPosX)
    impulsex = 0
    impulsey = force
    boardVel_x += .04*(boardcos*impulsex-boardsin*impulsey)
    boardVel_y -= .04*(boardsin*impulsex+boardcos*impulsey)
    currentTime = pygame.time.get_ticks()/1000
    pieceIndex, pieceRot pieceShape, dropInfo, dead, clearNum, clearedLines, perfectClear, isTSpin= boardstate.lockPiece()
    particles.newHardDropBlur(pieceShape, dropInfo, currentTime, boardstate.pieces[pieceIndex][0])
    particleList = []
    for i in boardstate.impulseArea(dropInfo[1], pieceRot, (0,-1))[2]:
        posx, posy = i[0]-5,i[1]-10
        for i in range(random.randint(0,10)):
            particleList.append([
                (posx*boardcos-posy*boardsin,posx*boardsin+posy*boardcos),
                (random.guass(0,1)-1*boardsin,random.guass(0,1)+1*boardcos),
                random.random()*2,
                "#FFFFFF",
                random.uniform(.5,1)
            ])
    autoLockTimer = currentTime

while running:
    currentTime = pygame.time.get_ticks()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not dead:
                holdingRight = True
                movementTimer = currentTime*1000
                DASOver = False
                if boardstate.translate((1,0)) and boardstate.pieceResting: autoLockTimer = currentTime
            elif event.key == pygame.K_LEFT and not dead:
                holdingLeft = True
                movementTimer = currentTime*1000
                DASOver = False
                if boardstate.translate((-1,0)) and boardstate.pieceResting: autoLockTimer = currentTime
            elif event.key == pygame.K_DOWN and not dead:
                holdingDown = True
                moveDownAmount = int(softdropSpeed*(currentTime-gravityTimer)/(0.8-((level-1)*0.007))**(level-1))
                gravityTimer += moveDownAmount*(0.8-((level-1)*0.007))**(level-1)/softdropSpeed
            elif event.key == pygame.K_UP and not dead:
                rotInfo = boardstate.rotate(1)
                if rotInfo[0] and boardstate.pieceResting: autoLockTimer = currentTime
                if rotInfo[1] > 0:
                    size_x,size_y = screen.get_size()
                    angleVel -= .75
                    pos = boardstate.piecePos

                    boardcos, boardsin = math.cos(angle),math.sin(angle)
                    boardVel_x -= .75*(-.4+(pos[1]+.5)*.04)*math.cos(angle)
                    boardVel_y += .75*(-.2+(pos[0]+.5)*.04)*math.sin(angle)
            elif event.key == pygame.K_z and not dead:
                rotInfo = boardstate.rotate(-1)
                if rotInfo[0] and boardstate.pieceResting: autoLockTimer = currentTime
                if rotInfo[1] > 0:
                    size_x,size_y = screen.get_size()
                    angleVel += .75
                    pos = boardstate.piecePos

                    boardcos, boardsin = math.cos(angle),math.sin(angle)
                    boardVel_x += .75*(-.42+(pos[1]+.5)*.04)*math.cos(angle)
                    boardVel_y -= .75*(-.22+(pos[0]+.5)*.04)*math.sin(angle)
            elif event.key == pygame.K_c and not dead:
                dead = not boardstate.nextPiece(True)
            elif event.key == pygame.K_SPACE and not dead:
                dropPiece()
            elif event.key == pygame.K_r:
                dead=False
                angleVel += 10*((1-random.random()*2>0)*2-1)
                score = 0
                level = 1
                boardstate.startNewGame()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                holdingRight = False
            elif event.key == pygame.K_LEFT:
                holdingLeft = False
            elif event.key == pygame.K_DOWN:
                holdingDown = False
    if not dead:
        if holdingDown:
            moveDownAmount = softdropSpeed*(currentTime-gravityTimer)//(0.8-((level-1)*0.007))**(level-1)
            gravityTimer += moveDownAmount*(0.8-((level-1)*0.007))**(level-1)/softdropSpeed
        else:
            moveDownAmount = (currentTime-gravityTimer)//(0.8-((level-1)*0.007))**(level-1)
            gravityTimer += moveDownAmount*(0.8-((level-1)*0.007))**(level-1)

        moved = False
        moveSideAmount = 0
        if holdingLeft or holdingRight:
            if not DASOver and currentTime*1000-movementTimer > movementDAS:
                movementTimer += movementDAS
                DASOver = True
            if DASOver:
                moveSideAmount = (currentTime*1000-movementTimer)//movementARR
                movementTimer += moveSideAmount*movementARR
            
            for i in range(int(moveSideAmount)):
                if boardstate.translate((-holdingLeft+holdingRight,0)): moved = True

        for i in range(int(moveDownAmount)):
            if boardstate.translate((0,-1)): moved = True

        if moved: autoLockTimer = currentTime

        if currentTime-autoLockTimer>0.5 and boardstate.pieceResting:
            dropPiece()

    screen.fill("#24292e")
    update_board()

    pygame.display.update()