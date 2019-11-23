import pygame, pygame.locals, sys, time
from clss import *
from random import randint
import loader

SIZE = WIDTH, LENGTH = (1400, 1000)
BACKGROUND = (0,0,0)
FORGROUND = (0,255,25)
MIDGROUND = (0,127,12)

pygame.init()
screen = pygame.display.set_mode(SIZE)

screen.fill(BACKGROUND)
pygame.display.flip()

def render_points(points):
    for point in points:
        pos, size = point.get()
        pygame.draw.circle(screen, FORGROUND, pos, size)
    #pygame.display.flip()

def render_lines(lines):
    for line in lines:
        p1, p2 = line.get()
        pygame.draw.line(screen, FORGROUND, p1, p2, 1)

def render_polys(polys):
    lookup = {True:0, False:1}
    polys = sorted(polys, key=lambda x:x.depth(), reverse=True )
    for poly in polys:
        pts, edge, fill = poly.get()
        if fill is not None:
            pygame.draw.polygon(screen, fill, pts, 0)
        pygame.draw.polygon(screen, edge, pts, 1)

def render_solid(solid):
    polys = solid.getPolys()
    polys = sorted(polys, key=lambda x: x.depth(), reverse=True)
    for poly in polys:
        pts, fill = poly.get()
        if fill:
            pygame.draw.polygon(screen, solid.color_fill, pts, 0)
        pygame.draw.polygon(screen, solid.color_edge, pts, 1)

if __name__ == "__main__":

    #cube = Solid3d([
    #    Poly3d(((50,250,0), (50,750,0), (50, 750, 500), (50, 250, 500))),
    #    Poly3d(((50,250,0), (550, 250, 0), (550, 250, 500), (50, 250, 500))),
    #    Poly3d(((50, 750, 0), (550, 750, 0), (550, 750, 500), (50, 750, 500))),
    #    Poly3d(((550, 250, 0), (550, 750, 0), (550, 750, 500), (550, 250, 500))),
    #    Poly3d(((50, 250, 0), (550, 250, 0), (550, 750, 0), (50, 750, 0))),
    #    Poly3d(((50, 250, 500), (550, 250, 500), (550, 750, 500), (50, 750, 500)))
    #])
    #cube2 = Solid3d([
    #    Poly3d(((50, 250, 0), (50, 750, 0), (50, 750, 500), (50, 250, 500))),
    #    Poly3d(((50, 250, 0), (550, 250, 0), (550, 250, 500), (50, 250, 500))),
    #    Poly3d(((50, 750, 0), (550, 750, 0), (550, 750, 500), (50, 750, 500))),
    #    Poly3d(((550, 250, 0), (550, 750, 0), (550, 750, 500), (550, 250, 500))),
    #    Poly3d(((50, 250, 0), (550, 250, 0), (550, 750, 0), (50, 750, 0))),
    #    Poly3d(((50, 250, 500), (550, 250, 500), (550, 750, 500), (50, 750, 500)))
    #])
    #cube2.translate((800,0,0))
    #print(cube2.size())
    raw = loader.load()
    for solid in raw:
        solid.setColor(FORGROUND)
        #solid.setWireframe()


    cube = raw[0]
    cube.setColor((0,25,250))
    raw[2].rotate(cube.center(), (180,0,0))
    tick = time.time()
    count = 600
    rotation = 1, 0, 1
    grow = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        if time.time() > tick + (1/60):
            print(1/(time.time() - tick))
            #print(len(cube))
            #print(*cube, sep='\n')
            screen.fill(BACKGROUND)
            tick = time.time()
            polys = []
            for solid in raw:
                solid.export_polys(polys)

            render_polys(polys)
            for solid in raw:
                solid.rotate(cube.center(), rotation)
            #render_solid(cube2)
            #cube.rotate(cube.center(),rotation)
            #cube2.rotate(cube2.center(), rotation2)

            #if cube2.size() > 300:
            #    grow = False
            #elif cube2.size() < 200:
            #    grow = True
            #if not grow:
            #    cube2.scale(cube2.center(), 0.99)
            #    cube.translate((-5,-5,-5))
            #else:
            #    cube2.scale(cube2.center(), 1.01)
            #    cube.translate((5,5,5))

            pygame.display.flip()
            if count < 588:
                pygame.image.save(screen, f"frames/frame{count:04}.png")
                count += 1
