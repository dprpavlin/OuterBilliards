import math

def sqr(x):
    return x*x

def Abs(x):
    T = type(x)
    return x if x > T(0) else -x

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Point2D(' + str(self.x) + ',' + str(self.y) + ')'
    
    def __hash__(self):
        return hash(str(self))

    def GetX(self):
        return self.x

    def GetY(self):
        return self.y

    def len(self):
        return math.sqrt(float(self.len2()))

    def len2(self):
        return sqr(self.x) + sqr(self.y)

    def lenManhatten(self):
        return Abs(self.x) + Abs(self.y)

    def maxAbsCoord(self):
        return max(self.x, self.y)

    def rotate90Left(self):
        return Point2D(-self.y, self.x)

    def rotate90Right(self):
        return Point2D(self.y, -self.x)
    
    def __add__(self, p):
        return Point2D(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point2D(self.x - p.x, self.y - p.y)

    def __mul__(self, a):
        if type(a) == type(self):
            return self.x * a.y - self.y * a.x
        return Point2D(self.x * a, self.y * a)

    def __xor__(self, p):
        return self.x * p.x + self.y * p.y

    def __add__(self, p):
        return Point2D(self.x + p.x, self.y + p.y)

    def __sub__(self, p):
        return Point2D(self.x - p.x, self.y - p.y)

    def __truediv__(self, a):
        return Point2D(self.x / a, self.y / a)

    def __eq__(self, p):
        return (self.x == p.x and self.y == p.y)

    def __ne__(self, p):
        return not (self == p)

def dist(point1, point2):
    return (point1 - point2).len()

def MultFromCenter(point, d, center):
    return center + (point - center) * d

def ByManhattenDistanceComparator(center):
    def compare(p1, p2):
        return (p1 - center).lenManhatten() < (p2 - center).lenManhatten()
    return compare

def ToIntTuple(point):
    if (type(point) == type(Point2D(2, 3))):
        return (round(point.x), round(point.y))
    else:
        return point
'''
p1 = Point2D(2, 5)
p2 = Point2D(3, -7)
p3 = Point2D(2, 5)

print(p1*p2)
print(p1 * (-2))
print(p1^p2)
print(p1 == p2)
print(p1 != p2)
print(p1 == p3)
print(p1 != p3)
'''
