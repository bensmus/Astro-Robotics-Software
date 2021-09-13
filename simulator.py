import random
from rover import Rover
from worldpoints import *

clock = pygame.time.Clock()

# Defining simulation speed
FPS = 1

# Defining colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 220)
RED = (255, 0, 0)
GREEN = (30, 200, 30)
BLUE = (20, 50, 200)
BROWN = 139,69,19


def setup(min_obstacle=5, max_obstacle=10, obstacle_count=30):
    """
    Set up the rover start and end points, and the obstacles.
    Returns:
    - wall_pts: set of Points
    - spawn_pts: set of Points
    """

    # WORLDSIZE - 1 is max_coor in general
    max_topleft = (WORLDSIZE - 1) - max_obstacle

    # [Rectangle(topleft, width, height)... ]
    rects = list()

    # The boundary points of every rectangle, without overlap -> one dimensional array
    # (for sonar).
    wall_pts = list()

    # As obstacles get created, pts will be removed from spawn possibilities
    spawn_pts = Rectangle(Point(0, 0), WORLDSIZE, WORLDSIZE).getAllPts()

    # Creating the obstacles.
    for i in range(obstacle_count):
        # Choosing a random point as well as dimensions, overlaps are okay.
        topleft = Point(random.randint(0, max_topleft),
                        random.randint(0, max_topleft))
        width = random.randint(min_obstacle, max_obstacle)
        height = random.randint(min_obstacle, max_obstacle)

        rect = Rectangle(topleft, width, height)
        rects.append(rect)
        spawn_pts -= rect.getAllPts()
        bound_pts = rect.getBoundPts()

        wall_pts.extend(bound_pts)

    # DO THIS OUTSIDE THE LOOP, WHEN ALL RECTS DEFINED
    # Filter the bound points. If they are inside (not on the edge of) an obstacle, they are removed.
    for rect in rects:
        wall_pts = set(
            filter(lambda point: not rect.contains(point), wall_pts))

    return wall_pts, spawn_pts


def wayfind(start, dest, wall_pts):
    """
    The algorithm in the rover class - rover.move() - requires:
    - list of obstacles (when the rover moves we get new obstacles),
    - rover position, start, dest

    That algorithm is called every frame, and outputs future rover position.
    """
    rover = Rover(start, dest)
    while rover.pos != dest:
        rover.scan(wall_pts)
        rover.move()
        drawWorldPts(BLUE, [rover.pos])
        pygame.display.update()
        clock.tick(FPS)
    

if __name__ == '__main__':

    wall_pts, spawn_pts = setup()
    SCREEN.fill(GRAY)  # reset everything
    drawWorldPts(BLACK, wall_pts)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # Getting worldpoint from mouse pos
                x, y = pygame.mouse.get_pos()
                screenpoint = Point(x, y, False)
                worldpoint = screenpoint.getWorldPt()
                
                if worldpoint in spawn_pts:
                    start = worldpoint
                    SCREEN.fill(GRAY)  # reset everything

                    drawWorldPts(BLACK, wall_pts)
                    drawWorldPts(BROWN, [worldpoint])
                    pygame.display.update()

                    # wait for second mouse click
                    waiting = True 
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                
                                # Getting worldpoint from mouse pos
                                x, y = pygame.mouse.get_pos()
                                screenpoint = Point(x, y, False)
                                worldpoint = screenpoint.getWorldPt()
                                
                                if worldpoint in spawn_pts:
                                    dest = worldpoint
                                    waiting = False 
                    
                    drawWorldPts(GREEN, [worldpoint])
                    pygame.display.update()

                    # WAYFINDING ALGORITHM
                    wayfind(start, dest, wall_pts)

    # Done! Time to quit.
    pygame.quit()

