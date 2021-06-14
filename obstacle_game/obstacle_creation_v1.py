'''
Coordinate system is (y, x),    y       x --->
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
import numpy.linalg as lin
import numpy as np
import random
pygame.init()


def get_bound_pts(topleft, dim):
    """Interpolate"""
    top = topleft[0]
    left = topleft[1]
    height = dim[0]
    width = dim[1]

    topright = (top, left + width)
    bottomleft = (top + height, left)
    bottomright = (top + height, left + width)

    bound_pts = []
    bound_pts.extend((topleft, topright, bottomleft, bottomright))
    bound_pts.extend(get_line_pts(topleft, topright, True))
    bound_pts.extend(get_line_pts(topright, bottomright, False))
    bound_pts.extend(get_line_pts(bottomleft, bottomright, True))
    bound_pts.extend(get_line_pts(topleft, bottomleft, False))

    return bound_pts


def get_line_pts(a, b, horiz):
    """
    Interpolate, do not include a or b
    b needs to be more positive than a for this to work
    """
    pts = []
    if horiz:
        for xcoor in range(a[1] + 1, b[1]):
            pts.append((a[0], xcoor))
    else:
        for ycoor in range(a[0] + 1, b[0]):
            pts.append((ycoor, a[1]))
    return pts


# Defining constants
WORLDSIZE = 1000
BLACK = (0, 0, 0)
OFFWHITE = (200, 200, 220)
RED = (255, 0, 0)

MAX_BOUNDING = 100
MIN_BOUNDING = 10
# max top or left for a bounding rectangle
MAX_COOR = WORLDSIZE - MAX_BOUNDING
OBSTACLE_COUNT = 20

# Set up the drawing window.
screen = pygame.display.set_mode([WORLDSIZE, WORLDSIZE])


if __name__ == '__main__':

    # Fill the background with white.
    screen.fill(OFFWHITE)

    # The topleft, dim of every rectangle
    topleft_dim = []  # [[(1, 2), (3, 4)]], for example

    # The boundary points of every rectangle
    # (for sonar)
    bound_pts_groups = []

    # The points unnocupied be rectangles
    # (for rover spawn locations)
    spawn_pts = []

    pixel_array = pygame.PixelArray(screen)

    for i in range(OBSTACLE_COUNT):
        topleft = (random.randint(0, MAX_COOR), random.randint(0, MAX_COOR))
        dim = (random.randint(MIN_BOUNDING, MAX_BOUNDING),
               random.randint(MIN_BOUNDING, MAX_BOUNDING))
        pygame.draw.rect(screen, BLACK, pygame.Rect(topleft, dim))
        topleft_dim.append([topleft, dim])
        bound_pts = get_bound_pts(topleft, dim)
        bound_pts_groups.append(bound_pts)
        
        # blit these bound_pts as a test
        for pt in bound_pts:
            pygame.draw.line(screen, RED, pt, pt)

    # Recognize the boundaries of the rectangles (sonar), as well as the points contained within them (spawn locations)
    # Get all points of the rectangle into a list

    # Update the display
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Done! Time to quit.
    pygame.quit()
