'''
Coordinate system is (x, y),    y       x --->
                                |
                                |
                                |
                                ∨
'''
'''
OBSTACLE CREATION TECHNIQUE
1.  Choose "n" random points in the worldsize
2.  Create bounding rectangles for all "n" points
3.  Do a chain circle growing technique from the middle until we create a bulbuous shape that touches the bounding rectangle,
    or until 5 iterations
'''

# Version 1 simplifies this obstacle creation technique, to have all obstacles be rectangles.

import pygame
import random
pygame.init()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def raw(self):
        return (self.x, self.y)


class Rectangle:
    def __init__(self, topleft, width, height):
        self.topleft = topleft
        self.width = width
        self.height = height


def get_bound_pts(topleft, width, height):
    """
    Get the points on the edge of the rectangle.
    """

    topright = Point(topleft.x + width, topleft.y)
    bottomleft = Point(topleft.x, topleft.y + height)
    bottomright = Point(topleft.x + width, topleft.y + height)

    bound_pts = []
    bound_pts.extend((topleft, topright, bottomleft, bottomright))
    bound_pts.extend(get_line_pts(topleft, topright, True))
    bound_pts.extend(get_line_pts(topright, bottomright, False))
    bound_pts.extend(get_line_pts(bottomleft, bottomright, True))
    bound_pts.extend(get_line_pts(topleft, bottomleft, False))

    return bound_pts


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


def not_in_rect(topleft, width, height):
    """
    Return a function that takes in a point, and checks if its contained within a rectangle.
    """
    def f(point):
        min_x = topleft.x
        min_y = topleft.y
        max_x = min_x + width
        max_y = min_y + height
        if point.y > min_y and point.y < max_y and point.x > min_x and point.x < max_x:
            return False
        return True
    return f


# Defining constants.
WORLDSIZE = 1000
BLACK = (0, 0, 0)
OFFWHITE = (200, 200, 220)
RED = (255, 0, 0)

MAX_BOUNDING = 100
MIN_BOUNDING = 10
# max top or left for a bounding rectangle
MAX_COOR = WORLDSIZE - MAX_BOUNDING
OBSTACLE_COUNT = 50

# Set up the drawing window.
screen = pygame.display.set_mode([WORLDSIZE, WORLDSIZE])


if __name__ == '__main__':

    # Fill the background with white.
    screen.fill(OFFWHITE)

    # [Rectangle(topleft, width, height)... ]
    rects = []

    # The boundary points of every rectangle, without overlap -> one dimensional array
    # (for sonar).
    wall_pts = []

    # The points unnocupied be rectangles
    # (for rover spawn locations).
    spawn_pts = []  # TODO

    # Creating the obstacles.
    for i in range(OBSTACLE_COUNT):
        # Choosing a random point as well as dimensions, overlaps are okay.
        topleft = Point(random.randint(0, MAX_COOR),
                        random.randint(0, MAX_COOR))
        width = random.randint(MIN_BOUNDING, MAX_BOUNDING)
        height = random.randint(MIN_BOUNDING, MAX_BOUNDING)

        # Drawing the black rectangle.
        pygame.draw.rect(screen, BLACK, (topleft.x, topleft.y, width, height))

        rects.append(Rectangle(topleft, width, height))
        bound_pts = get_bound_pts(topleft, width, height)

        # Filter the bound points. If they are inside an obstacle, they are removed.
        for rect in rects:
            bound_pts = filter(not_in_rect(
                rect.topleft, rect.width, rect.height), bound_pts)

        wall_pts.extend(bound_pts)

    # Draw the walls.
    for point in wall_pts:
        pygame.draw.line(screen, RED, point.raw(), point.raw())

    # Update the display
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Done! Time to quit.
    pygame.quit()
