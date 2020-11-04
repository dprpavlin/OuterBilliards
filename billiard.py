import utils
from drawPoint import *
from point2D import *
from generalizedSegment import *
from segmentIntersection import *
from random import random

def intersectLines(p1, p2, p3, p4):
    return lineIntersection(p1, p2, p3, p4)

def intersectSegments(p1, p2, p3, p4):
    seg1 = GeneralizedSegment(p1, p2, False, False)
    seg2 = GeneralizedSegment(p3, p4, False, False)
    return segmentIntersection(seg1, seg2)

def isPointOnBoundOfPolygon(p, polygon):
    n = len(polygon)
    for i in range(n-1, -1, -1):
        edge = GeneralizedSegment(polygon[i], polygon[i - 1], False, False)
        if edge.isOnSegment(p):
            return True
    return False

def ByPolarAngleAroundCenterComparator(center):
    def comp(p1, p2):
        T = type(p1.GetX())

        p1 = p1 - center
        p2 = p2 - center
        pr = p1*p2
        if (pr != T(0)):
            return pr > T(0)
        else:
            return p1.len2() < p2.len2()
    return comp

#def isPointInPolygon(p, polygon):
#    raise NotImplementedException('ERROR: isPointInPolygon is not implemented')
    #if isPointOnBoundOfPolygon(p, polygon)):
    #    return True
    #T = type(p.GetX())
    #p2 = Point2D(p.GetX(), p.GetY())
def isPointInPolygon(point, polygon, T=None):
    if T is None:
        T = type(point.GetX())
    if (isPointOnBoundOfPolygon(point, polygon)):
        return True

    mindy = None
    maxx = None
    for p in polygon:
        y = utils.Abs(point.GetY() - p.GetY())
        if (mindy is None or y < mindy) and y != T(0):
            mindy = y
        x = p.GetX()
        if maxx is None or x > maxx:
           maxx = x

    if maxx < point.GetX():
        return False
    segment = GeneralizedSegment(point, Point2D(maxx + T(2), point.GetY() + mindy / T(2)), False, False)
    
    ans = 0
    for i in range(len(polygon)):
        if segmentIntersection(segment, GeneralizedSegment(polygon[i], polygon[i-1], False, False)) is not None:
            ans += 1
    return (ans % 2 == 1)

def isSegmentInPolygon(p1, p2, polygonB, T=None):
    if T is None:
        T = type(p1.GetX())

    if not (isPointInPolygon(p1, polygonB) and isPointInPolygon(p2, polygonB)):
        return False
    ps = [p1, p2]
    for i in range(len(polygonB)):
        p = intersectSegments(p1, p2, polygonB[i], polygonB[i-1])
        if not (p is None):
            ps.append(p)

    ps = utils.sort(ps, ByPolarAngleAroundCenterComparator(p1))
    ps = utils.unique(ps)
    for i in range(len(ps)):
        #print(ps[i].GetX(), ps[i].GetY(), ps[i-1].GetX(), ps[i-1].GetY())
        if not isPointInPolygon((ps[i] + ps[i-1])/T(2), polygonB):
            #print(i)
            return False
    return True


# is polygonA in polygonB 
def isPolygonInPolygon(polygonA, polygonB, T=None):
    nA = len(polygonA)
    for i in range(nA):
        if not isSegmentInPolygon(polygonA[i], polygonA[i-1], polygonB, T):
            return False
    return True


def makeReflectionPoint(p, polygon, isRight):
    T = type(p.GetX())
    numReflectPoint = 0
    variantsNumber = 1
    for i in range(1, len(polygon)):
        vectMul = (polygon[numReflectPoint] - p)*(polygon[i] - p)
        if vectMul == T(0):
            variantsNumber += 1
        elif (isRight ^ (vectMul > T(0))):
            numReflectPoint = i
            variantsNumber = 1

    if variantsNumber == 1:
        return polygon[numReflectPoint] + polygon[numReflectPoint] - p
    else:
        return None

def findPictureForIntegerPolygon(surface, polygon, isRight):
    raise NotImplementedException('ERROR: isPointInPolygon is not implemented')

if __name__ == "__main__":
    print("OK")
    
    ps = [(0, 0), (0, 2), (100, 2), (100, 0), (2, 0), (2, 1), (1, 1), (1, 0)]
    ps = [(Fraction(a), Fraction(b)) for a, b in ps]
    ps = [Point2D(a, b) for a, b in ps]

    print(ps)

    p1 = Point2D(Fraction(0), Fraction(0))
    p2 = Point2D(Fraction(3), Fraction(0))
    print(isSegmentInPolygon(p1, p2, ps)) # False
    p1 = Point2D(Fraction(0), Fraction(1)) 
    p2 = Point2D(Fraction(3), Fraction(1))
    print(isSegmentInPolygon(p1, p2, ps)) # True
    p1 = Point2D(Fraction(0), Fraction(0))
    p2 = Point2D(Fraction(3), Fraction(3))
    print(isSegmentInPolygon(p1, p2, ps)) # False
    p1 = Point2D(Fraction(0), Fraction(0))
    p2 = Point2D(Fraction(2), Fraction(2))
    print(isSegmentInPolygon(p1, p2, ps)) # True
    p1 = Point2D(Fraction(1, 2), Fraction(0))
    p2 = Point2D(Fraction(2), Fraction(2))
    print(isSegmentInPolygon(p1, p2, ps)) #False
    p1 = Point2D(Fraction(0), Fraction(0))
    p2 = Point2D(Fraction(100), Fraction(0))
    print(isSegmentInPolygon(p1, p2, ps)) # False


