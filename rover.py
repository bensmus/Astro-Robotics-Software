from worldpoints import Point, drawWorldPts
from math import asin, atan2, dist, sqrt
from typing import MutableSet, List
import pygame
from time import sleep

def getCircle(radius, origin) -> MutableSet[Point]:
    """
    Midpoint circle algorithm.
    Gives you the best circle without fractional point values.
    Adapted from http://rosettacode.org/wiki/Bitmap/Midpoint_circle_algorithm#Python
    """

    x0 = origin.x
    y0 = origin.y
    f = 1 - radius 
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius 

    # starting points at 0 deg, 90 deg, 180 deg, 270 deg
    points = {
        Point(x0, y0 + radius), 
        Point(x0, y0 - radius), 
        Point(x0 + radius, y0),
        Point(x0 - radius, y0)
    }

    # think about one of the octants, then mirror
    while x < y:
        if f >= 0:
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x
        points.add(Point(x0 + x, y0 + y))
        points.add(Point(x0 - x, y0 + y))
        points.add(Point(x0 + x, y0 - y))
        points.add(Point(x0 - x, y0 - y))
        points.add(Point(x0 + y, y0 + x))
        points.add(Point(x0 - y, y0 + x))
        points.add(Point(x0 + y, y0 - x))
        points.add(Point(x0 - y, y0 - x))

    return points


def inAngleRange(origin, point, angle_range) -> bool: 
    """Determine if point is in range of certain angles"""
    angle = atan2(origin.y - point.y, origin.x - point.x)  # atan2 returns angles between -pi and pi radians
    return angle_range[0] <= angle and angle <= angle_range[1]


def filterFromAngleRanges(origin, points, angle_ranges) -> List[Point]:
    """Remove points that are in angle ranges"""
    points_list = list(points)
    for i, point in enumerate(points_list):
        # make sure that the point isn't in any of the angle_ranges
        for angle_range in angle_ranges:
            if inAngleRange(origin, point, angle_range):
                points_list.pop(i)
                break
    return points_list


def getAngleRange(origin, point):
    """
    Description:
    Each point gets an angle range. 
    Closer points take up a larger range of angles,
    further points take up a smaller range of angles.

    Implementation:
    s = distance from the middle of each pixel
    a = angle between the two pixels can then be calculated using atan2
    b = asin( (sqrt(2)/2) / s )
    minangle = a - b
    maxangle = a + b
    """
    # !
    widener = 2

    origin_mp = Point(point.x - 0.5, point.y - 0.5)
    point_mp = Point(origin.x - 0.5, origin.y - 0.5)
    s = dist(origin_mp.raw(), point_mp.raw())
    a = atan2(point_mp.y - origin_mp.y, point_mp.x - origin_mp.x)
    b =  asin(sqrt(2)/2 / s)
    minangle = a - b - widener
    maxangle = a + b + widener
    return minangle, maxangle

    
def getAngleRanges(origin, points):
    angle_ranges = []
    for point in points:
        angle_ranges.append(getAngleRange(origin, point))
    return angle_ranges


class Rover:
    def __init__(self, start, dest):
        self.pos = start
        self.dest = dest
        self.scanned_pts = []
        self.scanradius = 25
    
    def scan(self, wall_pts):
        """Grows scanned_pts"""
        angle_ranges = []
        for radius in range(1, self.scanradius):
            circle = getCircle(radius, self.pos)
            # Don't scan obstacles that you cannot see
            print(angle_ranges)
            scan_wave = filterFromAngleRanges(self.pos, circle, angle_ranges)
            drawWorldPts((0, 0, 255), scan_wave)
            pygame.display.update()
            sleep(1)
            just_scanned_pts = set(scan_wave).intersection(wall_pts)
            if just_scanned_pts != set():
                angle_ranges.extend(getAngleRanges(self.pos, just_scanned_pts))
                self.scanned_pts.append(just_scanned_pts)
            
            
        
    
    def move(self):
        # Extremely dumb algo
        # self.pos.y += 1

        # Less dumb algo: doesn't go out of bounds, avoids obstacles
        ...
