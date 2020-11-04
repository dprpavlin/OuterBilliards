from point2D import *
from generalizedSegment import *
from fractions import Fraction

def Abs(x):
    T = type(x)
    return -x if x < T(0) else x

def I(x):
    return x

def areParallelLines(p1, p2, p3, p4):
    T = type(p1.GetX())
    return (p2 - p1) * (p4 - p3) == T(0)

def lineIntersectionType(p1, p2, p3, p4, needFloat=False):
    v1 = p2 - p1
    v2 = p4 - p3

    ptype = float if needFloat else I
    t = ptype((p3 - p1)*(p4-p3)) / ((p2 - p1)*(p4 - p3))
    return Point2D(ptype(p1.x) + t * ptype(v1.x),
                   ptype(p1.y) + t * ptype(v1.y))

def lineIntersectionFloat(p1, p2, p3, p4):
    return lineIntersectionType(p1, p2, p3, p4, True)

def lineIntersection(p1, p2, p3, p4):
    if (areParallelLines(p1, p2, p3, p4)):
        return None
    return lineIntersectionType(p1, p2, p3, p4, False)

def segmentIntersection(seg1, seg2):
    p1 = seg1.getFirstPoint()
    p2 = seg1.getSecondPoint()
    p3 = seg2.getFirstPoint()
    p4 = seg2.getSecondPoint()

    #print('segmentIntersection:', p1, p2, p3, p4)
    p = lineIntersection(p1, p2, p3, p4)
    #print('segmentIntersection:', p, seg1.isOnSegment(p), seg2.isOnSegment(p))
    if (not(p) or not(seg1.isOnSegment(p)) or not(seg2.isOnSegment(p))):
        return None
    return p
     

if __name__ == '__main__':
    p1 = Point2D(Fraction(0, 1), Fraction(0, 1))
    p2 = Point2D(Fraction(1, 1), Fraction(1, 1))
    p3 = Point2D(Fraction(0, 1), Fraction(1, 1))
    p4 = Point2D(Fraction(1, 1), Fraction(3, 2))


    print(segmentIntersection(GeneralizedSegment(p1, p2, False, True), GeneralizedSegment(p3, p4, False, True)))
    print(segmentIntersection(GeneralizedSegment(p1, p2, False, True), GeneralizedSegment(p3, p4, True, False)))
    print(segmentIntersection(GeneralizedSegment(p1, p2, True, False), GeneralizedSegment(p3, p4, True, False)))
    
    #f = Fraction(1, 2)
    #print(type(f))
    #print(I(f))
    #p = Point2D(1, 2)
    #print(type(p))
    #print(I(p))

    #T = type(p)
    #print(T(2, 3))
    #print(T(2, 3) == T(4, 5))
    #print(type(T(2, 3)) == type(T(4, 5)))
    #print(type(T(2, 3)) == type(T(4, 5)))
    #print(type(p) == type(f))



