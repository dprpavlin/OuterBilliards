from workWith12Gon import *
from point2D import *
from segmentIntersection import *
from billiard import *
from absqrtn import *
from fractions import *

import pygame, sys, utils
from pygame.locals import *
from billiard import *

def makeColorFromHash(h):
    r = h % 256
    h /= 256
    g = h % 256
    h /= 256
    b = h % 256
    return (r, g, b)


def lineSign(point, line):
    p1 = line.getFirstPoint()
    p2 = line.getSecondPoint()
    return utils.sign((p2 - p1) * (point - p1))

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
#return list of (polygon, point, answer)-tuples

def testingIsPointInPolygon():
    polygon = [MyPoint(0, 0), MyPoint(0, 4), MyPoint(2, 4), MyPoint(4, 2), MyPoint(2, 0)]
    assert isPointInPolygon(MyPoint(3, 2), polygon) == True
    assert isPointInPolygon(MyPoint(3, 3), polygon) == True
    assert isPointInPolygon(MyPoint(3, 4), polygon) == False
    assert isPointInPolygon(MyPoint(-1, 1), polygon) == False
    assert isPointInPolygon(MyPoint(-1, 3), polygon) == False
    assert isPointInPolygon(MyPoint(1, 1), polygon) == True
    assert isPointInPolygon(MyPoint(1, 3), polygon) == True
    assert isPointInPolygon(MyPoint(4, 3), polygon) == False
    assert isPointInPolygon(MyPoint(4, 2), polygon) == True
    print('Test 1: OK')

    polygon = [MyPoint(2, 3), MyPoint(1, 12), MyPoint(3, 13), MyPoint(2, 6), MyPoint(6, 10),
               MyPoint(7, 7), MyPoint(6, 15), MyPoint(11, 14), MyPoint(12, 11), MyPoint(8, 10),
               MyPoint(9, 8), MyPoint(12, 7), MyPoint(13, 9), MyPoint(16, 10), MyPoint(15, 2),
               MyPoint(8, 2), MyPoint(8, 5), MyPoint(13, 5), MyPoint(13, 4), MyPoint(9, 4),
               MyPoint(9, 3), MyPoint(14, 3), MyPoint(14, 6), MyPoint(5, 5), MyPoint(3, 2)]
    
    assert isPointInPolygon(MyPoint(3, 2), polygon) == True
    assert isPointInPolygon(MyPoint(2, 2), polygon) == False
    assert isPointInPolygon(MyPoint(3, 3), polygon) == True
    assert isPointInPolygon(MyPoint(2, 7), polygon) == True
    assert isPointInPolygon(MyPoint(6, 14), polygon) == False
    assert isPointInPolygon(MyPoint(3, 3), polygon) == True
    assert isPointInPolygon(MyPoint(7, 8), polygon) == True
    assert isPointInPolygon(MyPoint(6, 14), polygon) == False
    print('Test 2: OK')

def testingSplitPolygonByLine(screen):
    def goAndPaint(polygon, line):
        screen.fill((0, 0, 0))
        drawGeneralizedSegment(screen, line, (462 % 256, 98, 78))
        DrawMyPolygon(screen, polygon, (462 % 256, 98, 78), 2)
        
        pygame.display.flip()
        ans = splitPolygonByLine(polygon, line)
        #print('---ANS:---:', len(ans[0]), len(ans[1]))
        num = 0
        for polygon in ans[0]:
        #    print(polygon)
            num += 100
            DrawMyPolygon(screen, polygon, (462 % 256, 98, 78), 1, (255, 0, num % 256))
        #print('------')
        for polygon in ans[1]:
        #    print(polygon)
            num += 100
            DrawMyPolygon(screen, polygon, (462 % 256, 98, 78), 1, (0, 255, num % 256))
        pygame.display.flip()
       # print('------')
       # print('Press \'y\' if it is correct splitting or \'n\' else') 
        while 1:
            end = False
            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    if event.key in [K_y, K_n]:
                        assert event.key == K_y
                        end = True
                        break
                else:
                    pass
            if end:
                break

    polygon = [MyPoint(0, 0), MyPoint(0, 200), MyPoint(200, 200), MyPoint(1, 0)]
    line = GeneralizedSegment(MyPoint(255, -1), MyPoint(255, -2), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(255, -21), MyPoint(255, -2), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(125, -21), MyPoint(125, -2), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(0, 200), MyPoint(200, 0), True, True)
    goAndPaint(polygon, line)
    #print('test 1: OK')

    polygon = [MyPoint(300, 400), MyPoint(100, 100), MyPoint(100, 700), MyPoint(600, 500), MyPoint(400, 100)]
    line = GeneralizedSegment(MyPoint(0, 100), MyPoint(0, 200), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(100, 100), MyPoint(600, 200), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(600, 200), MyPoint(100, 100), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(600, 200), MyPoint(100, 200), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(900, 600), MyPoint(600, 500), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(300, 400), MyPoint(600, 600), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(300, 400), MyPoint(600, 400), True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(300, 400), MyPoint(100, 100), True, True)
    goAndPaint(polygon, line)
    #print('test 2: OK')
    
    polygon = [MyPoint(2, 3), MyPoint(1, 12), MyPoint(3, 13), MyPoint(2, 6), MyPoint(6, 10),
               MyPoint(7, 7), MyPoint(6, 15), MyPoint(11, 14), MyPoint(12, 11), MyPoint(8, 10),
               MyPoint(9, 8), MyPoint(12, 7), MyPoint(13, 9), MyPoint(16, 10), MyPoint(15, 2),
               MyPoint(8, 2), MyPoint(8, 5), MyPoint(13, 5), MyPoint(13, 4), MyPoint(9, 4),
               MyPoint(9, 3), MyPoint(14, 3), MyPoint(14, 6), MyPoint(5, 5), MyPoint(3, 2)]
    scale = MyCipher(40)
    polygon = [point * scale for point in polygon]
    line = GeneralizedSegment(MyPoint(0, 0) * scale, MyPoint(1, 1) * scale, True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(0, 5) * scale, MyPoint(-1, 5) * scale, True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(9, 5) * scale, MyPoint(9, 100) * scale, True, True)
    goAndPaint(polygon, line)
    #print('test 3: OK')

    polygon = [MyPoint(2, 1), MyPoint(7, 1), MyPoint(8, 4), MyPoint(7, 3), MyPoint(7, 4), MyPoint(6, 4), MyPoint(6, 3), MyPoint(4, 3),
               MyPoint(5, 5), MyPoint(2, 5), MyPoint(3, 3), MyPoint(1, 3)]
    polygon = [point * scale for point in polygon]
    line = GeneralizedSegment(MyPoint(9, 3) * scale, MyPoint(100, 3) * scale, True, True)
    goAndPaint(polygon, line)
    line = GeneralizedSegment(MyPoint(9, 3) * scale, MyPoint(-100, 3) * scale, True, True)
    goAndPaint(polygon, line)
    #print('test 4: OK')
    
if __name__ == '__main__':
    def inputEvents(events):
        for event in events:
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit(0)
            else:
                pass

    def waitEnd():
        print('waiting for end')
        while 1:
            inputEvents(pygame.event.get())

    testingIsPointInPolygon()
    #sys.exit(0)

    pygame.init()
    size_x = 512 * 3 // 2
    size_y = 512 * 4
    window = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('My own little world')
    screen = pygame.display.get_surface()
    pygame.display.flip()
    testingSplitPolygonByLine(screen)
    #pygame.image.save(screen, 'testSave.bmp')
    waitEnd()

