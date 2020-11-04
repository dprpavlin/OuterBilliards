from workWith12Gon import *
from point2D import *
from segmentIntersection import *
from billiard import *
from absqrtn import *
from fractions import *

import pygame, sys
from pygame.locals import *

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
    size_x = 512
    size_y = 512 * 4
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    c0 = MyPoint(Fraction(20), Fraction(-360))
    c1 = MyPoint(Fraction(20), Fraction(20))
   
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
    
    '''superPolygon = firstComponent.copy()
    polygons = splitGoodPolygonByZones(superPolygon, polygon, zones)
    for i in range(len(polygons)):
        DrawMyPolygon(screen, polygons[i], ((148 + 350*i) % 256, (462 + 240*i)%256, (78 + 60*i)%256), 0)
    
    pygame.display.flip()
    waitEnd()
    '''

    for i in range(0, 4):
        DrawMyPolygon(screen, stableZones[i], ((148 + 350*i) % 256, (462 + 120*i)%256, (78 + 60*i)%256), 0)

    pygame.display.flip()
   
    center = (polygon[0] + polygon[6]) * MyCipher(Fraction(1, 2))
    DrawPoint(screen, center, (234, 56, 78), 2)
    ukp = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
    newc = reflect(center, ukp)
    DrawPoint(screen, ukp, (140, 20, 70), 3)
    newnewc = GetCenter(stableZones[0])
    newmidc = GetCenter(stableZones[3])
    
    pygame.display.flip()

     
    superPolygon = getFirstComponent(polygon)
    #superPolygon = getFirstComponent(polygon).copy()
    #for i in range(len(superPolygon)):
    #    superPolygon[i] = polygon[1] + (superPolygon[i] - polygon[1]) * (newmidc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    
    for i in range(len(superPolygon)):
        superPolygon[i] = polygon[1] + (superPolygon[i] - polygon[1]) * (newnewc.GetX() - polygon[1].GetX()) / (newc.GetX() - polygon[1].GetX())
    DrawMyPolygon(screen, superPolygon, (255, 255, 0), 0)
    pygame.display.flip()

    pygame.display.flip()
    pygame.image.save(screen, 'testSave.bmp')
    waitEnd()

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

    hps = tryMakeFirstReturnMap([superPolygon], superPolygon, polygon, zones, 20000)
    print('LENGTH: ', len(hps[0]), len(hps[1]))
    
    #for hp in hps[0]:
        #print(hp)
    #    print(len(hp[0]))
    #    DrawMyPolygon(screen, hp[0], (255, 0, 0), 1, makeColorFromHash(hp[1]))
    #print('=====')
    #for hp in hps[1]:
        #print(hp)
    #    DrawMyPolygon(screen, hp[0], (0, 0, 255), 1, makeColorFromHash(hp[1]))

    print(len(hps[0]), ", ", len(hps[1]))
    print(len(hps[0]), ", ", len(hps[1]), file=sys.stderr)
    """for (int i = 0; i < (int)hps.first.size(); ++i) {
        PaintStarPolygonInner(screen, hps.first[i].first, 462 + 10*i, 98 + 20*i, 78 + 70*i, 0);
        DrawMyPolygon(screen, hps.first[i].first, 148 + 350*i, 20 + 120*i, 70 + 140*i, 0);
    }
    for (int i = 0; i < (int)hps.second.size(); ++i) {
        PaintStarPolygonInner(screen, hps.second[i].first, 148 + 10*i, 20*i, 70*i, 0);
        DrawMyPolygon(screen, hps.second[i].first, 112 + 350*i, 32 + 120*i, 253 + 140*i, 2);
    }"""
    

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
    starts = reverseAndTestZones(pols, superPolygon, polygon, zones)
    for i in range(len(starts)):
        print('reverse polygon ', i)
        print(starts[i][0], ';', starts[i][1])
        for j in range(len(starts[i][0])):
            print('    ', starts[i][0][j])
        print('end of reverse polygon ', i)
     
    for i in range(len(starts)):
        sys.stderr.write(str(i) + ' polygons painted from ' + str(len(starts)) + '\n') 
        DrawMyPolygon(screen, starts[i][0], ((462+10*i)%256, (98+20*i)%256, (78+70*i)%256), 1, ((148+350*i)%256, (20+120*i)%256, (70+140*i)%256))
    #for (int i = 0; i < (int)starts.size(); ++i) {
    #    PaintStarPolygonInner(screen, starts[i].first, 462 + 10*i, 98 + 20*i, 78 + 70*i, 0);
    #    DrawMyPolygon(screen, starts[i].first, 148 + 350*i, 20 + 120*i, 70 + 140*i, 0);
    #}
   
    pygame.display.flip()
    pygame.image.save(screen, 'testSave.bmp')
    #waitEnd()

