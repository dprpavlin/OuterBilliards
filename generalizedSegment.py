
from point2D import Point2D
from fractions import Fraction

def Abs(x):
    T = type(x)
    return -x if x < T(0) else x

class GeneralizedSegment:
    def __init__(self, p1, p2, isNotEnd1, isNotEnd2):
        self._firstPoint = p1
        self._secondPoint = p2
        self._continuedForFirst = isNotEnd1
        self._continuedForSecond = isNotEnd2

        assert p1 != p2, 'ERROR: the attempt to create a degenerate segment...\n'

    def getFirstPoint(self):
        return self._firstPoint

    def isContinuedForFirst(self):
        return self._continuedForFirst

    def getSecondPoint(self):
        return self._secondPoint

    def isContinuedForSecond(self):
        return self._continuedForSecond

    def isOnSegment(self, p):
        T = type(self._firstPoint.GetX())
        #print('isOnSegment: test1')
        if (Abs((p - self._firstPoint) * (self._secondPoint - self._firstPoint)) > T(0)):
            return False
        #print('isOnSegment: test2')
       
        if ((not self._continuedForFirst) and (((p - self._firstPoint)^(self._secondPoint - self._firstPoint)) < T(0))):
            #print('isOnSegment fail:', ((p - self._firstPoint)^(self._secondPoint - self._firstPoint)))
            return False
        #print('isOnSegment: test3')

        if ((not self._continuedForSecond) and (((p - self._secondPoint)^(self._firstPoint - self._secondPoint)) < T(0))):
            return False
        #print('isOnSegment: OK')
      
        return True

    def isOnSegmentFloat(self, p):
        assert False, 'Not implemented yet'

    def isOnSegmentRational(self, p):
        assert False, 'Not implemented yet'

    def splitByPoint(self, delim):
        assert False, 'Not implemented yet'


if __name__ == '__main__':
    segment = GeneralizedSegment(Point2D(0, 1), Point2D(2, 1), False, True)
    print(segment.isOnSegment(Point2D(1, 1)))
    print(segment.isOnSegment(Point2D(-1, 1)))
    print(segment.isOnSegment(Point2D(3, 1)))
    print(segment.isOnSegment(Point2D(2, 1)))
    print(segment.isOnSegment(Point2D(1, 2)))

