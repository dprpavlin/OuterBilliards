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

def getZoneNumber(point, zones):
    for i in range(len(zones)):
        if isPointInPolygon(point, zones[i]):
            return i
    return None

def getZonePeriodOfZone(zone, polygon, zones):
    startZone = zone.copy()
    point = GetCenter(zone)
    iterations = 0
    while True:
        num = getZoneNumber(point, zones)
        assert not(isPointOnBoundOfPolygon(point, zones[num]))
        assert ([isPointInPolygon(p, zones[num]) for p in zone].count(False) == 0)
        point = MakeZoneOuterBilliardPoint(point, polygon)
        zone = MakeZoneOuterBilliard(zone, polygon, zones)
        iterations += 1
        if areMyPolygonsEqual(startZone, zone):
            return iterations

#return (component, period_of_component)
def findComponentOfPointWithPeriod(point, polygon, zones):
    startPoint = point
    currentZoneNumber = getZoneNumber(point, zones)
    currentPolygon = zones[currentZoneNumber].copy()
    startEqualPolygon = currentPolygon.copy()
    iterations = 0
    ans = None
    print('findComponentOfPoint started')
    number = 0
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
        number += 1
        if number % 50 == 0:
            print('findComponentOfPointWithPeriod: area is ', getDoubledOrientedArea(currentPolygon), ', number is ', iterations)
        #if iterations == 50:
        #    fsdfdsf
    print('findComponentOfPoint finished')
    while not(isPointInPolygon(startPoint, ans[0])):
        ans = (MakeZoneOuterBilliard(ans[0], polygon, True), ans[1])
    return ans

#find (a, b) - linear function f(x) = a*x + b so that f(x01) = x02, f(x11) = x12
def getLinearFunction(x01, x02, x11, x12):
    return (x02 - x12) / (x01 - x11) , (x01*x12 - x11*x02) / (x01 - x11)

class LinearSystem:
    def __init__(self, c, v1, v2):
        self.c = c
        self.v1 = v1
        self.v2 = v2
        assert v1*v2 != type(v1.GetX())(0)

    def getCoefs(self, p):
        v = p - self.c
        a = (v*self.v2) / (self.v1*self.v2)
        b = (self.v1*v) / (self.v1*self.v2)
        return (a, b)

    def getPoint(self, coefs):
        a, b = coefs
        return self.c + self.v1 * a + self.v2 * b

def linearSystemFromPolygon(polygon):
    assert len(polygon) >= 3
    return LinearSystem(polygon[0], polygon[-1] - polygon[0], polygon[1] - polygon[0])

def fromSystemToSystem(point, ls1, ls2):
    return ls2.getPoint(ls1.getCoefs(point))

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    c0 = MyPoint(Fraction(20), Fraction(-580))
    c1 = MyPoint(Fraction(20), Fraction(20))
   
    polygon = Get12gonFromSegment(c0, c1)
    DrawMyPolygon(screen, polygon, (135, 206, 235), 0)

    #DrawRayMyPoint(screen, MyPoint(Fraction(256), Fraction(256)), MyPoint(Fraction(1512), Fraction(512)), (0, 0, 120), 0)

    
    raysColor = (57, 179, 218)
    #print('polygon: ', polygon)
    DrawRayMyPoint(screen, polygon[0], polygon[1], raysColor, 1)
    DrawRayMyPoint(screen, polygon[1], polygon[2], raysColor, 1)
    DrawRayMyPoint(screen, polygon[3], polygon[2], raysColor, 1)
    DrawRayMyPoint(screen, polygon[4], polygon[3], raysColor, 1)
    DrawRayMyPoint(screen, polygon[5], polygon[4], raysColor, 1)
    DrawRayMyPoint(screen, polygon[6], polygon[5], raysColor, 1)
    

    firstComponent = getFirstComponent(polygon)
    boundColor = (21, 43, 49)
    DrawMyPolygon(screen, firstComponent, boundColor, 1)
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
    coefMid = (newmidc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    def Gamma(pol):
        return compressPolygon(pol, coefMid, polygon[1])

    #DrawMyPolygon(screen, stableZones[3], (0, 127, 0), 0)
    firstComponent = Gamma(firstComponent)
    #DrawMyPolygon(screen, firstComponent, (255, 255, 0), 0)
    pygame.display.flip()

    #pygame.image.save(screen, 'testSave.bmp')
    #waitEnd()
    
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
    
    #zone0 = stableZones[3]
    #zone1 = stableZones[2]
    #zone2 = MakeZoneOuterBilliard(currentComponents[8], polygon, True)
    fc = getFirstComponent(polygon)
    fc = compressPolygon(fc, coefMid, polygon[1])
    DrawMyPolygon(screen, fc, (0, 100, 0), 0)
    
    zone0 = stableZones[2]
    zone1 = stableZones[1]
    zone2 = compressPolygon(stableZones[3], coef, polygon[1])
    for i in range(35):
        zone2 = MakeZoneOuterBilliard(zone2, polygon, True)

    DrawMyPolygon(screen, zone0, (255, 0, 0), 0) 
    DrawMyPolygon(screen, zone1, (255, 0, 0), 0) 
    DrawMyPolygon(screen, zone2, (255, 0, 0), 0)

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
    c0, c1, c2 = GetCenter(zone0), GetCenter(zone1), GetCenter(zone2)
    pygame.display.flip()
    pygame.image.save(screen, 'testSave.bmp')
    sys.exit(0)
    
    def myOperation(c, zone, number):
        period = getZonePeriodOfZone(zone, polygon, zones)
        print('iteration ', number, ': ', period, ' iterations')        
        sys.stderr.write('iteration ' + str(number) + ': ' + str(period) + ' iterations' + '\n')
        sys.stderr.flush()
        newc = fromSystemToSystem(c, lsBig, lsSmall)
        newZone = [fromSystemToSystem(p, lsBig, lsSmall) for p in zone]
    #    newComponent, period = findComponentOfPointWithPeriod(newc, polygon, zones)
    #    assert areMyPolygonsEqual(newZone, newComponent)
    #    print('iteration ', number, ': ', period, ' iterations')
        return (newc, newZone)

    for number in range(100):
        c0, zone0 = myOperation(c0, zone0, number)
        c1, zone1 = myOperation(c1, zone1, number)
        c2, zone2 = myOperation(c2, zone2, number)

    pygame.image.save(screen, 'testSave.bmp')
    #waitEnd()

