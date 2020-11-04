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

def drawPeriodic(screen, pols, polygon, shift, raysColor, numIter = 15):
    pols = [pol.copy() for pol in pols]
    
    for base in pols:
        for i in range(numIter):
            b = base.copy()
            per = GetPeriod(GetCenter(b), polygon)
            print(per)
            for i in range(per):
                if per % 2 == 1:
                    DrawMyPolygon(screen, b, raysColor, 2, getColor(per*2))
                    c = GetCenter(b)
                    DrawPoint(screen, c, getColor(per), 2)
                else:
                    DrawMyPolygon(screen, b, raysColor, 2, getColor(per))
                b = MakeReflectionOuterBilliard(b, polygon, True)
            for i in range(len(base)):
                base[i] = base[i] + shift

def drawPic3(screen):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(512*3 - 60), Fraction(512*3 - 60))
    c1 = MyPoint(Fraction(512*3 - 60), Fraction(512*3 + 60))
    
    polygon = Get3gonFromSegment(c0, c1);
    raysColor = (47, 79, 79)
    
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 0))
    base6 = Get6gonFromSegment(c1, c1 + c1 - c0)
    base3 = Get3gonFromSegment(base6[2], base6[1])

    DrawMyPolygon(screen, base3, raysColor, 2, (0, 120, 0))
    DrawMyPolygon(screen, base6, raysColor, 2, (120, 0, 0))

    shift =  c1 - c0 + c1 - c0

    drawPeriodic(screen, [base3, base6], polygon, shift, raysColor)
    pygame.image.save(screen, 'pic3.bmp')
        
    waitEnd()

# something strange with sequence of periods, but the picture is OK
def drawPic6(screen):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(512*3 - 60), Fraction(512*3 - 60))
    c1 = MyPoint(Fraction(512*3 - 60), Fraction(512*3 + 60))
    
    polygon = Get6gonFromSegment(c0, c1);
    raysColor = (47, 79, 79)
    
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 0))
    base3 = Get3gonFromSegment(c1, c1 + c1 - c0)
    base61 = Get6gonFromSegment(base3[2], base3[1])
    base62 = [rotate60ClockwiseAround(p, GetCenter(polygon)) for p in base61]

    #DrawMyPolygon(screen, base3, raysColor, 2, (0, 120, 0))
    #DrawMyPolygon(screen, base6, raysColor, 2, (120, 0, 0))

    shift =  c1 - c0 + c1 - c0

    drawPeriodic(screen, [base3, base61, base62], polygon, shift, raysColor)
    pygame.image.save(screen, 'pic6.bmp')
        
    waitEnd()

def drawPic4(screen):
    screen.fill((0, 0, 0))
    c0 = MyPoint(Fraction(512*3 - 60), Fraction(512*3 - 60))
    c1 = MyPoint(Fraction(512*3 - 60), Fraction(512*3 + 60))
    
    polygon = Get4gonFromSegment(c0, c1);
    raysColor = (47, 79, 79)
    
    DrawMyPolygon(screen, polygon, raysColor, 2, (0, 0, 0))
    base4 = Get4gonFromSegment(c1, c1 + c1 - c0)

    shift = c1 - c0

    drawPeriodic(screen, [base4], polygon, shift, raysColor, 30)
    pygame.image.save(screen, 'pic4.bmp')
        
    waitEnd()

if __name__ == '__main__':
    pygame.init()
    size_x = 512 * 6
    size_y = 512 * 6
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    
    #drawPic3(screen)
    #drawPic6(screen)
    drawPic4(screen)
    waitEnd()
