import pygame
pygame.init()

WORLDSIZE = 100
SCREENSIZE = 600  # should be a multiple of WORLDSIZE

SCREEN = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))

class Point:
    """
    Point with natural number coordinates,
    either a point in the world, or on the screen (scaled up world).
    """
    def __init__(self, x, y, worldpoint=True):
        self.x = x
        self.y = y
        self.worldpoint = worldpoint  # boolean value

    def raw(self):
        return (self.x, self.y)

    def scale(self, scalar):  
        # scaling changes worldpoint->screenpoint or screenpoint->worldpoint
        return Point(round(self.x * scalar), round(self.y * scalar), not self.worldpoint)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.worldpoint == other.worldpoint
        return False

    def __hash__(self):
        return hash(self.raw())

    def __str__(self):
        return f"x = {self.x}, y = {self.y}"
    
    def getScreenpoint(self):
        if self.worldpoint:
            return self.scale(SCREENSIZE / WORLDSIZE)
        else:
            raise RuntimeError("Point is already screenpoint")
    
    def getWorldpoint(self):
        if not self.worldpoint:
            return self.scale(WORLDSIZE / SCREENSIZE)
        else:
            raise RuntimeError("Point is already worldpoint")
    
    def draw(self, color):
        if self.worldpoint:
            raise RuntimeError("Cannot draw worldpoint")
        else:
            scalar = SCREENSIZE / WORLDSIZE
            pygame.draw.rect(SCREEN, color, (self.x, self.y, scalar, scalar))


class Rectangle:
    """
    Allows for: 
    - getting the outline points of the rectangle
    - getting all the points of the rectangle
    - checking if a point is contained within the rectangle
    """
    def __init__(self, topleft, width, height):
        self.topleft = topleft
        self.width = width
        self.height = height

    def get_bound_pts(self):
        """
        Get the points on the edge of the rectangle.
        """

        topleft = self.topleft
        width = self.width
        height = self.height

        # if width is 3, we have points 0, 1, 2
        # each pixel takes up space
        topright = Point(topleft.x + width - 1, topleft.y)
        bottomleft = Point(topleft.x, topleft.y + height - 1)
        bottomright = Point(topleft.x + width - 1, topleft.y + height - 1)

        bound_pts = []
        bound_pts.extend((topleft, topright, bottomleft, bottomright))
        bound_pts.extend(get_line_pts(topleft, topright, True))
        bound_pts.extend(get_line_pts(topright, bottomright, False))
        bound_pts.extend(get_line_pts(bottomleft, bottomright, True))
        bound_pts.extend(get_line_pts(topleft, bottomleft, False))

        return bound_pts

    def contains(self, point):
        """
        Check if point is contained within a rectangle.
        Edge points are not contained (> vs >=).
        """
        topleft = self.topleft
        width = self.width
        height = self.height

        min_x = topleft.x
        min_y = topleft.y
        max_x = min_x + width - 1
        max_y = min_y + height - 1
        if point.y > min_y and point.y < max_y and point.x > min_x and point.x < max_x:
            return True
        return False

    def get_all_points(self):
        """
        Returns set of all point objects.
        """
        topleft = self.topleft
        width = self.width
        height = self.height

        points = set()
        for x in range(topleft.x, topleft.x + width):
            for y in range(topleft.y, topleft.y + height):
                points.add(Point(x, y))
        return points


def draw_worldpoints(color, worldpoints):
    """
    Represent each worldpixel larger so we can see if we are doing everything properly
    """
    for point in worldpoints:
        screenpoint = point.getScreenpoint()
        screenpoint.draw(color)


def get_line_pts(point_a, point_b, horiz):
    """
    Interpolate, do not include a or b
    b needs to be more positive than a for this to work.
    """
    pts = []
    if horiz:
        for xcoor in range(point_a.x + 1, point_b.x):
            pts.append(Point(xcoor, point_a.y))
    else:
        for ycoor in range(point_a.y + 1, point_b.y):
            pts.append(Point(point_a.x, ycoor))
    return pts