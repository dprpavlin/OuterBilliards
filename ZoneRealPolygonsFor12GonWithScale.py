from workWith12Gon import *
from point2D import *
from segmentIntersection import *
from billiard import *
from absqrtn import *
from fractions import *

import pygame, sys
from pygame.locals import *

#size_x = 512 * 5 // 2
#size_y = 512 * 4
size_y = 512 * 5 // 2
size_x = 512 * 4
pictureNameAfter = 'InnerRocketSmallAfter.bmp'
pictureNameBefore = 'InnerRocketSmallBefore.bmp'

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

#find (a, b) - linear function f(x) = a*x + b so that f(x01) = x02, f(x11) = x12
def getLinearFunction(x01, x02, x11, x12):
    return (x02 - x12) / (x01 - x11) , (x01*x12 - x11*x02) / (x01 - x11)

def getBoundsFromPolygon(polygon):
    xs = [p.GetX() for p in polygon]
    ys = [p.GetY() for p in polygon]
    return (min(xs), max(xs), min(ys), max(ys))

def makeScalingMyPoint(point, ax, bx, ay, by):
    return MyPoint(point.GetX() * ax + bx, point.GetY() * ay + by)

def makeScalingMyPolygon(polygon, ax, bx, ay, by):
    return [makeScalingMyPoint(point, ax, bx, ay, by) for point in polygon]

def makeScalingMyPolygons(polygons, ax, bx, ay, by):
    return [makeScalingMyPolygon(polygon, ax, bx, ay, by) for polygon in polygons]


def drawSuperPolygonSituation(polygon, zones, stableZones, superPolygon, splitting, pictureName):
    if type(splitting[0]) == tuple:
        splitting = [s[0] for s in splitting]
    for p in superPolygon:
        sys.stderr.write('POLYGON: ' + str((float(p.GetX()))) + ' ' + str(float(p.GetY())) + '\n')
    
    minx, maxx, miny, maxy = getBoundsFromPolygon(superPolygon)
    sys.stderr.write(str(minx) + ' ' + str(maxx) + ' ' + str(miny) + ' ' + str(maxy))
    newMinY = MyCipher(12)
    newMaxY = MyCipher(size_y - 12) 
    newMinX = MyCipher(12)
    newMaxX = MyCipher(size_x - 12) 
    ay, by = getLinearFunction(miny, newMinY, maxy, newMaxY)
    #ax, bx = ay, by
    ax, bx = getLinearFunction(minx, newMinX, maxx, newMaxX)
    polygon = makeScalingMyPolygon(polygon, ax, bx, ay, by)
    zones = makeScalingMyPolygons(zones, ax, bx, ay, by)
    stableZones = makeScalingMyPolygons(stableZones, ax, bx, ay, by)
    superPolygon = makeScalingMyPolygon(superPolygon, ax, bx, ay, by)
    splitting = makeScalingMyPolygons(splitting, ax, bx, ay, by)
  
    for p in superPolygon:
        sys.stderr.write('POLYGON: ' + str((float(p.GetX()))) + ' ' + str(float(p.GetY())) + '\n')
    #sys.exit(0)
    screen = pygame.display.get_surface()
    screen.fill((0, 0, 0))
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    DrawMyPolygon(screen, superPolygon, (255, 255, 0), 0)
    raysColor = (57, 179, 218)
    #print('polygon: ', polygon)
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 1)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 1)
    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 1)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 1)
    DrawRayMyPoint(screen, polygon[5], polygon[4], raysColor, 1)
    DrawRayMyPoint(screen, polygon[6], polygon[5], raysColor, 1)

    for i in range(0, 4):
        DrawMyPolygon(screen, stableZones[i], ((148 + 350*i) % 256, (462 + 240*i)%256, (78 + 60*i)%256), 0)
    pygame.display.flip()

#    DrawMyPolygon(screen, superPolygon, (0, 255, 0), 0)
    pygame.display.flip()

    print('LEN SPLITTING: ', len(splitting))
    sys.stderr.write('LEN SPLITTING: ' + str(len(splitting)))
    for i in range(len(splitting)):
        sys.stderr.write(str(i) + ' polygons painted from ' + str(len(splitting)) + '\n') 
        DrawMyPolygon(screen, splitting[i], ((462+10*i)%256, (98+20*i)%256, (78+70*i)%256), 1, ((148+350*i)%256, (20+120*i)%256, (70+140*i)%256))


    pygame.display.flip()
    pygame.image.save(screen, pictureName)

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    c0 = MyPoint(Fraction(20), Fraction(-60))
    c1 = MyPoint(Fraction(20), Fraction(20))
   
    polygon = Get12gonFromSegment(c0, c1)
   # DrawMyPolygon(screen, polygon, (0, 0, 120), 0)

    #DrawRayMyPoint(screen, MyPoint(Fraction(256), Fraction(256)), MyPoint(Fraction(1512), Fraction(512)), (0, 0, 120), 0)

    '''
    raysColor = (57, 179, 218)
    #print('polygon: ', polygon)
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 1)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 1)
    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 1)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 1)
    DrawRayMyPoint(screen, polygon[5], polygon[4], raysColor, 1)
    DrawRayMyPoint(screen, polygon[6], polygon[5], raysColor, 1)
    '''

    firstComponent = getFirstComponent(polygon)
    #DrawMyPolygon(screen, firstComponent, (21, 43, 49), 0)
    zones = getZonesFrom12Gon(polygon)
    for i in range(1, 4):
        print((zones[i][3] - zones[i][1]).len2() / (zones[i][2] - zones[i][0]).len2())
    #print('Zones...: zones = ', zones)
    stableZones = getStableZonesFrom12Gon(polygon, zones)
   
    '''superPolygon = firstComponent.copy()
    polygons = splitGoodPolygonByZones(superPolygon, polygon, zones)
    for i in range(len(polygons)):
        DrawMyPolygon(screen, polygons[i], ((148 + 350*i) % 256, (462 + 240*i)%256, (78 + 60*i)%256), 0)
    
    pygame.display.flip()
    waitEnd()
    '''

    '''
    for i in range(0, 4):
        DrawMyPolygon(screen, stableZones[i], ((148 + 350*i) % 256, (462 + 240*i)%256, (78 + 60*i)%256), 0)
    pygame.display.flip()
    '''
   
    center = (polygon[0] + polygon[6]) * MyCipher(Fraction(1, 2))
    #DrawPoint(screen, center, (234, 56, 78), 2)
    ukp = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
    newc = reflect(center, ukp)
    #DrawPoint(screen, ukp, (140, 20, 70), 3)
    newnewc = GetCenter(stableZones[0])
    newmidc = GetCenter(stableZones[3])
   
    coef = (newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    print('COEF: ', coef)
    coefMid = (newmidc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    
    #sys.exit(0)
    #pygame.display.flip()

     
    #superPolygon = zones[0].copy() #zone0
    #superPolygon = getFirstComponent(polygon).copy() #rocket(3 strings)
    
    # Plane zone 1
    num = 0
    for i in range(len(stableZones[1])):
        if stableZones[1][i].GetY() < stableZones[1][num].GetY():
            num = i
    if num > 0:
        num -= len(stableZones[1])
    #superPolygon = [polygon[1], stableZones[1][num-1], stableZones[1][num], stableZones[1][num+1]]
    # end of Plane zone 1
    


    #for i in range(len(superPolygon)):
    #    superPolygon[i] = polygon[1] + (superPolygon[i] - polygon[1]) * (newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    #for i in range(len(superPolygon)):
    #    superPolygon[i] = polygon[1] + (superPolygon[i] - polygon[1]) * (newmidc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    
    #for i in range(len(superPolygon)):
    #    superPolygon[i] = polygon[1] + (superPolygon[i] - polygon[1]) * (newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    
    #DrawMyPolygon(screen, superPolygon, (0, 255, 0), 0)
    #pygame.display.flip()

    #'''
    #newSuperPolygon started
    currentComponents = stableZones.copy()
    centerStableZone3 = GetCenter(stableZones[3])
    
    
    for i in range(0, 3):
        currentComponents.append([rotate150ClockwiseAround(point, centerStableZone3) for point in currentComponents[i]])
    
    p1 = centerStableZone3
    p2 = findMaxyMinxIndexInPolygon(currentComponents[3])
    if p2 > 0:
        p2 -= len(currentComponents[3])
    if currentComponents[3][p2].GetY() == currentComponents[3][p2 + 1].GetY():
        p2 -= 1
    else:
        p2 += 1
    p2 = currentComponents[3][p2]

    p3 = GetCenter(currentComponents[6])
    p4 = currentComponents[6][findMinyMinxIndexInPolygon(currentComponents[6])]
     
    p = segmentIntersection(GeneralizedSegment(p1, p2, True, True), GeneralizedSegment(p3, p4, True, True)) 
    currentComponents.append(findComponentOfPointWithPeriod(p, polygon, zones)[0])
    
    p1 = centerStableZone3
    p2 = findMinyMinxIndexInPolygon(currentComponents[3])
    if p2 > 0:
        p2 -= len(currentComponents[3])
    if currentComponents[3][p2].GetY() == currentComponents[3][p2 + 1].GetY():
        p2 -= 1
    else:
        p2 += 1
    p2 = currentComponents[3][p2]

    p3 = GetCenter(currentComponents[2])
    p4 = currentComponents[2][findMaxyMinxIndexInPolygon(currentComponents[2])]
     
    p = segmentIntersection(GeneralizedSegment(p1, p2, True, True), GeneralizedSegment(p3, p4, True, True)) 
    currentComponents.append(findComponentOfPointWithPeriod(p, polygon, zones)[0])
    
    zone0 = stableZones[3]
    zone1 = stableZones[2]
    zone2 = MakeZoneOuterBilliard(currentComponents[8], polygon, True)

    #DrawMyPolygon(screen, zone0, (127, 0, 0), 0) 
    #DrawMyPolygon(screen, zone1, (127, 0, 0), 0) 
    #DrawMyPolygon(screen, zone2, (127, 0, 0), 0)

    
    vertex = findMinyMinxIndexInPolygon(zone0)
    newComponent = [zone0[vertex]]

    pos = findMaxyMinxIndexInPolygon(zone2)
    shift = None
    if zone2[pos-1].GetY() == zone2[pos].GetY():
        pos -= len(zone2)
        shift = 1
    else:
        shift = -1
    for i in range(0, 5):
        newComponent.append(zone2[pos + shift*i])
    DrawMyPolygon(screen, newComponent, (255, 255, 0), 0)
    
    lsBig = linearSystemFromPolygon(firstComponent) 
    lsSmall = linearSystemFromPolygon(newComponent)
    dv = zone1[findMinyMinxIndexInPolygon(zone1)] - lsSmall.c
   
    #dv = MyPoint(-(dv.GetX()), -(dv.GetY()))
    for i in range(len(newComponent)):
        newComponent[i] = newComponent[i] + dv
    lsSmall.c = lsSmall.c + dv


    superPolygon = getFirstComponent(polygon).copy() #rocket(3 strings)
    print('superPolygon: ', superPolygon)
    print('newmidc: ', newmidc)
    print('polygon[1]: ', polygon[1])
    superPolygon = compressPolygon(superPolygon, coefMid, polygon[1])
    superPolygon = [fromSystemToSystem(p, lsBig, lsSmall) for p in superPolygon]
    for p in superPolygon:
        print('superPolygon: ', p)
    #superPolygon = GetFirstComponent
    #newSuperPolygon finished
    #'''

    DrawMyPolygon(screen, stableZones[2], (255, 0, 0), 0)
    DrawMyPolygon(screen, stableZones[1], (255, 0, 0), 0)
    stZone = compressPolygon(stableZones[3], coef, polygon[1])
    for i in range(35):
        stZone = MakeZoneOuterBilliard(stZone, polygon, True) 
    DrawMyPolygon(screen, stZone, (255, 0, 0), 0)
    DrawMyPolygon(screen, superPolygon, (255, 255, 0), 0)
    pygame.image.save(screen, 'testZone.bmp')
    sys.exit(0)

    polygons = [zones[0], zones[1], zones[2]]
    num = 0
    for i in range(1, len(stableZones[3])):
        if stableZones[3][i].GetY() < stableZones[3][num].GetY():
            num = i
    tmp = [stableZones[3][num-1],
           stableZones[3][num-2],
           lineIntersection(polygon[0], polygon[1], polygon[5], polygon[4])
          ]

    polygons.append(tmp)
    tmp = [lineIntersection(polygon[1], polygon[2], polygon[5], polygon[4]),
           stableZones[3][num - len(stableZones[3])], 
           stableZones[3][num + 1 - len(stableZones[3])],
           stableZones[3][num + 2 - len(stableZones[3])]
          ]
    polygons.append(tmp)

    hps = tryMakeFirstReturnMap([superPolygon], superPolygon, polygon, zones, 10000000)
    print('LENGTH: ', len(hps[0]), len(hps[1]))
    print(len(hps[0]), ", ", len(hps[1]))
    print(len(hps[0]), ", ", len(hps[1]), file=sys.stderr)
    print("FirstReturnMap To found\n")
    pols = []
    #std::vector<MyPolygon> pols;
    for i in range(len(hps[0])):
        print('polygon', i)
        print(len(hps[0][i][0]), ":")
        for j in range(len(hps[0][i][0])):
            print('   ', hps[0][i][0][j])
        print('end of polygon', i)
        pols.append(hps[0][i][0])
    print('===================\n')
    
    hps2 = hps
    fc = getFirstComponent(polygon)
    fc = compressPolygon(fc, coefMid, polygon[1])
    hps = tryMakeFirstReturnMap([fc], fc, polygon, zones, 10000000)
    print('LENGTH: ', len(hps[0]), len(hps[1]))
    print(len(hps[0]), ", ", len(hps[1]))
    print(len(hps[0]), ", ", len(hps[1]), file=sys.stderr)
    print("FirstReturnMap To found\n")
    bigPols = []
    #std::vector<MyPolygon> pols;
    for i in range(len(hps[0])):
        print('polygon', i)
        print(len(hps[0][i][0]), ":")
        for j in range(len(hps[0][i][0])):
            print('   ', hps[0][i][0][j])
        print('end of polygon', i)
        bigPols.append(hps[0][i][0])
    print('===================\n')
    
    bigSmallPols = [[fromSystemToSystem(p, lsBig, lsSmall) for p in pp] for pp in bigPols]
    
    assert len(bigSmallPols) == len(pols)
    edges = 0
    for i in range(len(pols)):
        for j in range(len(bigSmallPols)):
            if (areMyPolygonsEqual(pols[i], bigSmallPols[j])):
                sys.stderr.write(str(i) + ' ' + str(j) + '\n')
                edges += 1
    sys.stderr.write('EDGES: ' + str(edges) + '\n')
    
    drawSuperPolygonSituation(polygon, zones, stableZones, superPolygon, pols, pictureNameAfter)
    starts = reverseAndTestZones(pols, superPolygon, polygon, zones)
    drawSuperPolygonSituation(polygon, zones, stableZones, superPolygon, starts, pictureNameBefore)
    for i in range(len(starts)):
        print('reverse polygon ', i)
        print(starts[i][0], ';', starts[i][1])
        for j in range(len(starts[i][0])):
            print('    ', starts[i][0][j])
        print('end of reverse polygon ', i)
    ''' 
    for i in range(len(starts)):
        sys.stderr.write(str(i) + ' polygons painted from ' + str(len(starts)) + '\n') 
        DrawMyPolygon(screen, starts[i][0], ((462+10*i)%256, (98+20*i)%256, (78+70*i)%256), 1, ((148+350*i)%256, (20+120*i)%256, (70+140*i)%256))
    '''
    #for (int i = 0; i < (int)starts.size(); ++i) {
    #    PaintStarPolygonInner(screen, starts[i].first, 462 + 10*i, 98 + 20*i, 78 + 70*i, 0);
    #    DrawMyPolygon(screen, starts[i].first, 148 + 350*i, 20 + 120*i, 70 + 140*i, 0);
    #}
   
    #pygame.display.flip()
    #pygame.image.save(screen, 'testSave.bmp')
    #waitEnd()

