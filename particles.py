import math

hardDropSpeed = 500

hardDropBlurs = []
screenParticles = []

def newHardDropBlur(pieceShape, dropInfo, lifeBeginning, color):
    for i in pieceShape:
        hardDropBlurs.append(
            [
                (dropInfo[0][0]+i[0],dropInfo[0][1]+i[1]),
                (dropInfo[1][0]+i[0],dropInfo[1][1]+i[1]),
                lifeBeginning,
                math.sqrt((dropInfo[0][1]-dropInfo[1][1])/hardDropSpeed),
                0, # current position
                color
            ]
        )

def newScreenParticles(particles, lifeBeginning, drag=0.001, gravity=0):
    for i in particles:
        screenParticles.append(
            [
                i[1][0], # c_1 for x
                gravity/drag + i[1][1], # c_1 for y
                i[0][0] + i[1][0]/drag, # c_2 for x
                i[0][1] + (gravity/drag + i[1][2])/drag, # c_2 for y
                lifeBeginning,
                i[2], # lifespan
                i[3], # color
                i[4], # start transparency
                i[4], # current transparency
                i[0] # current position
            ]
        )

def updateParticles(newTime):
    hardDropBlurs = [i for i in hardDropBlurs if newTime-i[2] > i[3]]

    for i in hardDropBlurs:
        i[4] = hardDropSpeed*(newTime-i[2])**2
    
    for i in screenParticles:
        t = (newTime-i[4])
        i[9] = (
            -math.exp(-drag*t)*i[0]/drag + i[2],
            -gravity*t/drag-math.exp(-drag*t)*i[1]/drag + i[3]
        )
        i[8] = (x/i[5]-1)**2*(1-2*x/i[5])

def getHardDropBlur():
    return [[i[5], i[0][0], i[0][1]+i[5], i[0][1]-i[1][1]-i[5]] for i in getHardDropBlur]

def getScreenParticles():
    return [[i[9],i[8],i[6]] for i in screenParticles]