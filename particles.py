import math

drag = .1
gravity = 0

hardDropSpeed = 500

hardDropBlurs = []
screenParticles = []

def newHardDropBlur(pieceShape, dropInfo, lifeBeginning):
    for i in pieceShape:
        hardDropBlurs.append(
            [
                (dropInfo[0][0]+i[0],dropInfo[0][1]+i[1]),
                (dropInfo[1][0]+i[0],dropInfo[1][1]+i[1]),
                lifeBeginning,
                math.sqrt(dropInfo[1]/hardDropSpeed),
                0 # current position
            ]
        )

def newScreenParticles(particles, lifeBeginning):
    for i in particles:
        screenParticles.append(
            [
                i[1][0], # c_1 for x
                gravity/drag + i[1][1], # c_1 for y
                i[0][0] + i[1][0]/drag, # c_2 for x
                i[0][1] + (gravity/drag + i[1][2])/drag,
                lifeBeginning,
                i[2], # lifespan
                i[3], # color
                i[4], # transparency
                i[0] # current position
            ]
        )

def updateParticles(newTime):
    hardDropBlurs = [i for i in hardDropBlurs if newTime-i[2] > i[3]]

    for i in hardDropBlurs:
        i[4] = hardDropSpeed*(newTime-i[2])**2
    
    for i in screenParticles:
        t = (newTime-i[4])
        i[8] = (
            -math.exp(-drag*t)*i[0]/drag + i[2],
            -gravity*t/drag-math.exp(-drag*t)*i[1]/drag + i[3],
            (x/i[5]-1)**2*(1-2*x/i[5])
        )