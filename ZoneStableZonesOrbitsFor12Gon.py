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
pictureNameAfter = 'PlaneZone1SmallAfter.bmp'
pictureNameBefore = 'PlaneZone1SmallBefore.bmp'

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

def findMaxyMinxIndexInPolygon(pol):
    ans = 0
    for i in range(1, len(pol)):
        if pol[i].GetY() > pol[ans].GetY() or (pol[i].GetY() == pol[ans].GetY() and pol[i].GetX() < pol[ans].GetX()):
            ans = i
    return ans

def findMinyMinxIndexInPolygon(pol):
    ans = 0
    for i in range(1, len(pol)):
        if pol[i].GetY() < pol[ans].GetY() or (pol[i].GetY() == pol[ans].GetY() and pol[i].GetX() < pol[ans].GetX()):
            ans = i
    return ans


def drawSuperPolygonSituation(polygon, zones, stableZones, superPolygon, levelNumbers, coef, pictureName):
    
    minx, maxx, miny, maxy = getBoundsFromPolygon(superPolygon)
    newMinY = MyCipher(12)
    newMaxY = MyCipher(size_y - 12) 
    ay, by = getLinearFunction(miny, newMinY, maxy, newMaxY)
    polygon = makeScalingMyPolygon(polygon, ay, by, ay, by)
    zones = makeScalingMyPolygons(zones, ay, by, ay, by)
    stableZones = makeScalingMyPolygons(stableZones, ay, by, ay, by)
    superPolygon = makeScalingMyPolygon(superPolygon, ay, by, ay, by)
    
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

#    DrawMyPolygon(screen, superPolygon, (0, 255, 0), 0)
    pygame.display.flip()

    for i in range(len(splitting)):
        sys.stderr.write(str(i) + ' polygons painted from ' + str(len(splitting)) + '\n') 
        DrawMyPolygon(screen, splitting[i], ((462+10*i)%256, (98+20*i)%256, (78+70*i)%256), 1, ((148+350*i)%256, (20+120*i)%256, (70+140*i)%256))

    

    pygame.display.flip()
    pygame.image.save(screen, pictureName)

def getZoneNumber(point, zones):
    for i in range(len(zones)):
        if isPointInPolygon(point, zones[i]):
            return i
    return None

#return (component, period_of_component)
def findComponentOfPointWithPeriod(point, polygon, zones):
    startPoint = point
    currentZoneNumber = getZoneNumber(point, zones)
    currentPolygon = zones[currentZoneNumber].copy()
    startEqualPolygon = currentPolygon.copy()
    iterations = 0
    ans = None
    while True: 
        if isPointOnBoundOfPolygon(point, currentPolygon):
            return None

        currentZoneNumber = getZoneNumber(point, zones)
        newPolygons = splitGoodPolygonByZones(currentPolygon, polygon, zones)
        newPolygons = [tup[0] for tup in newPolygons if tup[1] == currentZoneNumber]
        
        newPolygon = None
        for pol in newPolygons:
            if isPointInPolygon(point, pol):
                newPolygon = pol
                break
        assert not(newPolygon is None)

        if not(areMyPolygonsEqual(newPolygon, currentPolygon)):
            iterations = 0
            startEqualPolygon = newPolygon.copy()
        
        if iterations > 0 and areMyPolygonsEqual(currentPolygon, startEqualPolygon):
            ans = (startEqualPolygon, iterations)
            break
        #if iterations == 10:
        #    return (startEqualPolygon, iterations)
        
        iterations += 1
        currentPolygon = MakeZoneOuterBilliard(newPolygon, polygon, True)
        point = MakeZoneOuterBilliardPoint(point, polygon)
        print('findComponentOfPointWithPeriod: area is ', getDoubledOrientedArea(currentPolygon), ', iterations is ', iterations)
        #if iterations == 50:
        #    fsdfdsf
    while not(isPointInPolygon(startPoint, ans[0])):
        ans = (MakeZoneOuterBilliard(ans[0], polygon, True), ans[1])
    return ans

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    c0 = MyPoint(Fraction(20), Fraction(-280))
    c1 = MyPoint(Fraction(20), Fraction(20))
   
    polygon = Get12gonFromSegment(c0, c1)
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)

    #DrawRayMyPoint(screen, MyPoint(Fraction(256), Fraction(256)), MyPoint(Fraction(1512), Fraction(512)), (0, 0, 120), 0)

    
    raysColor = (57, 179, 218)
    #print('polygon: ', polygon)
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 2)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 2)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 2)
    DrawRayMyPoint(screen, polygon[5], polygon[4], raysColor, 2)
    DrawRayMyPoint(screen, polygon[6], polygon[5], raysColor, 2)
    

    firstComponent = getFirstComponent(polygon)
    #boundColor = (21, 43, 49)
    boundColor = raysColor
    DrawMyPolygon(screen, firstComponent, boundColor, 2)
    zones = getZonesFrom12Gon(polygon)
    #print('Zones...: zones = ', zones)
    stableZones = getStableZonesFrom12Gon(polygon, zones)
    centerStableZone3 = GetCenter(stableZones[3])

    '''
    for i in range(0, 4):
        stZone = findComponentOfPointWithPeriod(GetCenter(stableZones[i]), polygon, zones)
        DrawMyPolygon(screen, stZone[0], boundColor, 0) 
    for i in range(0, 3):
        stPoint = rotate150ClockwiseAround(GetCenter(stableZones[i]), centerStableZone3)
        stZone = findComponentOfPointWithPeriod(stPoint, polygon, zones)
        DrawMyPolygon(screen, stZone[0], boundColor, 0)
        print('RESULT ITERATIONS: ', stZone[1])
    pygame.display.flip()
    waitEnd()
    sys.exit(0)
    '''
    
    center = (polygon[0] + polygon[6]) * MyCipher(Fraction(1, 2))
    #DrawPoint(screen, center, (234, 56, 78), 2)
    ukp = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
    newc = reflect(center, ukp)
    #DrawPoint(screen, ukp, (140, 20, 70), 3)
    newnewc = GetCenter(stableZones[0])
    newmidc = GetCenter(stableZones[3])

    coef = (newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    def Gamma(pol):
        return compressPolygon(pol, coef, polygon[1])

    pygame.display.flip()
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
    


    for i in range(0, 1):
        print('RANK ', i, ':')
        for j in range(len(currentComponents)):
            num = i * len(currentComponents) + j
            color = ((234 + 57 * num) % 256, (56 + 20 * num * num ) % 256, (78 + 134 * num * num * num) % 256)
            currentPolygon = currentComponents[j].copy()
            
            iteration = 0
            while True:
                DrawMyPolygon(screen, currentPolygon, boundColor, 2, color)
                iteration += 1
                currentPolygon = MakeZoneOuterBilliard(currentPolygon, polygon, True)
                if areMyPolygonsEqual(currentPolygon, currentComponents[j]):
                    break
            print('stable zone ', j, ': ', iteration, ' iterations')
            pygame.display.flip()
        '''
        if i == 0:
            drawSegment(screen, centerStableZone3, GetCenter(currentComponents[6]), (255, 0, 0), 3)
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
            drawGeneralizedSegment(screen, GeneralizedSegment(p1, p2, True, True), (255, 0, 0), 3)
            drawGeneralizedSegment(screen, GeneralizedSegment(p3, p4, True, True), (255, 0, 0), 3)
        '''

        for j in range(len(currentComponents)):
            currentComponents[j] = Gamma(currentComponents[j])
    
    for i in range(0, 4):
        DrawPoint(screen, GetCenter(stableZones[i]), (0, 0, 0), 3)
    pygame.image.save(screen, 'testSave.bmp')
    #waitEnd()

