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

def drawPic12_1(screen):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(900), Fraction(1020))
    c1 = MyPoint(Fraction(900), Fraction(1120))
    polygon = Get12gonFromSegment(c0, c1)
    
    raysColor = (47, 79, 79)
    
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))

    center = (polygon[0] + polygon[6]) / MyCipher(2)
    for i in range(-2, 11, 1):
        c = lineIntersection(polygon[i], polygon[i+1], polygon[i-3], polygon[i-4])
        newP = [reflect(p, c) for p in polygon]
        DrawMyPolygon(screen, newP, (0, 0, 120), 0)
        DrawMyPolygon(screen, newP, raysColor, 2)

    c3 = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
    polygon3 = [reflect(p, c3) for p in polygon]

    zz = [polygon[1], polygon3[6], polygon3[5], polygon3[4], polygon3[3], polygon3[2]]
    z = []
    for i in range(12):
        z.extend(zz)
        zz = [rotate30ClockwiseAround(p, center) for p in zz]

    DrawMyPolygon(screen, z, raysColor, 2, (0xff, 0xa5, 0x00))
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))

    for i in range(12):
        DrawLineMyPoint(screen, polygon[i-1], polygon[i], raysColor, 2)

    pygame.display.flip()
    pygame.image.save(screen, 'pic12-1.bmp')
        
    waitEnd()

def drawPic12_2_par(screen, isAfter):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(80), Fraction(50))
    c1 = MyPoint(Fraction(80), Fraction(250))
    polygon = Get12gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)
    
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    DrawMyPolygon(screen, polygon, raysColor, 2)
        
    zones = getZonesFrom12Gon(polygon)
    c3 = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
    polygon3 = [reflect(p, c3) for p in polygon]

    zones[4] = [polygon3[6] + (polygon3[7] - polygon3[6]) * MyCipher(100), polygon3[6], c3, polygon3[1], polygon3[1] + (polygon3[0] - polygon3[1]) * MyCipher(100)]
    lst = [zones[4][4], polygon3[1], polygon3[1] + (polygon[2] - polygon[1]) * MyCipher(100) ]
    zones.append(lst)

    stableZones = getStableZonesFrom12Gon(polygon, zones)
    print(len(zones))
    for i in range(len(zones)):
        if (isAfter):
            zones[i] = MakeZoneOuterBilliard(zones[i], polygon, needCompress = True, isInverse = False) 
        DrawMyPolygon(screen, zones[i], ((148 + 350*i) % 256, (462 + 120*i)%256, (78 + 60*i)%256), 0)
        DrawMyPolygon(screen, zones[i], raysColor, 2)

    for i in range(2, 8):
        DrawRayMyPoint(screen, polygon[i], polygon[i-1], raysColor, 2)
    
    DrawMyPolygon(screen, polygon3, (0, 0, 120), 0)
    
    for i in range(0, 3):
        c = GetCenter(stableZones[i])
        DrawPoint(screen, c, raysColor, 2)
    DrawPoint(screen, GetCenter(stableZones[3]), (255, 255, 255), 2)
    DrawPoint(screen, GetCenter(polygon3), (255, 255, 255), 2)

    pygame.display.flip()
    pygame.image.save(screen, "pic12-2-" + str(2 if isAfter else 1) + ".bmp")
        
    #waitEnd()
    
def drawPic12_2(screen):
    drawPic12_2_par(screen, False)
    drawPic12_2_par(screen, True)

def drawPic12_4(screen):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(80), Fraction(-150))
    c1 = MyPoint(Fraction(80), Fraction(250))
    polygon = Get12gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)
    
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    DrawMyPolygon(screen, polygon, raysColor, 2)
    
    c3 = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
    zones = getZonesFrom12Gon(polygon)
    stableZones = getStableZonesFrom12Gon(polygon, zones)
    
    o5 = reflect(GetCenter(polygon), c3)
    o4 = GetCenter(stableZones[3])
    o1 = GetCenter(stableZones[0])

    coefMid = (o4.GetX() - polygon[1].GetX()) / (o5.GetX() - polygon[1].GetX())
    coefSm = (o1.GetX() - polygon[1].GetX()) / (o5.GetX() - polygon[1].GetX()) 

    num = 3
    color4 = ((234 + 57 * num) % 256, (56 + 20 * num * num ) % 256, (78 + 134 * num * num * num) % 256)

    DrawMyPolygon(screen, stableZones[3], raysColor, 2, color4)
    
    comp = getFirstComponent(polygon)
    comp = [polygon[1] + (p - polygon[1]) * coefMid for p in comp]

    DrawMyPolygon(screen, comp, raysColor, 2, (0, 128, 0))

    DrawMyPolygon(screen, stableZones[2], raysColor, 2, (255, 0, 0))
    DrawMyPolygon(screen, stableZones[1], raysColor, 2, (255, 0, 0))

    compSm = [polygon[1] + (p - polygon[1]) * coefSm for p in stableZones[3]]
    for i in range(2):
        compSm = MakeZoneOuterBilliard(compSm, polygon, True, True)

    DrawMyPolygon(screen, compSm, raysColor, 2, (255, 0, 0))
    
    pos = findMaxyMinxIndexInPolygon(compSm)
    posv = findMinyMinxIndexInPolygon(stableZones[2])

    zoneX = [stableZones[2][posv], compSm[pos], compSm[pos-11], compSm[pos-10], compSm[pos-9], compSm[pos-8]]

    DrawMyPolygon(screen, zoneX, raysColor, 2, (255, 255, 0))

    pygame.display.flip()
    pygame.image.save(screen, "pic12-4.bmp")

def paintPic12TDashAlphas(screen, isBefore):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(80), Fraction(-50))
    c1 = MyPoint(Fraction(80), Fraction(150))
    polygon = Get12gonFromSegment(c0, c1)
    beta = getBeta(polygon)
    
    raysColor = (47, 79, 79)
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
    #DrawMyPolygon(screen, beta, raysColor, 2, (0, 0, 120))
    
    zonesBig = getZonesFrom12GonBig(polygon)
    if not isBefore:
        zonesBig = [MakeZoneOuterBilliard(zone, polygon, True) for zone in zonesBig]
    
    def genColor(i):
        return ((462 + 350*i) % 256, (20 + 120*i)%256, (70 + 60*i)%256) 
    
    for i in range(3, 8):
        DrawRayMyPoint(screen, polygon[i], polygon[i-1], raysColor, 2)
    for i in range(len(zonesBig)):
        DrawMyPolygon(screen, zonesBig[i], raysColor, 2, genColor(i))
    

    pygame.display.flip()
    pygame.image.save(screen, "pic12-TDashAlphas-" + str(1 if isBefore else 2) + ".bmp")

def paintPic12BadOrGoodSelfSimilarityFRM(screen, isGood, isBefore):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(80), Fraction(-1450))
    c1 = MyPoint(Fraction(80), Fraction(1050))
    polygon = Get12gonFromSegment(c0, c1)
    beta = getBeta(polygon)
    
    raysColor = (47, 79, 79)
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
    DrawMyPolygon(screen, beta, raysColor, 2, (0, 0, 120))
    
    fc = getFirstComponent(polygon)
    zones = getZonesFrom12Gon(polygon)
    stableZones = getStableZonesFrom12Gon(polygon, zones)
    
    for i in range(4):
        DrawMyPolygon(screen, stableZones[i], raysColor, 2, (0xff, 0xff, 0))

    O5 = GetCenter(beta)
    O4 = GetCenter(stableZones[3])
    O1 = GetCenter(stableZones[0])

    O = O4 if isGood else O1
    coef = (O.GetX() - polygon[1].GetX()) / (O5.GetX() - polygon[1].GetX())

    goodPolygon = [compressVector(polygon[1], p, coef) for p in fc]

    zonesAfter = tryMakeFirstReturnMapOnlyPolygons([goodPolygon], goodPolygon, polygon, zones, maxKol = 10000)
    zonesBefore = reverseAndTestZones(zonesAfter, goodPolygon, polygon, zones)
    
    for i in range(len(zonesBefore)):
        zone = zonesBefore[i][0].copy()
        while True:
            if isBefore:
                DrawMyPolygon(screen, zone, raysColor, 2, ((462 + 350*i) % 256, (20 + 120*i)%256, (70 + 60*i)%256) )
            zone = MakeZoneOuterBilliard(zone, polygon, needCompress=True)
            if (isPolygonInPolygon(zone, goodPolygon)):
                break
        if not isBefore:
            DrawMyPolygon(screen, zone, raysColor, 2, ((462 + 350*i) % 256, (20 + 120*i)%256, (70 + 60*i)%256) )
        
    pygame.image.save(screen, "pic12-FirstReturnMap-" + ("Good" if isGood else "Bad") + "-" + str(1 if isBefore else 2) + ".bmp")

def paintPicXAndSpiralSequence(screen):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(80), Fraction(-150))
    c1 = MyPoint(Fraction(80), Fraction(550))
    polygon = Get12gonFromSegment(c0, c1)
    beta = getBeta(polygon)
    
    raysColor = (47, 79, 79)
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
    DrawMyPolygon(screen, beta, raysColor, 2, (0, 0, 120))
    
    fc = getFirstComponent(polygon)
    zones = getZonesFrom12Gon(polygon)
    stableZones = getStableZonesFrom12Gon(polygon, zones)
    
    O5 = GetCenter(beta)
    O4 = GetCenter(stableZones[3])
    O1 = GetCenter(stableZones[0])

    coefMiddle = (O4.GetX() - polygon[1].GetX()) / (O5.GetX() - polygon[1].GetX())
    coefSmall = (O1.GetX() - polygon[1].GetX()) / (O5.GetX() - polygon[1].GetX())

    rocketMiddle = [compressVector(polygon[1], p, coefMiddle) for p in fc]
    rocketSmallMiddle = [compressVector(polygon[1], p, coefSmall) for p in rocketMiddle]
    C2 = [compressVector(polygon[1], p, coefSmall) for p in stableZones[3]]
    X = rocketSmallMiddle
   
    DrawMyPolygon(screen, rocketMiddle, raysColor, 2, (0, 120, 0))
    for i in range(4):
        DrawMyPolygon(screen, stableZones[i], raysColor, 2, (0, 255, 127))

    for i in range(3, 8):
        DrawRayMyPoint(screen, polygon[i], polygon[i-1], raysColor, 2)
   
    for _ in range(2):
        DrawMyPolygon(screen, X, raysColor, 2, (255, 255, 0))
        DrawMyPolygon(screen, C2, raysColor, 2, (255, 0, 0))
        X = MakeZoneOuterBilliard(X, polygon, needCompress = True, isInverse = True)
        C2 = MakeZoneOuterBilliard(C2, polygon, needCompress = True, isInverse = True)

    C0 = stableZones[2]
    C1 = stableZones[1]

    DrawMyPolygon(screen, X, raysColor, 2, (255, 255, 0))
    for C in [C0, C1, C2]:
        DrawMyPolygon(screen, C, raysColor, 2, (255, 0, 0))

    pygame.image.save(screen, "pic12-XAndSpiralSequence" + ".bmp")

def paintPeriodicComponents(screen, isSmallMiddle):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(80), Fraction(-150))
    c1 = MyPoint(Fraction(80), Fraction(550))
    polygon = Get12gonFromSegment(c0, c1)
    beta = getBeta(polygon)
    
    raysColor = (47, 79, 79)
    
    fc = getFirstComponent(polygon)
    zones = getZonesFrom12Gon(polygon)
    stableZones = getStableZonesFrom12Gon(polygon, zones)  
   
    O5 = GetCenter(beta)
    O4 = GetCenter(stableZones[3])
    O1 = GetCenter(stableZones[0])

    coefMiddle = (O4.GetX() - polygon[1].GetX()) / (O5.GetX() - polygon[1].GetX())
    coefSmall = (O1.GetX() - polygon[1].GetX()) / (O5.GetX() - polygon[1].GetX())

    rocketMiddle = [compressVector(polygon[1], p, coefMiddle) for p in fc]
    rocketSmallMiddle = [compressVector(polygon[1], p, coefSmall) for p in rocketMiddle]
    
    forbPol = rocketSmallMiddle if isSmallMiddle else rocketMiddle

    pcs, bad = findPeriodicComponents(fc, [forbPol], polygon, zones, iterations = 100, screen = None)

    print("LEN(bad):", len(bad))
    print("GO")
    #for pc in pcs:
    #    print("PERIOD: ", pc[1])

    prefix = "pic12-periodicComponents-" + ("smallMiddle" if isSmallMiddle else "middle") + "-"

    polygonArea = getDoubledOrientedArea(polygon)
    
    index = 0
    for pol, per in pcs:
        index += 1
        polArea = getDoubledOrientedArea(pol)
        
        perMiddle = 0
        for _ in range(per):
            if isPolygonInPolygon(pol, rocketMiddle):
                perMiddle += 1
            pol = MakeZoneOuterBilliard(pol, polygon, True, False)

        minx = pol[0].GetX()
        maxx = pol[0].GetX()
        for p in pol:
            x = p.GetX()
            minx = x if x < minx else minx
            maxx = x if x > maxx else maxx
        coef = MyCipher(512 * 3) / (maxx - minx)
        pol = [compressVector(MyPoint(Fraction(0), Fraction(0)), p, coef) for p in pol]
        minx *= coef
        maxx *= coef

        miny = pol[0].GetY()
        maxy = pol[0].GetY()
        for p in pol:
            y = p.GetY()
            miny = y if y < miny else miny
            maxy = y if y > maxy else maxy

        shift = MyPoint(MyCipher(512) - minx, MyCipher(512) - miny)
        pol = [p + shift for p in pol]
        
        screen.fill((0, 0, 0))
        DrawMyPolygon(screen, pol, raysColor, 2, (0, 255, 0))
        pygame.image.save(screen, prefix + str(index) + ".bmp")
        
        print("PERIODS: ", per, perMiddle)
        relativeArea = polArea / polygonArea
        print("RELATIVE AREA: ", relativeArea, float(relativeArea))

def paintPic12Splittings(screen, iterationsMax):
    c0 = MyPoint(Fraction(80), Fraction(-150))
    c1 = MyPoint(Fraction(80), Fraction(550))
    polygon = Get12gonFromSegment(c0, c1)
    beta = getBeta(polygon)
    
    raysColor = (47, 79, 79)
    
    fc = getFirstComponent(polygon)
    zones = getZonesFrom12Gon(polygon)
    stableZones = getStableZonesFrom12Gon(polygon, zones)  
   
    O5 = GetCenter(beta)
    O4 = GetCenter(stableZones[3])
    O1 = GetCenter(stableZones[0])

    coefMiddle = (O4.GetX() - polygon[1].GetX()) / (O5.GetX() - polygon[1].GetX())
    coefSmall = (O1.GetX() - polygon[1].GetX()) / (O5.GetX() - polygon[1].GetX())

    rocketMiddle = [compressVector(polygon[1], p, coefMiddle) for p in fc]
    rocketSmallMiddle = [compressVector(polygon[1], p, coefSmall) for p in rocketMiddle]
    
    forbPol = rocketSmallMiddle

    pcs, bad = findPeriodicComponents(fc, [forbPol], polygon, zones, iterations = 100, screen = None)


    def Gamma(p):
        return compressVector(polygon[1], p, coefSmall)

    redColor = (255, 0, 0)
    greenColor = (0, 255, 0)

    greens = []
    for pol, per in pcs:
        for _ in range(per):
            if isPolygonInPolygon(pol, rocketMiddle):
                greens.append((pol.copy(), greenColor))          
            pol = MakeZoneOuterBilliard(pol, polygon, True)

    zonesAfter = tryMakeFirstReturnMapOnlyPolygons([rocketMiddle], rocketMiddle, polygon, zones, maxKol = 100)
    zonesBefore = reverseAndTestZones(zonesAfter, rocketMiddle, polygon, zones)
    splitting = [(z[0].copy(), redColor) for z in zonesBefore]

    for iterations in range(iterationsMax):
        screen.fill((0, 0, 0))
        DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
        DrawMyPolygon(screen, beta, raysColor, 2, (0, 0, 120))
        DrawMyPolygon(screen, stableZones[3], raysColor, 2, (0, 0, 120))
    
        DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
        DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)

        DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 2)
        DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)
        DrawRayMyPoint(screen, polygon[5], polygon[4], raysColor, 2)
        DrawRayMyPoint(screen, polygon[6], polygon[5], raysColor, 2)
        DrawRayMyPoint(screen, polygon[7], polygon[6], raysColor, 2)

        for zone, color in splitting:
            DrawMyPolygon(screen, zone, raysColor, 2, color)
    
        pygame.image.save(screen, "pic12-Splitting-" + str(iterations) + ".bmp")

        if (iterations + 1 == iterationsMax):
            break

        newSplitting = greens.copy()

        iterFRM = 0
        numZone = 0
        for zone, color in splitting:
            numZone += 1
            z = [Gamma(p) for p in zone]
            cz = z.copy()
            while True:
                newSplitting.append( (cz.copy(), color) )
                cz = MakeZoneOuterBilliard(cz, polygon, True)
                if isPolygonInPolygon(cz, rocketSmallMiddle):
                    break
                iterFRM += 1
                if iterFRM % 10 == 0:
                    print(iterations, numZone, iterFRM)
        splitting = newSplitting
   
def paintBaseBetas(screen):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(200), Fraction(-40))
    c1 = MyPoint(Fraction(200), Fraction(180))
    polygon = Get12gonFromSegment(c0, c1)
    raysColor = (47, 79, 79)
    
    zones = getZonesFrom12Gon(polygon)
    beta = getBeta(polygon)
    
    stableZones = getStableZonesFrom12Gon(polygon, zones)

    betaColor = (0xff, 0xff, 0)
    
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 120))
    DrawMyPolygon(screen, beta, raysColor, 2, betaColor)
    DrawPoint(screen, GetCenter(beta), raysColor, 2)
    
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)

    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)
    DrawRayMyPoint(screen, polygon[5], polygon[4], raysColor, 2)
    DrawRayMyPoint(screen, polygon[6], polygon[5], raysColor, 2)
    DrawRayMyPoint(screen, polygon[7], polygon[6], raysColor, 2)

    for b in stableZones:
        DrawMyPolygon(screen, b, raysColor, 2, betaColor)
        DrawPoint(screen, GetCenter(b), raysColor, 2)

    pygame.image.save(screen, "pic12-betas" + ".bmp")

if __name__ == '__main__':
    pygame.init()
    size_x = 512 * 6
    size_y = 512 * 6
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    
    #drawPic12_2(screen)
    #paintPic12TDashAlphas(screen, True)
    #paintPic12TDashAlphas(screen, False)
    #paintPic12BadOrGoodSelfSimilarityFRM(screen, True, True)
    #paintPic12BadOrGoodSelfSimilarityFRM(screen, True, False)
    #paintPic12BadOrGoodSelfSimilarityFRM(screen, False, True)
    #paintPic12BadOrGoodSelfSimilarityFRM(screen, False, False)
    
    #paintPicXAndSpiralSequence(screen)
    #paintPeriodicComponents(screen, False)
    #paintPeriodicComponents(screen, True)

    #paintPic12Splittings(screen, 4) # works in a very-very long time....
    #paintPic12Splittings(screen, 2) # works in a very-very long time....
    
    paintBaseBetas(screen)
    
    waitEnd()
