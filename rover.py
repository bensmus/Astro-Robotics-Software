from worldpoints import Point, drawWorldPts
from math import sin, cos, pi, dist
import pygame
import numpy as np


def getLine(origin, radius, angle):
    line = set()
    x = origin.x
    y = origin.y

    for r in range(radius):
        line.add(
            Point( x+r*cos(angle), y+r*sin(angle) ).getRounded()
            )
    
    return line


def getNetRepulsion(pos, scanned_pts):
    repulsion_vectors = np.empty((0, 2))
    
    for pt in scanned_pts:
        distance = dist(pos.raw(), pt.raw())
        repulsive_force = 1/distance**2
        
        direction_vector = np.array([[pos.x - pt.x, pos.y - pt.y]])
        unit_vector = direction_vector / distance
        repulsion_vector = unit_vector * repulsive_force
        repulsion_vectors = np.append(repulsion_vectors, repulsion_vector, axis=0)
    
    net_repulsion = np.sum(repulsion_vectors, axis=0) 
    return net_repulsion


class Rover:
    
    def __init__(self, start, dest):
        self.pos = start
        self.dest = dest
        self.scanned_pts = []
        self.scanradius = 15
    
    
    def scan(self, wall_pts):
        """Grows scanned_pts"""
        for angle in np.arange(-pi, pi, 0.01):
            for radius in range(1, self.scanradius):
                line = getLine(self.pos, radius, angle)
                just_scanned_pts = line.intersection(wall_pts)
                # drawWorldPts((0, 0, 255), line)
                if just_scanned_pts != set():  # move on to next angle
                    self.scanned_pts.extend(list(just_scanned_pts))
                    break
        drawWorldPts((0, 0, 255), self.scanned_pts)
        pygame.display.update()
            
    
    

    def move(self):
        # Extremely dumb algo
        # self.pos.y += 1

        # Less dumb algo: flow field
        net_repulsion = getNetRepulsion(self.pos, self.scanned_pts)
        unit_net_repulsion = net_repulsion / np.linalg.norm(net_repulsion)
        print(unit_net_repulsion)
        self.pos.x += unit_net_repulsion[0]
        self.pos.y += unit_net_repulsion[1]
        
