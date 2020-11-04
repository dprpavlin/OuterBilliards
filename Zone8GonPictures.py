from workWith12Gon import *
from point2D import *
from segmentIntersection import *
from billiard import *
from absqrtn import *
from fractions import *

import pygame, sys
from pygame.locals import *

# WORKING ON def PaintPeriodicComponentsFor8(screen):

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


def findGcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x

def paintPicBaseAngleRaw(screen):
   
    #polygon = Get8gonFromSegment(c0, c1)
    polygon = [MyPoint(Fraction(120), Fraction(200)),
               MyPoint(Fraction(420), Fraction(100)),
               MyPoint(Fraction(520), Fraction(300)),
               MyPoint(Fraction(320), Fraction(600)),
               MyPoint(Fraction(120), Fraction(500))
              ]
               
    DrawMyPolygon(screen, polygon, (0, 0, 180), 0)
    DrawMyPolygon(screen, polygon, (57, 179, 218), 2)

    raysColor = (57, 179, 218)
    for i in range(0, len(polygon)):
        DrawRayMyPoint(screen, polygon[i-1], polygon[i], raysColor, 2)

    pygame.image.save(screen, 'picBaseAngleRaw.bmp')
    pygame.display.flip()

def paintPicEnterZRaw(screen): 
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(1200), Fraction(1240))
    c1 = MyPoint(Fraction(1200), Fraction(1540))
    polygon = Get8gonFromSegment(c0, c1)
    
    raysColor = (57, 179, 218)
    zpol = []
    for i in range(0, 8):
        c = lineIntersection(polygon[i], polygon[i-1], polygon[i+1-8], polygon[i+2-8])
        npol = [reflect(p, c) for p in polygon]
        DrawMyPolygon(screen, npol, (0, 0, 120), 0)
        DrawMyPolygon(screen, npol, raysColor, 2)
        for j in range(i+2, i-1, -1):
            zpol.append(npol[j % 8])
    
    DrawMyPolygon(screen, zpol, (0, 120, 0), 0)
    DrawMyPolygon(screen, zpol, raysColor, 2)
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    DrawMyPolygon(screen, polygon, raysColor, 2)
    for i in range(0, 8):
        DrawLineMyPoint(screen, polygon[i], polygon[i-1], raysColor, 2)
    
    pygame.image.save(screen, 'picEnterZRaw.bmp')
    pygame.display.flip()

def paintPicInducedT(screen): 
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(1200), Fraction(1440))
    c1 = MyPoint(Fraction(1200), Fraction(1740))
    polygon = Get8gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)

    c = lineIntersection(polygon[1], polygon[2], polygon[4], polygon[3])
    pol2 = [reflect(p, c) for p in polygon]
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    DrawMyPolygon(screen, pol2, (0, 0, 120), 0)
    
    for i in range(0, 8):
        c = lineIntersection(polygon[i], polygon[i-1], polygon[i+1-8], polygon[i+2-8])
        npol = [reflect(p, c) for p in polygon]
        DrawMyPolygon(screen, npol, (0, 0, 120), 0)
        DrawMyPolygon(screen, npol, raysColor, 2)

    firstComponent = getFirstComponent(polygon)
    DrawMyPolygon(screen, firstComponent, (120, 120, 0), 0)
    zones = getZonesFrom8Gon(polygon) 
    center = (polygon[0] + polygon[4]) / MyCipher(2)
    for i in range(0, 8):
        DrawMyPolygon(screen, zones[0], (255, 69, 0), 0)
        DrawMyPolygon(screen, zones[1], (255, 215, 0), 0)
        DrawMyPolygon(screen, zones[2], (0, 255, 0), 0)
        for j in range(0, 3):
            DrawMyPolygon(screen, zones[j], raysColor, 2)
            zones[j] = [rotate45ClockwiseAround(p, center) for p in zones[j]]

    #DrawRayMyPoint(screen, polygon[2], polygon[1], raysColor, 2)
    #DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 2)
    #DrawMyPolygon(screen, firstComponent, raysColor, 3)
    #DrawMyPolygon(screen, polygon, raysColor, 3)

    pygame.image.save(screen, 'picInducedT-A.bmp')
    pygame.display.flip()

    for i in range(0, 3):
        zones[i] = MakeZoneOuterBilliard(zones[i], polygon, needCompress = True, isInverse = False)

    
    for i in range(0, 8):
        DrawMyPolygon(screen, zones[0], (255, 69, 0), 0)
        DrawMyPolygon(screen, zones[1], (255, 215, 0), 0)
        DrawMyPolygon(screen, zones[2], (0, 255, 0), 0)
        for j in range(0, 3):
            DrawMyPolygon(screen, zones[j], raysColor, 2)
            zones[j] = [rotate45ClockwiseAround(p, center) for p in zones[j]]

    pygame.image.save(screen, 'picInducedT-B.bmp')
    pygame.display.flip()

def paintPicInducedTBig(screen): 
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(1200), Fraction(1440))
    c1 = MyPoint(Fraction(1200), Fraction(1740))
    polygon = Get8gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)

    center = (polygon[0] + polygon[4]) / MyCipher(2)
    zones = getZonesFrom8GonBig(polygon)

    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)
    DrawRayMyPoint(screen, polygon[5], polygon[4], raysColor, 2)

    for i in range(0, 8):
        DrawMyPolygon(screen, zones[0], (255, 69, 0), 0)
        DrawMyPolygon(screen, zones[1], (255, 215, 0), 0)
        DrawMyPolygon(screen, zones[2], (0, 255, 0), 0)
        DrawMyPolygon(screen, zones[3], (0, 255, 255), 0)
        for j in range(0, 4):
            DrawMyPolygon(screen, zones[j], raysColor, 2)
            zones[j] = [rotate45ClockwiseAround(p, center) for p in zones[j]]

    
    pygame.image.save(screen, 'picInducedTBig-A.bmp')
    pygame.display.flip()
    
    
    for i in range(0, 4):
        zones[i] = MakeZoneOuterBilliard(zones[i], polygon, needCompress = True, isInverse = False)
    
    for i in range(0, 8):
        DrawMyPolygon(screen, zones[0], (255, 69, 0), 0)
        DrawMyPolygon(screen, zones[1], (255, 215, 0), 0)
        DrawMyPolygon(screen, zones[2], (0, 255, 0), 0)
        DrawMyPolygon(screen, zones[3], (0, 255, 255), 0)
        for j in range(0, 4):
            DrawMyPolygon(screen, zones[j], raysColor, 2)
            zones[j] = [rotate45ClockwiseAround(p, center) for p in zones[j]]

    pygame.image.save(screen, 'picInducedTBig-B.bmp')
    pygame.display.flip()

def paintPicInducedTBigShift(screen): 
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(1200), Fraction(1440))
    c1 = MyPoint(Fraction(1200), Fraction(1740))
    polygon = Get8gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)

    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)
    DrawRayMyPoint(screen, polygon[5], polygon[4], raysColor, 2)
    
    center = (polygon[0] + polygon[4]) / MyCipher(2)
    ukp = intersectLines(polygon[1], polygon[2], polygon[3], polygon[4])
    pol2 = [reflect(p, ukp) for p in polygon]
    DrawMyPolygon(screen, pol2, (0, 0, 120), 0)
    
    
    
    shift = intersectLines(polygon[1], polygon[2], polygon[4], polygon[5]) - polygon[1]
    zones = getZonesFrom8GonBig(polygon)
    zones = [[p + shift for p in zone] for zone in zones]

    colors = [(255, 69, 0), (255, 215, 0), (0, 255, 0), (0, 255, 255)]
    DrawMyPolygon(screen, zones[0], colors[0], 0)
    DrawMyPolygon(screen, zones[1], colors[1], 0)
    DrawMyPolygon(screen, zones[2], colors[2], 0)
    DrawMyPolygon(screen, zones[3], colors[3], 0)
    
    pygame.image.save(screen, 'picInducedTBigShift-A.bmp')
    pygame.display.flip()
    
    for j in range(0, 4):
        for i in range(0, 4 - j):
            zones[j] = MakeZoneOuterBilliard(zones[j], polygon, True, False)
            DrawMyPolygon(screen, zones[j], colors[j], 0)
            DrawMyPolygon(screen, zones[j], raysColor, 2)

    pygame.image.save(screen, 'picInducedTBigShift-B.bmp')
    pygame.display.flip()
     

#WORKING ON THIS FUNCTION: need to paint periodic components
# with periods
def PaintPeriodicComponentsFor8(screen):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(200), Fraction(-40))
    c1 = MyPoint(Fraction(200), Fraction(40))
    polygon = Get8gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)

    c = lineIntersection(polygon[1], polygon[2], polygon[4], polygon[3])
    pol2 = [reflect(p, c) for p in polygon]
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    DrawMyPolygon(screen, polygon, raysColor, 1)
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)
    #DrawMyPolygon(screen, pol2, (0, 0, 120), 0)

    zones = getZonesFrom8Gon(polygon)
    basePeriodicPolygons = []
    basePeriodicPolygons.append(pol2.copy())
    for i in range(3):
        pf = zones[i]
        while True:
            pf2 = MakeZoneOuterBilliard(pf, polygon, True)
            if i == 2:
                pf2 = MakeZoneOuterBilliard(pf2, polygon, True)
            pf2 = intersectConvexPolygons(zones[i], pf2)
            if (arePolygonsEqual(pf, pf2)):
                break
            pf = pf2
        basePeriodicPolygons.append(pf)

    for i in range(len(basePeriodicPolygons)):
        DrawMyPolygon(screen, basePeriodicPolygons[i], ((i*100 + 57)%256, (i*200 + 179)%256, (i * 40 + 2007)%256), 0)

    cb = GetCenter(pol2)
    cs = GetCenter(basePeriodicPolygons[1])
    O = polygon[1]
    coef = (cs.GetX() - O.GetX()) / (cb.GetX() - O.GetX())
    print("COEF", coef)

    levels = 3
    levelsOut = 4
    
    for i in range(1, 3*(levels - 1) + 1):
        basePeriodicPolygons.append(compressPolygon(basePeriodicPolygons[i], coef, O))
    
    shift = intersectLines(polygon[1], polygon[2], polygon[4], polygon[5])
    shift = shift - O

    length = len(basePeriodicPolygons)
    for i in range(length * (levelsOut - 1)):
        basePeriodicPolygons.append([p + shift for p in basePeriodicPolygons[i]])

    for i in range(len(basePeriodicPolygons)):
        print(i)
        c = GetCenter(basePeriodicPolygons[i])
        c2 = c
        angleRotate = 0
        periodInduced = 0
        while (True):
            c2 = MakeZoneOuterBilliardPair(c2, polygon)
            periodInduced += 1
            angleRotate += c2[1]
            c2 = c2[0]
            if c2 == c:
                break
        period = periodInduced * 8 // findGcd(angleRotate, 8)
        print(i, periodInduced, angleRotate, period)
        
        zone = basePeriodicPolygons[i]
        for j in range(periodInduced):
            color = ((462+10*period)%256, (98+20*period)%256, (78+70*period)%256)
            color = ((462+10*i)%256, (98+20*i)%256, (78+70*i)%256)
            DrawMyPolygon(screen, zone, color, 0)
            c2 = MakeZoneOuterBilliardPoint(c, polygon)
            zone = [(p + c2 - c) for p in zone]
            c = c2

    #pygame.image.save(screen, 'picPeriodicComponents.bmp')
    #pygame.image.save(screen, 'picPeriodicComponentsBig.bmp')
    pygame.image.save(screen, 'picPeriodicComponentsBigShift.bmp')
    pygame.display.flip()

def paintInducedTSmallFor8(screen, isBefore):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(200), Fraction(-40))
    c1 = MyPoint(Fraction(200), Fraction(240))
    polygon = Get8gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)
    
    zones = getZonesFrom8Gon(polygon)
    stableZones = getStableZonesFrom8Gon(polygon, zones)
    O1 = GetCenter(stableZones[0])
    O2 = GetCenter(stableZones[1])
    beta = getBeta(polygon)
    O3 = GetCenter(beta)

    O23 = rotate135ClockwiseAround(O1, O2)
    O32 = rotate135CounterclockwiseAround(O1, O2)

    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
    DrawMyPolygon(screen, beta, raysColor, 2, (0, 0, 120))
    
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)

    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)

    if not isBefore:
        zones = [MakeZoneOuterBilliard(z, polygon, True, False) for z in zones]
    DrawMyPolygon(screen, zones[0], raysColor, 2, (255, 0, 0))
    DrawMyPolygon(screen, zones[1], raysColor, 2, (0xff, 0xff, 0))
    DrawMyPolygon(screen, zones[2], raysColor, 2, (0, 255, 0))

    DrawPoint(screen, O1, (255, 255, 255), 2)
    DrawPoint(screen, O2, (0, 0, 0), 2)
    DrawPoint(screen, O23, (0, 0, 0), 2)
    DrawPoint(screen, O32, (0, 0, 0), 2)
    DrawPoint(screen, O3, (255, 255, 255), 2)
    
    pygame.image.save(screen, "pic8-TDash-Small" + str(1 if isBefore else 2) + ".bmp")
    
#def paintInducedTSmallFor8(screen, isBefore):
#    screen.fill((0, 0, 0))
#    c0 = MyPoint(Fraction(200), Fraction(-240))
#    c1 = MyPoint(Fraction(200), Fraction(240))
#    polygon = Get8gonFromSegment(c0, c1)
#    raysColor = (47, 79, 79)
#    
#    zones = getZonesFrom8Gon(polygon)
#    beta = getBeta(polygon)
#
#    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
#    DrawMyPolygon(screen, beta, raysColor, 2, (0, 0, 120))
#    
#    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
#    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)
#
#    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)
#
#    if not isBefore:
#        zones = [MakeZoneOuterBilliard(z, polygon, True, False) for z in zones]
#    DrawMyPolygon(screen, zones[0], raysColor, 2, (255, 0, 0))
#    DrawMyPolygon(screen, zones[1], raysColor, 2, (0xff, 0xff, 0))
#    DrawMyPolygon(screen, zones[2], raysColor, 2, (0, 255, 0))
#
#    pygame.image.save(screen, "pic8-TDash-Small" + str(1 if isBefore else 2) + ".bmp")

def paintBaseBetas(screen):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(200), Fraction(-40))
    c1 = MyPoint(Fraction(200), Fraction(380))
    polygon = Get8gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)
    
    zones = getZonesFrom8Gon(polygon)
    beta = getBeta(polygon)
    
    stableZones = getStableZonesFrom8Gon(polygon, zones)
    beta1, beta2, beta32, beta23 = getZeroRankPolygonsFrom8Gon(polygon, zones, stableZones)

    betaColor = (0xff, 0x8c, 0)
    
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
    DrawMyPolygon(screen, beta, raysColor, 2, (0, 0, 120))
    
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)

    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)

    for b in [beta1, beta2, beta32, beta23]:
        DrawMyPolygon(screen, b, raysColor, 2, betaColor)
        DrawPoint(screen, GetCenter(b), raysColor, 2)

def paintPicZeroRankFigures(screen):
    paintBaseBetas(screen)
    pygame.image.save(screen, "pic8-betas" + ".bmp")

def paintPicSelfSimilarity(screen, isBefore):
    paintBaseBetas(screen)
    c0 = MyPoint(Fraction(200), Fraction(-40))
    c1 = MyPoint(Fraction(200), Fraction(380))
    polygon = Get8gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)
    
    zones = getZonesFrom8Gon(polygon)
    beta = getBeta(polygon)

    stableZones = getStableZonesFrom8Gon(polygon, zones)
    beta1, beta2, beta32, beta23 = getZeroRankPolygonsFrom8Gon(polygon, zones, stableZones)


    betaColor = (0xff, 0x8c, 0)
    

    def Gamma(p):
        return compressVector(polygon[1], p, (GetCenter(beta1).GetX() - polygon[1].GetX()) / (GetCenter(beta).GetX() - polygon[1].GetX()))

    smallZones = [[Gamma(p) for p in z] for z in zones]
    
    def genColor(i):
        if i == 0:
            return (0xff, 0, 0)
        if i == 1:
            return (0xff, 0xff, 0)
        if i == 2:
            return (0, 0xff, 0)

    pols = smallZones
    GX = [Gamma(p) for p in [polygon[1], beta[0], beta[7], beta[6]]]

    for i in range(len(pols)):
        zone = pols[i].copy()
        while True:
            if isBefore:
                DrawMyPolygon(screen, zone, raysColor, 2, genColor(i))
            zone = MakeZoneOuterBilliard(zone, polygon, needCompress=True)
            if isPolygonInPolygon(zone, GX):
                break
        if not isBefore:
            DrawMyPolygon(screen, zone, raysColor, 2, genColor(i))

    pygame.image.save(screen, "pic8-selfSimilarity-" + str(1 if isBefore else 2) + ".bmp")
    
def paintPic8SpiralSequence(screen):
    c0 = MyPoint(Fraction(200), Fraction(-40))
    c1 = MyPoint(Fraction(200), Fraction(240))
    polygon = Get8gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)
    
    zones = getZonesFrom8Gon(polygon)
    beta = getBeta(polygon)

    stableZones = getStableZonesFrom8Gon(polygon, zones)
    beta1, beta2, beta32, beta23 = getZeroRankPolygonsFrom8Gon(polygon, zones, stableZones)

    def Gamma(p):
        return compressVector(polygon[1], p, (GetCenter(beta1).GetX() - polygon[1].GetX()) / (GetCenter(beta).GetX() - polygon[1].GetX()))
    
    O1 = GetCenter(beta1)
    O2 = GetCenter(beta2)

    X = getFirstComponent(polygon)
    X = [Gamma(Gamma(p)) for p in X]

    X = MakeZoneOuterBilliard(X, polygon, True)
    X = MakeZoneOuterBilliard(X, polygon, True)

    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
    DrawMyPolygon(screen, beta, raysColor, 2, (0, 0, 120))
    
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)

    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)
   
    DrawMyPolygon(screen, beta2, raysColor, 2, (255, 0, 0))
    DrawMyPolygon(screen, beta23, raysColor, 2, (255, 0, 0))

    C2 = [Gamma(p) for p in beta1]
    C2 = MakeZoneOuterBilliard(C2, polygon, True)
    C2 = MakeZoneOuterBilliard(C2, polygon, True)

    DrawMyPolygon(screen, C2, raysColor, 2, (255, 0, 0))
    DrawMyPolygon(screen, X, raysColor, 2, (0xff, 0xff, 0))

    pygame.image.save(screen, "pic8-XAndSpiralSequence" + ".bmp")

def paintPic8Splittings(screen, iterations):
    c0 = MyPoint(Fraction(200), Fraction(-40))
    c1 = MyPoint(Fraction(200), Fraction(240))
    polygon = Get8gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)
    
    zones = getZonesFrom8Gon(polygon)
    beta = getBeta(polygon)

    stableZones = getStableZonesFrom8Gon(polygon, zones)
    beta1, beta2, beta32, beta23 = getZeroRankPolygonsFrom8Gon(polygon, zones, stableZones)

    def Gamma(p):
        return compressVector(polygon[1], p, (GetCenter(beta1).GetX() - polygon[1].GetX()) / (GetCenter(beta).GetX() - polygon[1].GetX()))

    redColor = (255, 0, 0)
    greenColor = (0, 255, 0)

    splitting = [(z.copy(), redColor) for z in zones]

    fc = getFirstComponent(polygon)
    gfc = [Gamma(p) for p in fc]

    for _ in range(iterations):
        newSplitting = [(beta1, greenColor), (beta2, greenColor), (beta32, greenColor), (beta23, greenColor)]
        for zone, color in splitting:
            z = [Gamma(p) for p in zone]
            cz = z.copy()
            while True:
                newSplitting.append( (cz.copy(), color) )
                cz = MakeZoneOuterBilliard(cz, polygon, True)
                if isPolygonInPolygon(cz, gfc):
                    break
        splitting = newSplitting
    
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
    DrawMyPolygon(screen, beta, raysColor, 2, (0, 0, 120))
    
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)

    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)

    for zone, color in splitting:
        DrawMyPolygon(screen, zone, raysColor, 2, color)
    
    pygame.image.save(screen, "pic8-Splitting-" + str(iterations) + ".bmp")

if __name__ == '__main__':
    pygame.init()
    size_x = 512 * 6
    size_y = 512 * 6
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    
    #paintPicBaseAngleRaw(screen)
    #paintPicEnterZRaw(screen)
    #paintPicInducedT(screen)
    #PaintFirstReturnMapFor8(screen)
    #paintPicInducedTBigShift(screen)

    #paintInducedTSmallFor8(screen, True)
    #paintInducedTSmallFor8(screen, False)
    #paintPicZeroRankFigures(screen)
    #paintPicSelfSimilarity(screen, True)
    #paintPicSelfSimilarity(screen, False)

    #paintPic8SpiralSequence(screen)
    paintPic8Splittings(screen, 0)
    paintPic8Splittings(screen, 1)
    paintPic8Splittings(screen, 2)
    paintPic8Splittings(screen, 3)
    
    waitEnd()
    

