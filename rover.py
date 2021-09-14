from worldpoints import Point, drawWorldPts
from math import sin, cos, pi
from typing import MutableSet, List
import pygame
from time import sleep
from numpy import arange


def getLine(origin, radius, angle):
    line = set()
    x = origin.x
    y = origin.y

    for r in range(radius):
        line.add(
            Point( x+r*cos(angle), y+r*sin(angle) ).getRounded()
            )
    
    return line


class Rover:
    def __init__(self, start, dest):
        self.pos = start
        self.dest = dest
        self.scanned_pts = []
        self.scanradius = 25
    
    def scan(self, wall_pts):
        """Grows scanned_pts"""
        for angle in arange(-pi, pi, 0.001):
            for radius in range(1, self.scanradius):
                line = getLine(self.pos, radius, angle)
                just_scanned_pts = line.intersection(wall_pts)
                # drawWorldPts((0, 0, 255), line)
                if just_scanned_pts != set():  # move on to next angle
                    self.scanned_pts.extend(list(just_scanned_pts))
                    break
        drawWorldPts((0, 0, 255), self.scanned_pts)
        pygame.display.update()
        breakpoint()
            
            
        
    
    def move(self):
        # Extremely dumb algo
        # self.pos.y += 1

        # Less dumb algo: doesn't go out of bounds, avoids obstacles
        ...
