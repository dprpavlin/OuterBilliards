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
#pictureNameAfter = 'RocketBigMiddleTestAfter.bmp'
#pictureNameBefore = 'RocketBigMiddleTestBefore.bmp'

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

#polygon2 should be result of moving of polygon1
def fromPolygonToPolygonMoving(point, polygon1, polygon2):
    return fromSystemToSystem(point, linearSystemFromPolygon(polygon1), linearSystemFromPolygon(polygon2)) 

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

def drawBaselinePicture(polygon, zones, stableZones):
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


class SelfSimilarityFor12Gon:
    def __init__(self, c0, c1):
        self.polygon = Get12gonFromSegment(c0, c1)
        self.firstComponent = getFirstComponent(self.polygon)
        self.zones = getZonesFrom12Gon(self.polygon)
        self.stableZones = getStableZonesFrom12Gon(self.polygon, self.zones)
        
        center = (self.polygon[0] + self.polygon[6]) * MyCipher(Fraction(1, 2))
        ukp = lineIntersection(self.polygon[1], self.polygon[2], self.polygon[6], self.polygon[5])
        newc = reflect(center, ukp)
        newnewc = GetCenter(self.stableZones[0])
        newmidc = GetCenter(self.stableZones[3])
        
        self.midScale = (newmidc.GetX() - self.polygon[1].GetX()) / (newc.GetX() - self.polygon[1].GetX())
        self.smallScale = (newnewc.GetX() - self.polygon[1].GetX()) / (newc.GetX() - self.polygon[1].GetX())

        #self.superPolygonBig = getFirstComponent(self.polygon).copy() #rocket small(3 strings)
        #self.superPolygonBig = compressPolygon(self.superPolygonBig, self.smallScale, self.polygon[1])
        # Plane zone 1
        num = 0
        for i in range(len(self.stableZones[1])):
            if self.stableZones[1][i].GetY() < self.stableZones[1][num].GetY():
                num = i
        if num > 0:
            num -= len(self.stableZones[1])
        self.superPolygonBig = [self.polygon[1], self.stableZones[1][num-1], self.stableZones[1][num], self.stableZones[1][num+1]]
        # end of Plane zone 1
        self.superPolygonSmall = compressPolygon(self.superPolygonBig, self.smallScale, self.polygon[1])

        self.localZonesAfter = tryMakeFirstReturnMapOnlyPolygons([self.superPolygonBig], self.superPolygonBig, self.polygon, self.zones, 10000000)
        self.localZonesBefore = reverseAndTestZonesOnlyPolygons(self.localZonesAfter, self.superPolygonBig, self.polygon, self.zones)

    def gammaPoint(self, point):
        return compressVector(point, self.smallScale, self.polygon[1])

    def gammaPolygon(self, polygon):
        return compressPolygon(polygon, self.smallScale, self.polygon[1])
    
    #def checkSelfSimilarity(self):
    #    realLocalZonesSmallAfter 

    def drawSuperPolygonSituation(self, splitting, pictureName):
        return drawSuperPolygonSituation(self.polygon, self.zones, self.stableZones, self.superPolygonBig, splitting, pictureName)
    
    def movePointByZoneRule(self, point, zoneNumber):
        assert zoneNumber >= 0 and zoneNumber < len(self.localZonesBefore)
        return fromPolygonToPolygonMoving(point, self.localZonesBefore[zoneNumber], self.localZonesAfter[zoneNumber]) 
        
    def makeMapPoint(self, point):
        assert isPointInPolygon(point, self.superPolygonBig)
        for i in range(len(self.localZonesBefore)):
            if (isPointOnBoundOfPolygon(point, self.localZonesBefore[i])):
                return None
        for i in range(len(self.localZonesBefore)):
            if isPointInPolygon(point, self.localZonesBefore[i]):
                ans = self.movePointByZoneRule(point, i) 
                return (ans, i)
     
    def makeMapPolygon(self, polygon):
        #print('makeMapPolygon: polygon: ', polygon)
        for i in range(len(self.localZonesBefore)):
            if (arePointsInPolygon(polygon, self.localZonesBefore[i])):
                ans = [self.movePointByZoneRule(point, i) for point in polygon]
                #print('makeMapPolygon: ANS: ', ans)
                return (ans, i)
        DrawMyPolygon(pygame.display.get_surface(), polygon, (0, 255, 0), 0)
        pygame.display.flip()
        waitEnd()
        assert False

    def drawSmallZones(self, pictureName):
        smallZones = [self.gammaPolygon(polygon) for polygon in self.localZonesBefore]
        return drawSuperPolygonSituation(self.polygon, self.zones, self.stableZones, self.superPolygonBig, smallZones, pictureName)

    def drawOrbitOfSmallZones(self, pictureName):
        drawBaselinePicture(self.polygon, self.zones, self.stableZones)
        smallZones = [self.gammaPolygon(polygon) for polygon in self.localZonesBefore]
        screen = pygame.display.get_surface()
        for i in range(len(smallZones)):
            iteration = 0
            smallZone = smallZones[i].copy()
            while True:
                iteration += 1
                #print('drawOrbitOfSmallZones: polygon ', i, ', iteration ', iteration, f=sys.stderr)
                sys.stderr.write('drawOrbitOfSmallZones: polygon ' + str(i) +  ', iteration '+ str(iteration) + '\n')
                DrawMyPolygon(screen, smallZone, ((148 + 350*i) % 256, (462 + 240*i)%256, (78 + 60*i)%256), 0)
                smallZone = self.makeMapPolygon(smallZone)[0]
                if arePointsInPolygon(smallZone, self.superPolygonSmall):
                    break
            assert areMyPolygonsEqual(smallZone, self.gammaPolygon(self.localZonesAfter[i]))
            print('polygon ', i, ': ', len(smallZone), ' vertexes, ', iteration, 'iterations')
        pygame.display.flip()
        pygame.image.save(screen, pictureName)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    #screen = pygame.display.get_surface()
    
    c0 = MyPoint(Fraction(20), Fraction(-180))
    c1 = MyPoint(Fraction(20), Fraction(20))
    ss = SelfSimilarityFor12Gon(c0, c1)
    #ss.drawSuperPolygonSituation(ss.localZonesBefore, 'testLocalZonesBefore.bmp')
    #ss.drawSuperPolygonSituation(ss.localZonesAfter, 'testLocalZonesAfter.bmp')
    #ss.drawSuperPolygonSituation([ss.makeMapPolygon(polygon)[0] for polygon in ss.localZonesBefore], 'testLocalZonesMakeMap.bmp')
    #ss.drawSmallZones('testSmallZones.bmp')
    ss.drawOrbitOfSmallZones('testSmallZonesAndMapMiddleSmallRocket.bmp')
    sys.exit(0)


