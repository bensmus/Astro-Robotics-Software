from worldpoints import Point
from math import atan2
from typing import MutableSet


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


def filterFromAngleRanges(origin, points, angle_ranges) -> None:
    """Remove points that are in angle ranges"""
    for i, point in enumerate(points):
        # make sure that the point isn't in any of the angle_ranges
        for angle_range in angle_ranges:
            if inAngleRange(origin, point, angle_range):
                points.pop(i)
                break
    

def getAngleRanges(points):
    ...


class Rover:
    def __init__(self, start, dest):
        self.pos = start
        self.dest = dest
        self.scanned_pts = []
        self.scanradius = 10
    
    def scan(self, wall_pts):
        """Grows scanned_pts"""
        angle_ranges = []
        for radius in range(1, self.scanradius):
            circle = getCircle(radius, self.pos)
            # Don't scan obstacles that you cannot see
            filterFromAngleRanges(self.pos, circle, angle_ranges)
            just_scanned_pts = circle.intersection(wall_pts)
            self.scanned_pts.append(just_scanned_pts)
            # ! Implement get_angle_ranges
            angle_ranges.append(getAngleRanges(just_scanned_pts))
            
        
    
    def move(self):
        # Extremely dumb algo
        # self.pos.y += 1

        # Less dumb algo: doesn't go out of bounds, avoids obstacles
        ...
