import pygame, utils, sys
from pygame.locals import *
from segmentIntersection import *
from billiard import *
from absqrtn import *
from fractions import Fraction
from drawLine import *
#from intersectConvexPolygons import *

#Temporary: work with 12-gon!!!
# it is defined by the following constant
WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE = 12

#print("WORK WITH 8-GON!!! file workWith12Gon.py")
print("WORK WITH 12-GON!!! file workWith12Gon.py")
print("CHANGES ARE IN MyCipher, CheckMyCipher, MakeZoneOuterBilliardPair and getFirstComponent")
print("ALSO THERE ARE ADDITIONAL FUNCTIONS")

def Test():
    print("WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE:", WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE)

def CheckFraction(a):
    if type(a) == int:
        a = Fraction(a)
    assert type(a) == Fraction
    return a

#Depends on 8 or 12
def MyCipher(a, b=Fraction(0)): 
    a = CheckFraction(a)
    b = CheckFraction(b)
    #print(a, b)
    if WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 12:
        return Absqrt3(a, b)
    if WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 8:
        return Absqrt2(a, b)
    assert(False)

ZERO = MyCipher(Fraction(0))
COS30 = MyCipher(Fraction(0, 1), Fraction(1, 2))
SIN30 = MyCipher(Fraction(1, 2), Fraction(0, 1))

COS45 = MyCipher(Fraction(0), Fraction(1, 2))
SIN45 = COS45

#Depends on 8 or 12
def CheckMyCipher(a):
    if WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 8:
        if (type(a) != Absqrt2):
            a = MyCipher(a)
        assert type(a) == Absqrt2, "ERROR: " + str(a) + " is not Absqrt2..."
        return a

    if WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 12:
        if (type(a) != Absqrt3):
            a = MyCipher(a)
        assert type(a) == Absqrt3, "ERROR: " + str(a) + " is not Absqrt3..."
        return a

def MyPoint(x, y):
    x = CheckMyCipher(x)
    y = CheckMyCipher(y)
    return Point2D(x, y)

def getValueFromMyCipher(mc):
    return float(mc)

def DrawSegmentMyPoint(surface, p1, p2, color, fat=1):
    segment = GeneralizedSegment(p1, p2, False, False)
    drawGeneralizedSegment(surface, segment, color, fat)

def DrawRayMyPoint(surface, p1, p2, color, fat=1):
    #print(p1)
    #print(p2)
    segment = GeneralizedSegment(p1, p2, False, True)
    drawGeneralizedSegment(surface, segment, color, fat)

def DrawLineMyPoint(surface, p1, p2, color, fat=1):
    segment = GeneralizedSegment(p1, p2, True, True)
    drawGeneralizedSegment(surface, segment, color, fat)

def DrawMyPolygon(surface, polygon, color, fat=1, colorInner=None):
    drawPolygon(surface, polygon, color, fat, colorInner)

def GetCenter(polygon):
    c = MyPoint(ZERO, ZERO)
    for p in polygon:
        c = c + p
    return c * MyCipher(Fraction(1, len(polygon)))

def rotate30Counterclockwise(p):
    return MyPoint(COS30 * p.GetX() - SIN30 * p.GetY(), SIN30 * p.GetX() + COS30*p.GetY())

def rotate30Clockwise(p):
    return MyPoint(COS30 * p.GetX() + SIN30 * p.GetY(), SIN30 * (-p.GetX()) + COS30*p.GetY())

def rotate30ClockwiseAround(p, c):
    return c + rotate30Clockwise(p - c)

def rotate30CounterclockwiseAround(p, c):
    return c + rotate30Counterclockwise(p-c)

def rotate120Counterclockwise(p):
    for i in range(4):
        p = rotate30Counterclockwise(p)
    return p

def rotate120Clockwise(p):
    for i in range(4):
        p = rotate30Clockwise(p)
    return p

def rotate120ClockwiseAround(p, c):
    return c + rotate120Clockwise(p - c)

def rotate120CounterclockwiseAround(p, c):
    return c + rotate120Counterclockwise(p-c)

def rotate60Counterclockwise(p):
    for i in range(2):
        p = rotate30Counterclockwise(p)
    return p

def rotate60Clockwise(p):
    for i in range(2):
        p = rotate30Clockwise(p)
    return p

def rotate60ClockwiseAround(p, c):
    return c + rotate60Clockwise(p - c)

def rotate60CounterclockwiseAround(p, c):
    return c + rotate60Counterclockwise(p-c)

#def rotate150ClockwiseAround(p, c):
#    return c - rotate30Counterclockwise(p-c)

#def rotate150CounterclockwiseAround(p, c):
#    return c - rotate30Clockwise(p-c)



#Only for 8-gon
def rotate45Counterclockwise(p):
    return MyPoint(COS45 * p.GetX() - SIN45 * p.GetY(), SIN45 * p.GetX() + COS45*p.GetY())

#Only for 8-gon
def rotate45Clockwise(p):
    return MyPoint(COS45 * p.GetX() + SIN45 * p.GetY(), SIN45 * (-p.GetX()) + COS45*p.GetY())

#Only for 8-gon
def rotate45ClockwiseAround(p, c):
    return c + rotate45Clockwise(p - c)

#Only for 8-gon
def rotate45CounterclockwiseAround(p, c):
    return c + rotate45Counterclockwise(p-c)

#Only for 8-gon
def rotate135ClockwiseAround(p, c):
    return c - rotate45Counterclockwise(p-c)

#Only for 8-gon
def rotate135CounterclockwiseAround(p, c):
    return c - rotate45Clockwise(p-c)

#Only for 12-gon
def Get12gon(c, r):
    ans = []
    p = MyPoint(Fraction(1), Fraction(0))
    for i in range(0, 12):
        ans.append(c + r * p)
        p = rotate30Counterclockwise(p)
    return ans

#Only for 12-gon
def Get12gonFromSegment(C0, C1):
#    print(type(C0))
#    print(type(C1))

    ans = []
    V = C1 - C0
    for i in range(0, 12):
        ans.append(C0)
        C0 = C0 + V
        V = rotate30Clockwise(V)
#        print(str(i) + ' ' + str(type(C0)))

    return ans

#Only for 12-gon
def Get3gon(c, r):
    ans = []
    p = MyPoint(Fraction(1), Fraction(0))
    for i in range(0, 3):
        ans.append(c + r * p)
        p = rotate120Counterclockwise(p)
    return ans

#Only for 12-gon
def Get3gonFromSegment(C0, C1):
#    print(type(C0))
#    print(type(C1))

    ans = []
    V = C1 - C0
    for i in range(0, 3):
        ans.append(C0)
        C0 = C0 + V
        V = rotate120Clockwise(V)
#        print(str(i) + ' ' + str(type(C0)))
    return ans

#Only for 12-gon
def Get6gon(c, r):
    ans = []
    p = MyPoint(Fraction(1), Fraction(0))
    for i in range(0, 6):
        ans.append(c + r * p)
        p = rotate60Counterclockwise(p)
    return ans

#Only for 12-gon
def Get6gonFromSegment(C0, C1):
#    print(type(C0))
#    print(type(C1))

    ans = []
    V = C1 - C0
    for i in range(0, 6):
        ans.append(C0)
        C0 = C0 + V
        V = rotate60Clockwise(V)
#        print(str(i) + ' ' + str(type(C0)))
    return ans

#For any gon
def Get4gon(c, r):
    ans = []
    p = MyPoint(Fraction(1), Fraction(0))
    for i in range(0, 4):
        ans.append(c + r * p)
        p = p.rotate90Right()
    return ans

#for any gon
def Get4gonFromSegment(C0, C1):
#    print(type(C0))
#    print(type(C1))

    ans = []
    V = C1 - C0
    for i in range(0, 4):
        ans.append(C0)
        C0 = C0 + V
        V = V.rotate90Right()
#        print(str(i) + ' ' + str(type(C0)))
    return ans

#Only for 8-gon
def Get8gon(c, r):
    ans = []
    p = MyPoint(Fraction(1), Fraction(0))
    for i in range(0, 8):
        ans.append(c + r * p)
        p = rotate45Counterclockwise(p)
    return ans

#Only for 8-gon
def Get8gonFromSegment(C0, C1):
#    print(type(C0))
#    print(type(C1))

    ans = []
    V = C1 - C0
    for i in range(0, 8):
        ans.append(C0)
        C0 = C0 + V
        V = rotate45Clockwise(V)
        print(str(i) + ' ' + str(type(C0)))
    return ans

def isInAngle(p, A, B, C):
    if ((B-A)*(C-A) < MyCipher(Fraction(0))):
        T = B
        B = C
        C = T
    if (((C - A)*(p - A)) > MyCipher(Fraction(0))):
        return False
    if (((B - A)*(p - A)) < MyCipher(Fraction(0))):
        return False
    return True

def isOnLine(p, A, B):
    assert not(A == B)
    return (p - A)*(B - A) == ZERO


def isOnRay(p, O, A):
    return isOnLine(p, O, A) and ((p - O)^(A - O) >= ZERO)


def isOnSegment(p, A, B): 
    return isOnRay(p, A, B) and isOnRay(p, B, A)


def isInConvexPolygon(p, polygon):
    n = len(polygon)
    for i in range(0, n):
        if (not isInAngle(p, polygon[i], polygon[(i-1) if i > 0 else (n-1)], polygon[i+1 if (i+1<n) else 0])):
            return False
    return True


def isInTriangle(p, a, b, c):
    polygon = []
    polygon.append(a)
    polygon.append(b)
    polygon.append(c)
    return isInConvexPolygon(p, polygon)


def isInStarPolygon(p, polygon):
    if type(p) == list:
        for point in p:
            if not isInStarPolygon(point, polygon):
                return False
        return True
        assert False, 'ERROR: isInStarPolygon for two polygons is not implemented yet'

    n = len(polygon)
    if (not isInAngle(p, polygon[0], polygon[1], polygon[n-1])):
        return False
    for i in range(1, n):
        if (isInTriangle(p, polygon[0], polygon[i], polygon[i+1 if (i+1<n) else 0])):
            return True
    return False

def isInZone(pol, zones):
    for i in range(0, len(zones)):
        if (isInStarPolygon(pol, zones[i])):
            return True
    return False

def reflect(p, c):
    if type(c) == Point2D:
        return c + c - p

   # num = 0
   # for i in range(0, len(pol)):
   #     if ((pol[num] - p)*(pol[i] - p) > MyCipher(Fraction(0))):
   #         num = i
   # return pol[num]*MyCipher(Fraction(2)) - p

def isInFirstAngle(p, polygon):
    p00 = reflect(polygon[0], polygon[1])
    return isInAngle(p, polygon[1], polygon[2], p00)

#Depends on 12 or 8
def MakeZoneOuterBilliardPair(p, polygon, isInverse=False):
    assert not isInConvexPolygon(p, polygon)
    np = makeReflectionPoint(p, polygon, isInverse)
    if (not np):
        return (None, -1)
    p = np
    O = GetCenter(polygon)
    kol = len(polygon)
    while (not isInFirstAngle(p, polygon)):
        if WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 12:
            p = rotate30ClockwiseAround(p, O)
        elif WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 8:
            p = rotate45ClockwiseAround(p, O)
        kol -= 1
        assert(kol)
    
    return (p, kol)

def MakeZoneOuterBilliardPoint(p, polygon, isInverse = False): 
    return MakeZoneOuterBilliardPair(p, polygon, isInverse)[0]


def compressVector(a, b, scale):
    return a + (b - a) * scale


def compressPolygon(polygon, scale, center=None):
    polygon = polygon.copy()
    if center is None:
        center = GetCenter(polygon)
    for i in range(0, len(polygon)):
        polygon[i] = compressVector(center, polygon[i], scale)
    return polygon

def MakeReflectionOuterBilliard(zone, polygon, needCompress = False):
    zone = zone.copy()

    if (needCompress):
        zone = compressPolygon(zone, MyCipher(Fraction(1, 2)))

    for i in range(0, len(zone)):
        zone[i] = makeReflectionPoint(zone[i], polygon, False)
    
    if (needCompress):
        zone = compressPolygon(zone, MyCipher(Fraction(2, 1)))

    return zone

def GetPeriod(point, polygon, bound = 1000000000):
    p = point
    for i in range(bound):
        p = makeReflectionPoint(p, polygon, False)
        if p == point:
            return i+1
    assert(False, "ERROR: period is more than bound!!!")

def MakeZoneOuterBilliard(zone, polygon, needCompress = False, isInverse = False): 
    #print('workWith12Gon.py: zone = ', zone)
    zone = zone.copy()

    if (needCompress):
        zone = compressPolygon(zone, MyCipher(Fraction(1, 2)))
    #print('workWith12Gon.py: zone = ', zone)
    
    for i in range(0, len(zone)):
        zone[i] = MakeZoneOuterBilliardPoint(zone[i], polygon, isInverse)

    if (needCompress):
        zone = compressPolygon(zone, MyCipher(Fraction(2, 1)))
    
    return zone


def isInFirstComponent(p, polygon, zones):
    assert len(zones) == 5
    for i in range(0, len(zones)):
        if (isInStarPolygon(p, zones[i])):
            return True
    return False



def intersectConvexPolygons(polygon1, polygon2):
    ps = []
    for i in range(0, len(polygon1)):
        ps.append(polygon1[i])
    for i in range(0, len(polygon2)):
        ps.append(polygon2[i])
    
    for i in range(len(polygon1)):
        seg1 = GeneralizedSegment(polygon1[i], polygon1[(i+1) if i + 1 < len(polygon1) else 0], False, False)
        for j in range(0, len(polygon2)):
            seg2 = GeneralizedSegment(polygon2[j], polygon2[j+1 if j + 1 < len(polygon2) else 0], False, False)
            uk = segmentIntersection(seg1, seg2)
            if (uk): 
                ps.append(uk)

    ans = []
    for i in range(0, len(ps)):
        if (isInConvexPolygon(ps[i], polygon1) and isInConvexPolygon(ps[i], polygon2)):
    
            ans.append(ps[i])

    pans = [ans[0]]
    pans.extend(utils.sort(ans[1:], ByPolarAngleAroundCenterComparator(ans[0])))
    ans = utils.unique(pans)
    return ans

def getZonesFrom12Gon(polygon):
    assert(len(polygon) == 12)
    zones = []
    for i in range(1, 5):
        pol = []
        pol.append(intersectLines(polygon[0], polygon[1], polygon[i], polygon[i+1]))
        pol.append(intersectLines(polygon[0], polygon[1], polygon[i+1], polygon[i+2]))
        pol.append(intersectLines(polygon[1], polygon[2], polygon[i+1], polygon[i+2]))
        if (i > 1):
            pol.append(intersectLines(polygon[1], polygon[2], polygon[i], polygon[i+1]))
        zones.append(pol)
    
    center = (polygon[0] + polygon[6]) / MyCipher(2)
    ukp = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
    newc = reflect(center, ukp)

    zone = [ukp]

    for i in range(8, 12):
        zone.append(polygon[i] + newc - center)
    zones.append(zone)
    return zones

def getZonesFrom12GonBig(polygon):
    assert(len(polygon) == 12)
    zones = []
    for i in range(1, 5):
        pol = []
        pol.append(intersectLines(polygon[0], polygon[1], polygon[i], polygon[i+1]))
        pol.append(intersectLines(polygon[0], polygon[1], polygon[i+1], polygon[i+2]))
        pol.append(intersectLines(polygon[1], polygon[2], polygon[i+1], polygon[i+2]))
        if (i > 1):
            pol.append(intersectLines(polygon[1], polygon[2], polygon[i], polygon[i+1]))
        zones.append(pol)
   

    beta = getBeta(polygon)

    center = (polygon[0] + polygon[6]) / MyCipher(2)
    
    u0 = beta[0]
    v0 = u0 + (polygon[1] - polygon[0]) * MyCipher(100 + len(polygon))
    u1 = beta[7]
    v1 = u1 + v0 - u0
    v2 = lineIntersection(v0, v1, polygon[1], polygon[2])
    
    zones.append([v0, u0, intersectLines(polygon[1], polygon[2], polygon[6], polygon[5]), u1, v1])
    zones.append([v1, u1, v2])
    return zones

#Only for 8-gon
def getZonesFrom8Gon(polygon):
    assert(len(polygon) == 8)
    zones = []
    for i in range(1, 3):
        pol = []
        pol.append(intersectLines(polygon[0], polygon[1], polygon[i], polygon[i+1]))
        pol.append(intersectLines(polygon[0], polygon[1], polygon[i+1], polygon[i+2]))
        pol.append(intersectLines(polygon[1], polygon[2], polygon[i+1], polygon[i+2]))
        if (i > 1):
            pol.append(intersectLines(polygon[1], polygon[2], polygon[i], polygon[i+1]))
        zones.append(pol)
    
    center = (polygon[0] + polygon[4]) / MyCipher(2)
    ukp = lineIntersection(polygon[1], polygon[2], polygon[4], polygon[3])
    newc = reflect(center, ukp)

    zone = [ukp]

    for i in range(6, 8):
        zone.append(polygon[i] + newc - center)
    zones.append(zone)
    return zones

def getZonesFrom8GonBig(polygon):
    assert(len(polygon) == 8)
    zones = []
    for i in range(1, 3):
        pol = []
        pol.append(intersectLines(polygon[0], polygon[1], polygon[i], polygon[i+1]))
        pol.append(intersectLines(polygon[0], polygon[1], polygon[i+1], polygon[i+2]))
        pol.append(intersectLines(polygon[1], polygon[2], polygon[i+1], polygon[i+2]))
        if (i > 1):
            pol.append(intersectLines(polygon[1], polygon[2], polygon[i], polygon[i+1]))
        zones.append(pol)
   
    pinf = polygon[0] + (polygon[1] - polygon[0]) * MyCipher(20)
    pinf2 = intersectLines(pinf, pinf + polygon[3] - polygon[2], polygon[5], polygon[4])
    pinf3 = intersectLines(pinf, pinf2, polygon[1], polygon[2])
    
    zone = [pinf,
            intersectLines(polygon[0], polygon[1], polygon[3], polygon[4]),
            intersectLines(polygon[1], polygon[2], polygon[3], polygon[4]),
            intersectLines(polygon[1], polygon[2], polygon[4], polygon[5]),
            pinf2
           ]
    zones.append(zone)

    zone = [pinf2,
            intersectLines(polygon[1], polygon[2], polygon[4], polygon[5]),
            pinf3
           ]
    zones.append(zone)
    return zones

#Depends on 12 or 8
def getBeta(polygon):
    assert(len(polygon) == WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE)

    if WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 12:
        p = intersectLines(polygon[0], polygon[1], polygon[6], polygon[5])
        return  Get12gonFromSegment(p, p + polygon[1] - polygon[0])

    if WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 8:
        p = intersectLines(polygon[0], polygon[1], polygon[4], polygon[3])
        return  Get8gonFromSegment(p, p + polygon[1] - polygon[0])

#Depends on 12 or 8
def getFirstComponent(polygon):
    if WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 8:
        center = (polygon[0] + polygon[4]) / MyCipher(2)
        ukp = lineIntersection(polygon[1], polygon[2], polygon[4], polygon[3])
        newc = reflect(center, ukp)

        ans = [polygon[1]]
        ans.append(polygon[0] + newc - center)
        for i in range(7, 5, -1):
            ans.append(polygon[i] + newc - center)

        return ans
    
    if WORK_WITH_RIGHT_REGULAR_POLYGONS_MODE == 12:
        center = (polygon[0] + polygon[6]) / MyCipher(2)
        ukp = lineIntersection(polygon[1], polygon[2], polygon[6], polygon[5])
        newc = reflect(center, ukp)

        ans = [polygon[1]]
        ans.append(polygon[0] + newc - center)
        for i in range(11, 7, -1):
            ans.append(polygon[i] + newc - center)

        return ans
    assert(False)

def isInFirstComponent(p, polygon):
    if (not isInFirstAngle(p, polygon)):
        return False
    return isInStarPolygon(p, getFirstComponent(polygon))

def arePolygonsEq(pol1, pol2):
    if len(pol1) != len(pol2):
        return False

    num = None
    for i in range(0, len(pol2)):
        if pol1[0] == pol2[i]:
            num = i
    if num is None:
        return False
    
    ok = True
    for i in range(0, len(pol1)):
        ok &= (pol1[i] == pol2[num - i])
    if ok:
        return True
    ok = True
    num -= len(pol1)
    for i in range(0, len(pol1)):
        ok &= (pol1[i] == pol2[num + i])
    return ok

def arePolygonsEqual(pol1, pol2):
    return arePolygonsEq(pol1, pol2)

def getFirstReturnMap(p, zoneReturnMap, polygon, orbit, maxKol = 100): 
    raise NotImplementedException()

def getStableZonesFrom12Gon(polygon, zones) :
    ansZones = []
    for numZone in range(0, 4):
        zone = zones[numZone]
        for i in range(0, 100):
            #print('WorkWith12Gon.py: iteration ', i, file=sys.stderr)
            #if i > 2:
            #    sys.exit(0)
            #print('WorkWith12Gon.py: getStableZonesFrom12Gon: zone = ', zone)
            zoneOuter = MakeZoneOuterBilliard(zone, polygon, True)
            #print('WorkWith12Gon.py: getStableZonesFrom12Gon: zoneOuter = ', zoneOuter)
            newZone = intersectConvexPolygons(zoneOuter, zones[numZone])
            if (arePolygonsEq(zone, newZone)):
                break
            zone = newZone
        
        #zones[numZone] = zone
        ansZones.append(zone)
    
    return ansZones

def getStableZonesFrom8Gon(polygon, zones) :
    ansZones = []
    for numZone in range(0, 2):
        zone = zones[numZone]
        for i in range(0, 100):
            #print('WorkWith12Gon.py: iteration ', i, file=sys.stderr)
            #if i > 2:
            #    sys.exit(0)
            #print('WorkWith12Gon.py: getStableZonesFrom12Gon: zone = ', zone)
            zoneOuter = MakeZoneOuterBilliard(zone, polygon, True)
            #print('WorkWith12Gon.py: getStableZonesFrom12Gon: zoneOuter = ', zoneOuter)
            newZone = intersectConvexPolygons(zoneOuter, zones[numZone])
            if (arePolygonsEq(zone, newZone)):
                break
            zone = newZone
        
        #zones[numZone] = zone
        ansZones.append(zone)
    
    return ansZones

def getZeroRankPolygonsFrom8Gon(polygon, zones, stableZones):
    beta1 = stableZones[0].copy()
    beta2 = stableZones[1].copy()
    o2 = GetCenter(beta2)
    beta32 = [rotate135CounterclockwiseAround(p, o2) for p in beta1]
    beta23 = [rotate135ClockwiseAround(p, o2) for p in beta1]
    return (beta1, beta2, beta32, beta23)

def deleteThreePointsOnOneLine(polygon) :
    polygon = utils.unique(polygon)
    while (len(polygon) >= 2 and polygon[-1] == polygon[0]):
        polygon.pop()
    if (len(polygon) <= 2) :
        return []
    
    ans = []
    for i in range(0, len(polygon)) :
        pi = ((i-1) if i > 0 else len(polygon) - 1)
        ni = (i + 1 if (i + 1 < len(polygon)) else 0)
        if (not isOnSegment(polygon[i], polygon[pi], polygon[ni])):
            ans.append(polygon[i]) 
    
    if (len(ans) <= 2):
        return []
    return ans

def PaintStarPolygonInner(screen, polygon, color, fat=1):
    raise NotImplementedException('use something from pygame.draw.polygon...')



def checkIsNotThreeOnOneLine(polygon) :
    #print(polygon)
    for i in range(0, len(polygon)):
        for j in range(i+1,  len(polygon)) :
            assert polygon[i] != polygon[j]
            for k in range(0, len(polygon)):
                assert i == k or j == k or not(isOnSegment(polygon[k], polygon[i], polygon[j])), str((i, j, k))
        


def splitGoodPolygonByZonesOldVersion(goodPolygon, polygon, zones) :
    assert(len(polygon) == 12 and len(zones) == 5)
    newPolygon = []
    rays = []

    for i in range(3, 7):
        rays.append(GeneralizedSegment(polygon[i], polygon[i-1], False, True))
    #print('LEN: ', len(goodPolygon))
    for i in range(0, len(goodPolygon)) :
        p = goodPolygon[i]
        np = goodPolygon[i+1 if (i + 1 < len(goodPolygon)) else 0]
        seg = GeneralizedSegment(p, np, False, False)
        ps = [p]
        for j in range(0, len(rays)) :
            inter = segmentIntersection(seg, rays[j])
            if (inter is None):
                continue
            ps.append(inter)
        
        ps = utils.sort(ps, ByManhattenDistanceComparator(p))
        #print('PS: ', ps)
        newPolygon.extend(ps)
   
    anss = []
    for i in range(0, 5):
        anss.append([])
    for i in range(0, len(newPolygon)):
        for j in range(0, 5):
            if (isInStarPolygon(newPolygon[i], zones[j])):
                anss[j].append(newPolygon[i])
    anssp = []
    
    for i in range(0, 5) :
        #print('WorkWith12Gon: splitGoodPolygonsByZones:', i)
        #for j in range(len(anss[i])):
        #    print(j, anss[i][j])
        anss[i] = deleteThreePointsOnOneLine(anss[i])
        #print('WorkWith12Gon: splitGoodPolygonsByZones after:', i)
        #for j in range(len(anss[i])):
        #    print(j, anss[i][j])
        checkIsNotThreeOnOneLine(anss[i])
        if (len(anss[i]) >= 3):
            anssp.append((anss[i], i))
    
    return anssp

def lineSign(point, line):
    p1 = line.getFirstPoint()
    p2 = line.getSecondPoint()
    return utils.sign((p2 - p1) * (point - p1))

def arePointsInPolygon(points, polygon, T=None):
#    print('arePointsInPolygon: points: ', points)
#    print('arePointsInPolygon: polygon: ', polygon)

    lst = [isPointInPolygon(point, polygon, T) for point in points]
    return lst.count(False) == 0

def getIsFirstHalf(vector1, vector2):
    T = type(vector1.GetX())
    zero = T(0)
    assert vector1.len2() > zero
    mul = vector1*vector2
    if mul != T(0):
        return mul > zero
    else:
        return (vector1^vector2) >= zero

def ByDirectionPolAngleComparator(d1, d2):
    assert d1 != d2
    direct = d2 - d1
    T = type(d1.GetX())
    zero = T(0)
    def compare(p1, p2):
        p1 = p1 - d1
        p2 = p2 - d1
        half1 = getIsFirstHalf(direct, p1)
        half2 = getIsFirstHalf(direct, p2)
        if half1 != half2:
            return half1
        
        mul = p1*p2
        if mul != zero:
            return mul > zero
        else:
            return p1.len2() < p2.len2()
    
    return compare

def getDoubledOrientedSquare(polygon):
    T = type(polygon[0].GetX())
    square = T(0)
    for i in range(len(polygon)):
        square += (polygon[i-1].GetX() - polygon[i].GetX()) * (polygon[i-1].GetY() + polygon[i].GetY())
    return square

def getDoubledOrientedArea(polygon):
    return getDoubledOrientedSquare(polygon)

#returns tuple with two lists of polygons (left and right)
def splitPolygonByLine(polygon, line, verbose=False):
    polygon = polygon.copy()
    T = type(polygon[0].GetX())
    square = getDoubledOrientedSquare(polygon)
    if verbose:
        print('SQUARE: ', square)
    if square < T(0):
        if verbose:
            print('REVERSE')
        polygon.reverse()

    signs = [lineSign(point, line) for point in polygon]
    numSigns = [signs.count(0), signs.count(1), signs.count(-1)]
    if numSigns[-1] == 0:
        return ([], [polygon])
    if numSigns[1] == 0:
        return ([polygon], [])

    newPolygon = []
    for i in range(len(polygon)):
        if signs[i] * signs[i-1] == -1:
             newPolygon.append(segmentIntersection(line, GeneralizedSegment(polygon[i], polygon[i-1], False, False)))
        newPolygon.append(polygon[i])

    polygon = newPolygon
    signs = [lineSign(point, line) for point in polygon]
    n = len(polygon)
    graph = []
    for i in range(n):
        graph.append([])
        if i: 
            graph[i-1].append(i)
    graph[n-1].append(0)

    def segmentIntersectionCoordinateComparator(line):
        def coordinate(point):
            return (line.getSecondPoint() - line.getFirstPoint()) ^ (point - line.getFirstPoint())
        def less(num1, num2):
            return coordinate(polygon[num1]) < coordinate(polygon[num2])
        return less
    if verbose:
        print ('SIGNS AFTER:', signs)
    pointsOnLine = [i for i in range(n) if signs[i] == 0]
    pointsOnLine = utils.sort(pointsOnLine, less=segmentIntersectionCoordinateComparator(line))
    for i in range(1, len(pointsOnLine)):
        graph[pointsOnLine[i]].append(pointsOnLine[i-1])
        graph[pointsOnLine[i-1]].append(pointsOnLine[i])

    if verbose:
        for i in range(n):
            for j in range(len(graph[i])):
                print('EDGE: ', i, graph[i][j])

    used = [0] * n
    ans = ([], [])
    for vertex in range(n):
        if signs[vertex] != 0 and used[vertex] == 0:
           assert len(graph[vertex]) == 1
           if verbose:
               print('VERTEX: ', vertex)
           currentVertex = graph[vertex][0]
           previousVertex = vertex
           newPolygon = [polygon[currentVertex]]
           used[currentVertex] = 1
           while currentVertex != vertex:
               if len(graph[currentVertex]) == 1:
                   nextVertex = graph[currentVertex][0]
               else:
                   less = ByDirectionPolAngleComparator(polygon[currentVertex], polygon[previousVertex]) 
                   nextVertex = None
                   for v in graph[currentVertex]:
                       if v != previousVertex:
                           if nextVertex == None or less(polygon[nextVertex], polygon[v]):
                               nextVertex = v
               used[nextVertex] = 1
               #sys.stdout.write(str(nextVertex))
               #sys.stdout.write(' ')
               newPolygon.append(polygon[nextVertex])
               previousVertex = currentVertex
               currentVertex = nextVertex
           #sys.stdout.write('\n')
           newPolygon = deleteThreePointsOnOneLine(newPolygon)
           if signs[vertex] < 0:
               ans[0].append(newPolygon)
           else:
               ans[1].append(newPolygon)
    return ans


def splitGoodPolygonByZones(goodPolygon, polygon, zones):
    assert(len(polygon) == 12 and len(zones) == 5)
    newPolygon = []
    rays = []
   
    polygons = [goodPolygon.copy()]
    resultPolygons = []

    for i in range(3, 7):
        ray = GeneralizedSegment(polygon[i], polygon[i-1], False, True)
        for p in polygons:
            splitted = splitPolygonByLine(p, ray)
            polygons = splitted[0]
            for pol in splitted[1]:
                resultPolygons.append((pol, i-3))
            #resultPolygons.extend(splitted[1])

    for pol in polygons:
        resultPolygons.append((pol, 4))
    #resultPolygons.extend(polygons)
    return resultPolygons
    
def splitGoodPolygonByZonesOnlyPolygons(goodPolygon, polygon, zones):
    ans = splitGoodPolygonByZones(goodPolygon, polygon, zones)
    ans = [a[0] for a in ans]
    return ans

#typedef std::vector<std::pair<MyPolygon, long long> > HashedPolygons

#returns list from (polygon, int)-tuples
#works only in assumption that at any moment of time, all current figures are completely in one of startPolygons or completely not on startPolygons
def tryMakeFirstReturnMap(startPolygons, goodPolygon, polygon, zones, maxKol = 100) :
    startPolygons = utils.copy2dList(startPolygons)

    #print(startPolygons)
    #print(goodPolygon)
    #print(polygon)
    pols = []
    ans = []
    npols = []
    
    for i in range(len(startPolygons)):
        pols.append((startPolygons[i], 0))

    iter = 0
    if maxKol <= 0:
        maxKol = 1

    while (iter < maxKol and not(len(pols) == 0)):
        npols = []
        iter += 1
        print('tryMakeFirstReturnMap: iteration', iter, file=sys.stderr)
        for i in range(0, len(pols)):
            curh = pols[i][1]
            if (iter > 1):
                if (isInStarPolygon(pols[i][0], goodPolygon)) :
                    ans.append((pols[i][0], curh))
                    continue

            newPols = splitGoodPolygonByZones(pols[i][0], polygon, zones)
            #print(newPols) 
            for j in range(len(newPols)):
                if (iter > 1):
                    if (isInStarPolygon(newPols[j][0], goodPolygon)) :
                        ans.append((newPols[j][0], curh))
                        continue
                    
                newh = curh * 10007 + newPols[j][1]
                newh %= (2 ** 64)
                newPolygon = MakeZoneOuterBilliard(newPols[j][0], polygon, True, False)
                if (isInStarPolygon(newPolygon, goodPolygon)):
                    ans.append((newPolygon, newh))
                else:
                    npols.append((newPolygon, newh))
            
        
        pols = npols
        #npols.swap(pols)
    
    return (ans, pols)

def tryMakeFirstReturnMapOnlyPolygons(startPolygons, goodPolygon, polygon, zones, maxKol = 100) :
    ans = tryMakeFirstReturnMap(startPolygons, goodPolygon, polygon, zones, maxKol)
    print(ans)
    #assert(len(ans[1]) == 0)
    print("LEN: ", len(ans[1]), "should be 0")
    ans = ans[0]
    for i in range(len(ans)):
        ans[i] = ans[i][0]
    return ans

#returns (polygon, num)-tuple
def reverseAndTestZone(pol, goodPolygon, polygon, zones):
    #assert isInZone(pol, zones) and isInStarPolygon(pol, goodPolygon)
    assert isInStarPolygon(pol, goodPolygon)
    ans = 0
    while True:
        ans += 1
        pol = MakeZoneOuterBilliard(pol, polygon, True, True)
        assert(isInZone(pol, zones))
        if isInStarPolygon(pol, goodPolygon):
            break
    return (pol, ans)

#returns [(polygon,num)-tuples]
def reverseAndTestZones(pols, goodPolygon, polygon, zones):
    ans = []
    for i in range(len(pols)):
        ans.append(reverseAndTestZone(pols[i], goodPolygon, polygon, zones))
        sys.stderr.write(str(i) + 'th polygon (size ' + str(len(ans[-1][0])) + ') \'reversed\' with ' + str(ans[-1][1]) + ' iterations\n')
        sys.stdout.write(str(i) + 'th polygon (size ' + str(len(ans[-1][0])) + ') \'reversed\' with ' + str(ans[-1][1]) + ' iterations\n')
    return ans

def reverseAndTestZonesOnlyPolygons(pols, goodPolygon, polygon, zones):
    ans = reverseAndTestZones(pols, goodPolygon, polygon, zones)
    ans = [a[0] for a in ans]
    return ans

#std::pair<HashedPolygons, HashedPolygons> tryMakeFirstReturnMap(const MyPolygon &goodPolygon,
#                                                                    const MyPolygon &polygon,
#                                                                    const std::vector<MyPolygon> &zones,
 #                                                                   int maxKol = 100) :
 #   return tryMakeFirstReturnMap(std::vector<MyPolygon>(1, goodPolygon), goodPolygon, polygon, zones, maxKol)
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

def findHashForPolygon(polygon):
    num = findMinyMinxIndexInPolygon(polygon)
    n = len(polygon)
    #print('HI', n)
    s = ''
    for i in range(n):
        s = s + str(polygon[num+i-n]) + ';'
    sRev = ''
    for i in range(n):
        sRev = sRev + str(polygon[num-i]) + ';'
    if (s < sRev):
        return s
    else:
        return sRev

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
        if number % 10 == 0:
            print("findComponentOfPoint: iteration", number)
            #print('findComponentOfPointWithPeriod: area is ', getDoubledOrientedArea(currentPolygon), ', number is ', iterations)
        #if iterations == 50:
        #    fsdfdsf
    print('findComponentOfPoint iterations are finished')
    while not(isPointInPolygon(startPoint, ans[0])):
        ans = (MakeZoneOuterBilliard(ans[0], polygon, True), ans[1])
    print('findComponentOfPoint finished')
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

# разобраться, прежде чем использовать - что-то тут не то
def fromSystemToSystem(point, ls1, ls2):
    return ls2.getPoint(ls1.getCoefs(point))

def isPolygonInOneOfForbiddenPolygons(polygon, forbiddenPolygons):
    #print("POLYGON:", polygon)
    #print("FORBIDDEN POLYGONS:", forbiddenPolygons)
    #print("FORBIDDEN POLYGONS:", len(forbiddenPolygons))
    for fp in forbiddenPolygons:
        if (isPolygonInPolygon(polygon, fp)):
            return True
    return False

#returns list of (polygon, int)- tuples - periodic figures and periods
def findPeriodicComponents(startPolygon, forbiddenPolygons, polygon, zones, iterations = 100, screen = None):
    ans = []
   
    polygonsDict = {}
    sz = 0
    #polygonsList = []

    currentPolygons = [startPolygon]
    for i in range(iterations):
        print("iteration", i, ", ", len(currentPolygons), " in a game")
        newPolygons = []
        #for cp in currentPolygons:
        index = 0
        while (index < len(currentPolygons)):
            cp = currentPolygons[index]
            index += 1

            #print("PREVED")
            ncp = cp.copy()
            if (isPolygonInOneOfForbiddenPolygons(ncp, forbiddenPolygons)):
                if not(screen is None):
                    DrawMyPolygon(screen, ncp, (128, 128, 0), 0)
                continue
            
            h = findHashForPolygon(ncp)
            if polygonsDict.get(h) is not None:
                continue
            polygonsDict[h] = sz
            sz += 1

            period = 0
            while True:
                period += 1
                nps = splitGoodPolygonByZonesOnlyPolygons(ncp, polygon, zones)
                #print(nps)
                if (len(nps) == 1):
                    #print(ncp)
                    nncp = MakeZoneOuterBilliard(nps[0], polygon, True)
                    #print(ncp)
                    if (arePolygonsEqual(nncp, cp)):
                        ans.append((nncp, period))
                        break
                    #print(ncp)
                    if (isPolygonInOneOfForbiddenPolygons(nncp, forbiddenPolygons)):
                        #print("OUT")
                        if not(screen is None):
                            print("GO")
                            #print(ncp)
                            numIter = 0
                            ncp = cp.copy()
                            while (not(isPolygonInOneOfForbiddenPolygons(ncp, forbiddenPolygons))):
                                DrawMyPolygon(screen, ncp, (128, 128, 0), 0)
                                ncp = MakeZoneOuterBilliard(ncp, polygon, True, False)
                                numIter += 1
                                print("GO ITER", numIter)
                                #if (numIter == 20000):
                                #    break
                                #print(ncp)
                        break
                    ncp = nncp
                    h = findHashForPolygon(ncp)
                    if polygonsDict.get(h) is not None:
                        print("OUT 2")
                        break
                    polygonsDict[h] = sz
                    sz += 1
                else:
                    newPolygons.extend(nps)
                    break
        currentPolygons = newPolygons
    
    print(len(ans), " periodic components, ", len(currentPolygons), " are alive now")
    return (ans, currentPolygons)


#emulate induced T for given periodic point for all occurrences of point in polygonFRM,
#stores numbers of zones in zonesFRM in which the occurrences lie;
#polygonBase is 12-gonal or 8-gonal (or else) table 
def findPeriodicTrajectoryForReturnMap(point, polygonFRM, zonesFRM, polygonBase):
    ans = []
    startPoint = point
    while True:
        if isPointInPolygon(point, polygonFRM):
            for i in range(len(zonesFRM)):
                if isPointInPolygon(point, zonesFRM[i]):
                    ans.append(i)
                    break
        point = MakeZoneOuterBilliardPoint(point, polygonBase)
        if (point == startPoint):
            break
    return ans

def findAggregatedInfoAboutPeriodicTrajectoryForReturnMap(point, polygonFRM, zonesFRM, polygonBase):
    ans2 = findPeriodicTrajectoryForReturnMap(point, polygonFRM, zonesFRM, polygonBase)
    ans = [ans2.count(i) for i in range(len(zonesFRM))]
    return ans
 
#emulate induced T for given point for all occurrences of point during returning to polygonFRM,
#stores numbers of zones in zonesCode in which the occurrences lie;
#polygonBase is 12-gonal or 8-gonal (or else) table 
def findReturningTrajectoryForReturnMap(point, polygonFRM, polygonCode, zonesCode, polygonBase):
    ans = []
    startPoint = point
    while True:
        if isPointInPolygon(point, polygonCode):
            for i in range(len(zonesCode)):
                if isPointInPolygon(point, zonesCode[i]):
                    ans.append(i)
                    break
        point = MakeZoneOuterBilliardPoint(point, polygonBase)
        if (isPointInPolygon(point, polygonFRM)):
            break
    return ans

def findAggregatedInfoAboutReturningTrajectoryForReturnMap(point, polygonFRM, polygonCode, zonesCode, polygonBase):
    ans2 = findReturningTrajectoryForReturnMap(point, polygonFRM, polygonCode, zonesCode, polygonBase)
    ans = [ans2.count(i) for i in range(len(zonesCode))]
    return ans

if __name__ == '__main__':
    pol = [MyPoint(0, 0), MyPoint(0, 3), MyPoint(1, 2), MyPoint(3, 3), MyPoint(4, -1), MyPoint(3, -1), MyPoint(3, 0), MyPoint(2, 1)]
    line = GeneralizedSegment(MyPoint(0, 3), MyPoint(3, 0), True, True)
    pols = splitPolygonByLine(pol, line)
    print("EE")
    for p in pols[0][0]:
        print(p)
    for p in pols[0][1]:
        print(p)
    print("EE")
    for p in pols[1][0]:
        print(p)


