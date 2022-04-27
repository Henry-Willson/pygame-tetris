import math

drag = .1
hardDropSpeed = 500

hardDropParticles = []
screenParticles = []

def newHardDropParticle(pieceShape, dropInfo, lifeBeginning):
    for i in pieceShape:
        hardDropParticles.append(
            [
                (dropInfo[0][0]+i[0],dropInfo[0][1]+i[1]),
                (dropInfo[1][0]+i[0],dropInfo[1][1]+i[1]),
                lifeBeginning,
                math.sqrt(dropInfo[1]/hardDropSpeed),
                0
            ]
        )

def newScreenParticles():
    print("yea")

def updateParticles(newTime):
    hardDropParticles = [i for i in hardDropParticles if newTime-i[2] > i[3]]

    for i in hardDropParticles:
        i[4] = hardDropSpeed*(newTime-i[2])**2