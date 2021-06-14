from obstacle_creation_v1 import *
screen.fill(OFFWHITE)
bound = get_bound_pts((0, 0), (10, 10))
for pt in bound:
    pygame.draw.line(screen, RED, pt, pt)


pygame.display.update()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Done! Time to quit.
pygame.quit()
