import math

EPS = 1e-4

def getSpringMatrix(freq,damp,dt):
    decay = math.exp(-damp*freq*dt)

    if (damp == 1):
        return (1 + freq*dt)*decay, dt*decay, -freq*freq*dt*decay, (1 - freq*dt)*decay
    elif (damp < 1):
        c = math.sqrt(1 - damp*damp)

        i = math.cos(freq*c*dt)
        j = math.sin(freq*c*dt)

        if (c > EPS):
            z = j/c
        else:
            a = dt*freq
            z = a + ((a*a)*(c*c)*(c*c)/20 - c*c)*(a*a*a)/6

        if (freq*c > EPS):
            y = j/(freq*c)
        else:
            b = freq*c
            y = dt + ((dt*dt)*(b*b)*(b*b)/20 - b*b)*(dt*dt*dt)/6

        return (i + damp*z)*decay, y*decay, -z*freq*decay, (i - z*damp)*decay
    else:
        # Hecc you why would you have it over 1?????
        print("WHYYYYYY >:(")