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

if __name__ == '__main__':
    pygame.init()
    size_x = 512 * 2
    size_y = 512 * 8
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    c0 = MyPoint(Fraction(20), Fraction(-10))
    c1 = MyPoint(Fraction(20), Fraction(140))
    
    polygon = Get12gonFromSegment(c0, c1)
    DrawMyPolygon(screen, polygon, (0, 0, 120), 0)

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
    #DrawMyPolygon(screen, firstComponent, (21, 43, 49), 0)
    zones = getZonesFrom12Gon(polygon)
    #print('Zones...: zones = ', zones)
    stableZones = getStableZonesFrom12Gon(polygon, zones)
    for zone in stableZones:
        print(findHashForPolygon(zone))
    
    center = (polygon[0] + polygon[6]) * MyCipher(Fraction(1, 2))
    DrawPoint(screen, center, (234, 56, 78), 2)
    ukp = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
    newc = reflect(center, ukp)
    DrawPoint(screen, ukp, (140, 20, 70), 3)
    newnewc = GetCenter(stableZones[0])
    newmidc = GetCenter(stableZones[3])
    
    superPolygon = getFirstComponent(polygon)
    #for i in range(len(superPolygon)):
    #    superPolygon[i] = polygon[1] + (superPolygon[i] - polygon[1]) * (newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    
    p = GetCenter(stableZones[3])
    p = polygon[1] + (p - polygon[1]) *  (newmidc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())

    #comp = findComponentOfPointWithPeriod(p, polygon, zones)
    #print("PERIOD: ", comp[1])
    #comp = comp[0]
    #for i in range(len(comp)):
    #    comp[i] = polygon[1] + (comp[i] - polygon[1]) /  (newnewc.GetX() - polygon[1].GetX()) * (newc.GetX() - polygon[1].GetX())

    #print(arePolygonsEqual(comp, stableZones[3]))
#def tryMakeFirstReturnMapOnlyPolygons(startPolygons, goodPolygon, polygon, zones, maxKol = 100) :
#def reverseAndTestZones(pols, goodPolygon, polygon, zones):
    
    #waitEnd()

    #    firstComponent[i] = polygon[1] + (firstComponent[i] - polygon[1]) * (newmidc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())

    for i in range(len(superPolygon)):
        superPolygon[i] = polygon[1] + (superPolygon[i] - polygon[1]) * (newmidc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    middlePolygon = superPolygon.copy()
    for i in range(len(superPolygon)):
        superPolygon[i] = polygon[1] + (superPolygon[i] - polygon[1]) * (newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    DrawMyPolygon(screen, superPolygon, (0, 255, 0), 0)
    pygame.display.flip()

    zones4After = tryMakeFirstReturnMapOnlyPolygons([middlePolygon], middlePolygon, polygon, zones, maxKol = 100)
    zones4Before = reverseAndTestZonesOnlyPolygons(zones4After, middlePolygon, polygon, zones)
    #zones4After = tryMakeFirstReturnMapOnlyPolygons([superPolygon], superPolygon, polygon, zones, maxKol = 10000000)
    #zones4Before = reverseAndTestZonesOnlyPolygons(zones4After, superPolygon, polygon, zones)
    #print("RESULTRESULT: ", len(zones4Before))
    
    DrawMyPolygon(screen, zones4Before[0], (255, 0, 0), 0)
    DrawMyPolygon(screen, zones4Before[1], (0, 255, 0), 0)
    DrawMyPolygon(screen, zones4Before[2], (0, 0, 255), 0)
    DrawMyPolygon(screen, zones4Before[3], (255, 255, 0), 0)
    DrawMyPolygon(screen, zones4Before[4], (127, 0, 0), 0)
    DrawMyPolygon(screen, zones4Before[5], (0, 127, 0), 0)
    DrawMyPolygon(screen, zones4Before[6], (0, 0, 127), 0)
    DrawMyPolygon(screen, zones4Before[7], (127, 127, 0), 0)

    pygame.display.flip()
    #pygame.image.save(screen, "pic12-superZones.bmp")
    pygame.image.save(screen, "pic12-middleZones.bmp")
    waitEnd()
    for zone in zones4Before:
        print(findAggregatedInfoAboutReturningTrajectoryForReturnMap(GetCenter(zone), middlePolygon, firstComponent, zones, polygon))
        print(findReturningTrajectoryForReturnMap(GetCenter(zone), middlePolygon, firstComponent, zones, polygon))

    def Gamma1(pol):
        return [polygon[1] + (p - polygon[1])*(newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX()) for p in pol]

    zones4BeforeCompressed = [Gamma1(z) for z in zones4Before]

    for zone in zones4BeforeCompressed:
        print(findAggregatedInfoAboutReturningTrajectoryForReturnMap(GetCenter(zone), superPolygon, middlePolygon, zones4Before, polygon))
        print(findReturningTrajectoryForReturnMap(GetCenter(zone), superPolygon, middlePolygon, zones4Before, polygon))
        


    pygame.display.flip()
    waitEnd()
    

    for i in range(len(zones4Before)):
        z = zones4Before[i]
        DrawMyPolygon(screen, z, ((148 + 774*i)%256, (20 + 75*i)%256, (70 + 13*i)%256), 0)
 
    pygame.display.flip()
    #waitEnd()
    
    ans = findPeriodicComponents(firstComponent, [superPolygon], polygon, zones, iterations = 20)
    #ans = findPeriodicComponents(firstComponent, [superPolygon], polygon, zones, 20, screen)
    ans, rems = ans
    #print(len(ans), "!!!!!!!")
    #pygame.display.flip()
    #waitEnd()
   
    #print(ans)
    for i in range(len(ans)):
        pol = ans[i][0].copy()
        print(len(pol))
        #print(findAggregatedInfoAboutPeriodicTrajectoryForReturnMap(GetCenter(pol), firstComponent, zones, polygon))
        #print(findPeriodicTrajectoryForReturnMap(GetCenter(pol), firstComponent, zones, polygon))
        print(findAggregatedInfoAboutPeriodicTrajectoryForReturnMap(GetCenter(pol), middlePolygon, zones4Before, polygon))
        print(findPeriodicTrajectoryForReturnMap(GetCenter(pol), middlePolygon, zones4Before, polygon))
        #for j in range(ans[i][1]):
        for j in range(1):
            DrawMyPolygon(screen, pol, ((148 + 350*i) % 256, (462 + 120*i)%256, (78 + 60*i)%256), 0)
            pol = MakeZoneOuterBilliard(pol, polygon, True)
        #print(ans[i][1], float(getDoubledOrientedArea(ans[i][0]))) 
    pygame.display.flip()
    waitEnd()
    
    '''superPolygon = firstComponent.copy()
    polygons = splitGoodPolygonByZones(superPolygon, polygon, zones)
    for i in range(len(polygons)):
        DrawMyPolygon(screen, polygons[i], ((148 + 350*i) % 256, (462 + 240*i)%256, (78 + 60*i)%256), 0)
    
    pygame.display.flip()
    waitEnd()
    '''



