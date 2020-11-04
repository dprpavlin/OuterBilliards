import sys, pygame
from pygame.locals import *
from point2D import *

def IsValidPoint(surface, point):
    x, y = ToIntTuple(point)
    rect = surface.get_rect()
    return (x >= rect.x) and (x < rect.x + rect.w) and (y >= rect.y) and (y < rect.y + rect.h)

def DrawPoint(surface, point, color, fat=1):
    point = ToIntTuple(point) 
    pygame.draw.circle(surface, color, point, fat)





