from workWith12Gon import *
from point2D import *
from segmentIntersection import *
from billiard import *
from absqrtn import *
from fractions import *

import pygame, sys
from pygame.locals import *

# The problem is to reveal periodic components of not very big period...
# And the same be without, for example, "big rocket"

def makeColorFromHash(h):
    r = h % 256
    h /= 256
    g = h % 256
    h /= 256
    b = h % 256
    return (r, g, b)

def inputEvents(events):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        else:
            pass

def waitEnd():
    print('waiting for end', file=sys.stderr)
    while 1:
        inputEvents(pygame.event.get())

def getColor(n):
    #return ((148 + 462*n) % 256, (20 + 98 * n) % 256, (70 + 78 * n) % 256)
    return ((148 + 198*n) % 256, (20 + 23 * n) % 256, (70 + 5 * n) % 256)

def calculateCodeOfAperiodicFor8Gon(screen, iterations = 10000):
    c0 = MyPoint(Fraction(900), Fraction(100))
    c1 = MyPoint(Fraction(900), Fraction(1120))
    
    #WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE = 8
    
    raysColor = (47, 79, 79)
    polygon = Get8gonFromSegment(c0, c1)
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))


    zones = getZonesFrom8Gon(polygon)
    stableZones = getStableZonesFrom8Gon(polygon, zones)
  
    print("OK")

    index = -1
    O = polygon[1]
    K = lineIntersection(polygon[0], polygon[1], polygon[4], polygon[3])
    C = lineIntersection(polygon[1], polygon[2], polygon[4], polygon[3])
    M = C + C - polygon[2]
    for i in range(8):
        if isOnSegment(stableZones[1][i], O, K) and isOnSegment(stableZones[1][i-1], O, K):
            index = i-1

    gz = [stableZones[1][(j + index) % 8] for j in range(8)]

    coef = (C.GetX() - gz[4].GetX()) / (C.GetX() - O.GetX())
    
    gz2 = [compressVector(C, p, coef) for p in gz]

    ap = lineIntersection(O, gz2[0], M, gz2[7])

    app = ap
    DrawPoint(screen, ap, (255, 255, 255), 3)
    
    ans = ""
    
    for i in range(iterations):
        print(i)
        ap, r = MakeZoneOuterBilliardPair(ap, polygon)
        ans += str(r)

    

    DrawMyPolygon(screen, stableZones[0], raysColor, 2, (0, 120, 0))
    DrawMyPolygon(screen, stableZones[1], raysColor, 2, (120, 0, 0))
    DrawMyPolygon(screen, gz2, raysColor, 2, (120, 0, 0))
    DrawPoint(screen, app, (255, 255, 255), 3)
    DrawPoint(screen, gz2[2], (255, 255, 255), 6)
    DrawPoint(screen, gz2[1], (255, 255, 255), 6)
    DrawPoint(screen, O, (255, 255, 255), 6)
    DrawPoint(screen, M, (255, 255, 255), 6)

    pygame.image.save(screen, 'test.bmp')

    return ans

    waitEnd()


#def MakeZoneOuterBilliardPair(p, polygon, isInverse=False):




if __name__ == '__main__':
    pygame.init()
    size_x = 512 * 6
    size_y = 512 * 6
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    
    print(calculateCodeOfAperiodicFor8Gon(screen, 300))
    #drawPic3(screen)
    #drawPic6(screen)
    #drawPic4(screen)
    waitEnd()
