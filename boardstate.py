import random

JLSTZOffset = [
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
	[(0, 0), (1, 0), (1,-1), (0, 2), (1, 2)],
	[(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
	[(0, 0), (-1, 0), (-1,-1), (0, 2), (-1, 2)]
]

pieces = [
    [ # I piece
        "#00fcff",
        [(-1,0),(0,0),(1,0),(2,0)],
        [
            [(0, 0),(-1, 0),(2, 0),(-1, 0),(2, 0)],
            [(-1, 0),(0, 0),(0, 0),(0, 1),(0,-2)],
            [(-1, 1),(1, 1),(-2, 1),(1, 0),(-2, 0)],
            [(0, 1),(0, 1),(0, 1),(0, 1),(0, 2)]
        ]
    ],
    [ # J Piece
        "#00aaff",
        [(-1,0),(-1,1),(0,0),(1,0)],
        JLSTZOffset
    ],
    [ # L Piece
        "#ff9400",
        [(-1,0),(0,0),(1,0),(1,1)],
        JLSTZOffset
    ],
    [ # O Piece
        "#ffe600",
        [(0,0),(0,1),(1,0),(1,1)],
        [
            [(0,0)],
            [(0,-1)],
            [(-1,-1)],
            [(-1,0)]
        ]
    ],
    [ # S Piece
        "#00f600",
        [(-1,0),(0,0),(0,1),(1,1)],
        JLSTZOffset
    ],
    [ # T Piece
        "#ff40ff",
        [(-1,0),(0,0),(0,1),(1,0)],
        JLSTZOffset
    ],
    [ # Z Piece
        "#ff0051",
        [(-1,1),(0,0),(0,1),(1,0)],
        JLSTZOffset
    ]
]

rotCosSin = [(1,0),(0,1),(-1,0),(0,-1)] # CW

boardState = [
]

bag = [i for i in range(len(pieces))]

piecePos = (4,20)
pieceRot = 0
pieceIndex = bag.pop(random.randint(0,len(bag)-1))
pieceDropPos = (0,0)
pieceResting = False

pieceQueue = [bag.pop(random.randint(0,len(bag)-1)),bag.pop(random.randint(0,len(bag)-1)),bag.pop(random.randint(0,len(bag)-1))]
hold = None

def minoVacant(pos):
    return  pos[0] >= 0 and pos[0] < 10 and pos[1] >= 0 and (pos[1] >= len(boardState) or boardState[pos[1]][pos[0]] == None)

def isPosValid(pos, rotation):
    rotCos, rotSin = rotCosSin[rotation]
    for i in pieces[pieceIndex][1]:
        if not minoVacant((pos[0]+i[0]*rotCos+i[1]*rotSin,pos[1]-i[0]*rotSin+i[1]*rotCos)):
            return False
    return True

def rotate(dir):
    global pieceRot, piecePos
    newRot = (pieceRot+dir)%4
    for i,v in enumerate(pieces[pieceIndex][2][pieceRot]):
        newPos = (piecePos[0]+v[0]-pieces[pieceIndex][2][newRot][i][0],piecePos[1]+v[1]-pieces[pieceIndex][2][newRot][i][1])
        if isPosValid(newPos, newRot):
            piecePos = newPos
            pieceRot = newRot
            updateRestingState()
            if pieceIndex != 5:
                return True, 0
            else: # T spin classification
                rotCos, rotSin = rotCosSin[pieceRot]
                aCorner = not minoVacant((newPos[0]-1*rotCos+1*rotSin,newPos[1]+1*rotSin+1*rotCos))
                bCorner = not minoVacant((newPos[0]+1*rotCos+1*rotSin,newPos[1]-1*rotSin+1*rotCos))
                cCorner = not minoVacant((newPos[0]-1*rotCos-1*rotSin,newPos[1]+1*rotSin-1*rotCos))
                dCorner = not minoVacant((newPos[0]+1*rotCos-1*rotSin,newPos[1]-1*rotSin-1*rotCos))
                return True, (aCorner+bCorner+cCorner+dCorner>=3)+(aCorner and bCorner and (cCorner or dCorner))
    return False, 0

def translate(dir):
    global piecePos
    newPos = (piecePos[0]+dir[0],piecePos[1]+dir[1])
    if isPosValid(newPos, pieceRot):
        piecePos = newPos
        updateRestingState()
        return True
    else:
        return False

def updateRestingState():
    piecePosX = piecePos[0]
    newPieceDropPosY = piecePos[1]

    while isPosValid((piecePosX,newPieceDropPosY-1),pieceRot):
        newPieceDropPosY -= 1
    
    global pieceDropPos,pieceResting
    pieceDropPos = (piecePosX,newPieceDropPosY)
    pieceResting = pieceDropPos==piecePos

def lockPiece():
    rotCos, rotSin = rotCosSin[pieceRot]
    pieceColor = pieces[pieceIndex][0]

    gameOver = True

    for i in pieces[pieceIndex][1]:
        mino_x = pieceDropPos[0]+i[0]*rotCos+i[1]*rotSin
        mino_y = pieceDropPos[1]-i[0]*rotSin+i[1]*rotCos

        gameOver = gameOver and mino_y >= 20

        if mino_y >= len(boardState):
            for _ in range(len(boardState),mino_y+1):
                boardState.append([None for _ in range(10)])

        boardState[mino_y][mino_x] = pieceColor
    
    clearedLines = []
    linesCleared = 0

    for j in range(len(boardState)):
        cleared = True
        for i in range(10):
            cleared = cleared and boardState[j-linesCleared][i] is not None
        if cleared == True:
            del boardState[j-linesCleared]
            linesCleared += 1
            clearedLines.append(j)

    return gameOver or not nextPiece(), linesCleared, len(boardState)== 0

def nextPiece(isHold=False):
    global piecePos, pieceRot, pieceIndex, hold, bag
    piecePos = (4,20)
    pieceRot = 0
    
    if isHold and hold is not None:
        newhold = pieceIndex
        pieceIndex = hold
        hold = newhold
    else:
        if isHold:
            hold = pieceIndex
        
        pieceIndex = pieceQueue.pop(0)
        
        if len(bag) == 0:
            bag = [i for i in range(len(pieces))]
        pieceQueue.append(bag.pop(random.randint(0,len(bag)-1)))

    for i in pieces[pieceIndex][1]:
        if not minoVacant((4+i[0],20+i[1])):
            return False

    updateRestingState()
    return True

def impulseArea(pos, rotation, dir):
    rotCos, rotSin = rotCosSin[rotation]
    impulsePosX = 0
    impulsePosY = 0
    weights = 0
    for i in pieces[pieceIndex][1]:
        if not minoVacant((pos[0]+dir[0]+i[0]*rotCos+i[1]*rotSin,pos[1]+dir[1]-i[0]*rotSin+i[1]*rotCos)):
            impulsePosX += pos[0]+dir[0]+i[0]*rotCos+i[1]*rotSin
            impulsePosY += pos[1]+dir[1]-i[0]*rotSin+i[1]*rotCos
            weights += 1

    return impulsePosX/weights+dir[0]/2, impulsePosY/weights+dir[1]/2

def startNewGame():
    global bag, piecePos, pieceRot, pieceResting, pieceQueue, pieceIndex, hold
    boardState = []

    bag = [i for i in range(len(pieces))]

    piecePos = (4,20)
    pieceRot = 0
    pieceIndex = bag.pop(random.randint(0,len(bag)-1))

    pieceQueue = [bag.pop(random.randint(0,len(bag)-1)),bag.pop(random.randint(0,len(bag)-1)),bag.pop(random.randint(0,len(bag)-1))]
    hold = None

    updateRestingState()