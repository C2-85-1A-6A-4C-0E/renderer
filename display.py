import pygame, pygame.locals, sys, time
from clss import *
from random import randint

SIZE = WIDTH, LENGTH = (1000, 1000)
BACKGROUND = (0,0,0)
FORGROUND = (0,255,25)

pygame.init()
screen = pygame.display.set_mode(SIZE)

screen.fill(BACKGROUND)
pygame.display.flip()

def render_points(points):
    for point in points:
        pos, size = point.get()
        pygame.draw.circle(screen, FORGROUND, pos, size)
    pygame.display.flip()

def render_lines(lines):
    for line in lines:
        p1, p2 = line.get()
        pygame.draw.line(screen, FORGROUND, p1, p2, 1)
    pygame.display.flip()

def render_polys(polys):
    lookup = {True:0, False:1}
    for poly in polys:
        pts, fill = poly.get()
        pygame.draw.polygon(screen, FORGROUND, pts, lookup[fill])
    pygame.display.flip()

if __name__ == "__main__":
    #points = random2dPoints(SIZE, 10, (1,5))
    #render_points(points)
    #lines = random2dLines(SIZE, 10)
    #render_lines(lines)
    #polys = randomPoly2d(SIZE, 3, (3,3), (True, False))
    #render_polys(polys)

    cube = [
        Poly3d(((250,250,0), (250,750,0), (250, 750, 500), (250, 250, 500))),
        Poly3d(((250,250,0), (750, 250, 0), (750, 250, 500), (250, 250, 500))),
        Poly3d(((250, 750, 0), (750, 750, 0), (750, 750, 500), (250, 750, 500))),
        Poly3d(((750, 250, 0), (750, 750, 0), (750, 750, 500), (750, 250, 500)))
    ]
    render_polys(cube)
    tick = time.time()
    count = 600
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        if time.time() > tick + .034:
            #print(len(cube))
            #print(*cube, sep='\n')
            screen.fill(BACKGROUND)
            tick = time.time()
            for poly in cube:
                poly.rotate((500,500,250), .5, -1, -.5)
            render_polys(cube)
            if count < 588:
                pygame.image.save(screen, f"frames/frame{count:04}.png")
                count += 1
