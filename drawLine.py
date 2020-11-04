import pygame
from pygame.locals import *
from point2D import *
from drawPoint import *
from segmentIntersection import *

import sys, utils

def drawSegment(surface, p1, p2, color, fat=1):
    p1 = ToIntTuple(p1)
    p2 = ToIntTuple(p2)
    pygame.draw.line(surface, color, p1, p2, fat)

def drawGeneralizedSegment(surface, segment, color, fat=1):
    T = type(segment.getFirstPoint().GetX())
    rect = surface.get_rect()

    a = [None] * 6
    
    p1 = segment.getFirstPoint()
    p2 = segment.getSecondPoint()
    #print('drawGeneralizedSegment arguments: ', p1, p2)

    if not(segment.isContinuedForFirst()) and IsValidPoint(surface, p1):
        a[0] = p1
        #a[0] = Point2D(float(p1.x), float(p1.y))
    if not(segment.isContinuedForSecond()) and IsValidPoint(surface, p2):
        a[1] = p2
        #a[1] = Point2D(float(p2.x), float(p2.y))

    
    leftUpCorner = Point2D(T(rect.x), T(rect.y))
    rightUpCorner = Point2D(T(rect.x + rect.w), T(rect.y))
    rightDownCorner = Point2D(T(rect.x + rect.w), T(rect.y + rect.h))
    leftDownCorner = Point2D(T(rect.x), T(rect.y + rect.h))

    #print('leftUpCorner ', leftUpCorner)
    #print('rightUpCorner ', leftUpCorner)
    #print('leftDownCorner ', leftDownCorner)
    #print('rightDownCorner ', rightDownCorner)

    a[2] = segmentIntersection(segment, GeneralizedSegment(leftUpCorner, rightUpCorner, False, False))
    a[3] = segmentIntersection(segment, GeneralizedSegment(rightUpCorner, rightDownCorner, False, False))
    a[4] = segmentIntersection(segment, GeneralizedSegment(rightDownCorner, leftDownCorner, False, False))
    a[5] = segmentIntersection(segment, GeneralizedSegment(leftDownCorner, leftUpCorner, False, False))
    
    #print('lstBefore: ', a[0], a[1], a[2], a[3], a[4], a[5])
    for i in range(0, 5):
        if a[i]:
            for j in range(i+1, 6):
                if a[j] and (a[i] == a[j]):
                    a[j] = None
    #print('lstPre: ', a[0], a[1], a[2], a[3], a[4], a[5])

    r = 0
    l = 0
    while (l < 6):
        if not a[l]:
            r = max(l, r)
            while (r < 6 and not a[r]):
                r += 1
            if r == 6:
                break
            t = a[l]
            a[l] = a[r]
            a[r] = t
        l += 1
    #print('lst: ', a[0], a[1], a[2], a[3], a[4], a[5])
    #if l <= 2:
    #    sys.exit()
    while len(a) > l:
        a.pop()
    if l >= 3:
        for i in range(2, l):
            if a[i]:
                assert (a[1] - a[0])*(a[i]-a[0]) == T(0), 'ERROR: point ' + str(i) + ' is not on line...'

        a = utils.sort(a, ByManhattenDistanceComparator(a[0]))
        a = utils.sort(a, ByManhattenDistanceComparator(a[0]))
        a[1] = a[-1]
        while len(a) > 2:
            a.pop()
    
    l = len(a)
    assert l <= 2, 'ERROR: l is ' + str(l) + 'which is more than 2\n'
    if l == 0:
        return
    if l == 1:
        DrawPoint(surface, a[0], color, fat)
    else:
        #print('real segment: ', a[0], a[1])
        drawSegment(surface, a[0], a[1], color, fat)

def drawPolygon(surface, dataPoints, color, fat=1, colorInner=None):
    points = []
    for i in range(0, len(dataPoints)):
        points.append(ToIntTuple(dataPoints[i]))
    if colorInner:
        pygame.draw.polygon(surface, colorInner, points, 0)
    pygame.draw.polygon(surface, color, points, fat)

