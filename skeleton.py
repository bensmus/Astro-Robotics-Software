'''
Coordinate system is (y, x),    y       x --->
                                |
                                |
                                |
                                ∨
'''
import pygame
pygame.init()

WIDTH = 500
HEIGHT = 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the drawing window.
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Run until the user asks to quit.
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Registering key down events.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("LEFT")
            if event.key == pygame.K_d:
                print("RIGHT")

    # Fill the background with white.
    screen.fill(WHITE)

    # Draw stuff! Or whatever.

    # Update the display
    pygame.display.update()

# Done! Time to quit.
pygame.quit()
