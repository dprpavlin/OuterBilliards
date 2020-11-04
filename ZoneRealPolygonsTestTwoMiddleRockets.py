from workWith12Gon import *
from point2D import *
from segmentIntersection import *
from billiard import *
from absqrtn import *
from fractions import *

import pygame, sys
from pygame.locals import *

size_x = 512 * 5 // 2
size_y = 512 * 4
pictureNameAfter = 'RocketBigMiddleTestAfter.bmp'
pictureNameBefore = 'RocketBigMiddleTestBefore.bmp'

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

def areMyPolygonsEqual(polygon1, polygon2):
    if len(polygon1) != len(polygon2):
        return False
    num = -1
    l = len(polygon1)
    for i in range(l):
        if polygon1[0] == polygon2[i]:
            num = i
            break
    if num < 0:
        return False
    isOK = True
    for i in range(l):
        if polygon1[-i] != polygon2[num-i]:
            isOK = False
            break
    if isOK:
        return True
    isOK = True
    for i in range(l):
        if polygon1[i] != polygon2[num-i]:
           isOK = False
           break
    return isOK

def drawSuperPolygonSituation(polygon, zones, stableZones, superPolygon, splitting, pictureName):
    if type(splitting[0]) == tuple:
        splitting = [s[0] for s in splitting]
    
    minx, maxx, miny, maxy = getBoundsFromPolygon(superPolygon)
    newMinY = MyCipher(12)
    newMaxY = MyCipher(size_y - 12) 
    ay, by = getLinearFunction(miny, newMinY, maxy, newMaxY)
    polygon = makeScalingMyPolygon(polygon, ay, by, ay, by)
    zones = makeScalingMyPolygons(zones, ay, by, ay, by)
    stableZones = makeScalingMyPolygons(stableZones, ay, by, ay, by)
    superPolygon = makeScalingMyPolygon(superPolygon, ay, by, ay, by)
    splitting = makeScalingMyPolygons(splitting, ay, by, ay, by)
    
    screen = pygame.display.get_surface()
    screen.fill((0, 0, 0))
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)
    
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

    DrawMyPolygon(screen, superPolygon, (0, 255, 0), 0)
    pygame.display.flip()

    for i in range(len(splitting)):
        sys.stderr.write(str(i) + ' polygons painted from ' + str(len(splitting)) + '\n') 
        DrawMyPolygon(screen, splitting[i], ((462+10*i)%256, (98+20*i)%256, (78+70*i)%256), 1, ((148+350*i)%256, (20+120*i)%256, (70+140*i)%256))

    pygame.display.flip()
    pygame.image.save(screen, pictureName)

if __name__ == '__main__':
    #pygame.init()
    #window = pygame.display.set_mode((size_x, size_y))
    #pygame.display.set_caption('My own little world')
    #screen = pygame.display.get_surface()
    c0 = MyPoint(Fraction(20), Fraction(-60))
    c1 = MyPoint(Fraction(20), Fraction(20))
   
    polygon = Get12gonFromSegment(c0, c1)

    firstComponent = getFirstComponent(polygon)
    zones = getZonesFrom12Gon(polygon)
    stableZones = getStableZonesFrom12Gon(polygon, zones)
    
    center = (polygon[0] + polygon[6]) * MyCipher(Fraction(1, 2))
    ukp = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
    newc = reflect(center, ukp)
    newnewc = GetCenter(stableZones[0])
    newmidc = GetCenter(stableZones[3])
    
    superPolygon = getFirstComponent(polygon).copy() #rocket(3 strings)

    for i in range(len(superPolygon)):
        superPolygon[i] = polygon[1] + (superPolygon[i] - polygon[1]) * (newmidc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    superPolygonBig = superPolygon.copy()
    superPolygonSmall = superPolygon.copy()
    for i in range(len(superPolygon)):
        superPolygonSmall[i] = polygon[1] + (superPolygonSmall[i] - polygon[1]) * (newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())

    hpsBig = tryMakeFirstReturnMapOnlyPolygons([superPolygonBig], superPolygonBig, polygon, zones, 10000000)
    hpsSmall = tryMakeFirstReturnMapOnlyPolygons([superPolygonSmall], superPolygonSmall, polygon, zones, 10000000)
    print(hpsBig)
    #print(hpsSmall)
    #print(hpsBig[0])
   
    #hpsBig = hpsBig[0]
    #for i in range(len(hpsBig)):
    #    hpsBig[i] = hpsBig[i][0]
    #print(hpsBig)
    #sys.exit(0)

    print('LENGTH BIG: ', len(hpsBig))
    print('LENGTH SMALL: ', len(hpsSmall))
    
    #print(len(hpsBig[0]), ", ", len(hpsBig[1]))
    #print(len(hpsBig[0]), ", ", len(hpsBig[1]), file=sys.stderr)
    #print(len(hpsSmall[0]), ", ", len(hpsSmall[1]))
    #print(len(hpsSmall[0]), ", ", len(hpsSmall[1]), file=sys.stderr)

    #hpsBig = hpsBig[0]
    #hpsSmall = hpsSmall[0]
    #assert len(hpsBig) == len(hpsSmall)

    hpsBigCompressed = hpsBig.copy()

    for i in range(len(hpsBigCompressed)):
        for j in range(len(hpsBigCompressed[i])):
            hpsBigCompressed[i][j] = polygon[1] + (hpsBigCompressed[i][j] - polygon[1]) * (newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())

    #hpsSmall = hpsBigCompressed
    startsBig = reverseAndTestZonesOnlyPolygons(hpsBig, superPolygon, polygon, zones)
    startsSmall = reverseAndTestZonesOnlyPolygons(hpsSmall, superPolygon, polygon, zones)

    
    for i in range(len(hpsBigCompressed)):
        print(i, ': ')
        num = [-1]
        for j in range(len(hpsSmall)):
            if areMyPolygonsEqual(hpsBigCompressed[i], hpsSmall[j]):
                num.append(j)
        print(num)



    """for (int i = 0; i < (int)hps.first.size(); ++i) {
        PaintStarPolygonInner(screen, hps.first[i].first, 462 + 10*i, 98 + 20*i, 78 + 70*i, 0);
        DrawMyPolygon(screen, hps.first[i].first, 148 + 350*i, 20 + 120*i, 70 + 140*i, 0);
    }
    for (int i = 0; i < (int)hps.second.size(); ++i) {
        PaintStarPolygonInner(screen, hps.second[i].first, 148 + 10*i, 20*i, 70*i, 0);
        DrawMyPolygon(screen, hps.second[i].first, 112 + 350*i, 32 + 120*i, 253 + 140*i, 2);
    }"""
    
    """
    print("FirstReturnMap To found\n") 
    polsSmall = []
    for i in range(len(hpsSmall[0])):
        print('polygon', i)
        print(len(hpsSmall[0][i][0]), ":")
        for j in range(len(hpsSmall[0][i][0])):
            print('   ', hpsSmall[0][i][0][j])
        print('end of polygon', i)
        polsSmall.append(hpsSmall[0][i][0])

    print('===================\n')
    print("FirstReturnMap To found\n") 
    polsBig = []
    for i in range(len(hpsBig[0])):
        print('polygon', i)
        print(len(hpsBig[0][i][0]), ":")
        for j in range(len(hpsBig[0][i][0])):
            print('   ', hpsBig[0][i][0][j])
        print('end of polygon', i)
        polsBig.append(hpsBig[0][i][0])
    print('===================\n')
    """
    


    #drawSuperPolygonSituation(polygon, zones, stableZones, superPolygon, pols, pictureNameAfter)
    #starts = reverseAndTestZones(pols, superPolygon, polygon, zones)
    #drawSuperPolygonSituation(polygon, zones, stableZones, superPolygon, starts, pictureNameBefore)
    #for i in range(len(starts)):
    #    print('reverse polygon ', i)
    #    print(starts[i][0], ';', starts[i][1])
    #    for j in range(len(starts[i][0])):
    #        print('    ', starts[i][0][j])
    #    print('end of reverse polygon ', i)
    
    
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

