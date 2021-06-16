import pygame
import random
pygame.init()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def raw(self):
        return (self.x, self.y)

    def __str__(self):
        return f"x = {self.x}, y = {self.y}"


class Rectangle:
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

    def get_not_in_func(self):
        """
        Return a function that takes in a point, and checks if its contained within a rectangle.
        """
        topleft = self.topleft
        width = self.width
        height = self.height

        def f(point):
            min_x = topleft.x
            min_y = topleft.y
            max_x = min_x + width
            max_y = min_y + height
            if point.y > min_y and point.y < max_y and point.x > min_x and point.x < max_x:
                return False
            return True
        return f

    def get_set_all_points(self):
        """
        Get all the points of the rectangle.
        """
        topleft = self.topleft
        width = self.width
        height = self.height

        points = set()
        for x in range(topleft.x, topleft.x + width + 1):
            for y in range(topleft.y, topleft.y + height + 1):
                points.add((x, y))
        return points


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


def reset_start_dest(spawn_pts, start, dest):

    if start != None:
        # Clearing previous
        pygame.draw.circle(screen, BLUE, start, 2)
        pygame.draw.circle(screen, BLUE, dest, 2)

    start = random.choice(list(spawn_pts))
    dest = random.choice(list(spawn_pts - {start}))
    pygame.draw.circle(screen, PINK, start, 2)
    pygame.draw.circle(screen, PINK, dest, 2)
    return start, dest


# Defining constants.
WORLDSIZE = 1000
BLACK = (0, 0, 0)
OFFWHITE = (200, 200, 220)
RED = (117, 11, 11)
BLUE = (20, 50, 200)
PINK = (255, 0, 230)

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
    rects = list()

    # The boundary points of every rectangle, without overlap -> one dimensional array
    # (for sonar).
    wall_pts = list()

    # The points unnocupied by rectangles
    # (for rover spawn locations).
    spawn_pts = set()
    for x in range(WORLDSIZE):
        for y in range(WORLDSIZE):
            spawn_pts.add((x, y))

    # Creating the obstacles.
    for i in range(OBSTACLE_COUNT):
        # Choosing a random point as well as dimensions, overlaps are okay.
        topleft = Point(random.randint(0, MAX_COOR),
                        random.randint(0, MAX_COOR))
        width = random.randint(MIN_BOUNDING, MAX_BOUNDING)
        height = random.randint(MIN_BOUNDING, MAX_BOUNDING)

        # Drawing the black rectangle.
        pygame.draw.rect(screen, BLACK, (topleft.x, topleft.y, width, height))

        rect = Rectangle(topleft, width, height)
        rects.append(rect)
        spawn_pts -= rect.get_set_all_points()
        bound_pts = rect.get_bound_pts()

        wall_pts.extend(bound_pts)

    # DO THIS OUTSIDE THE LOOP, WHEN ALL RECTS DEFINED
    # Filter the bound points. If they are inside an obstacle, they are removed.
    for rect in rects:
        wall_pts = list(filter(rect.get_not_in_func(), wall_pts))

    # Draw the walls.
    for point in wall_pts:
        pygame.draw.line(screen, RED, point.raw(), point.raw())

    # Draw the spawn locations.
    for point in spawn_pts:
        pygame.draw.line(screen, BLUE, point, point)

    # Choose and draw 2 random start and destination points.
    start, dest = reset_start_dest(spawn_pts, None, None)

    # Print the first 20 obstacle points for fun
    for point in wall_pts[:20]:
        print(point)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start, dest = reset_start_dest(spawn_pts, start, dest)

        x, y = pygame.mouse.get_pos()
        print(f'mouse coordinates x = {x:-3}, y = {y:-3}', end='\r')
        pygame.display.update()

    # Done! Time to quit.
    pygame.quit()
