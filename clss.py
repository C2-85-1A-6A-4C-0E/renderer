import math
class Point2d:
    def __init__(self, position, size=1):
        self.x = position[0]
        self.y = position[1]
        self.size = size

    def get(self):
        return (self.x, self.y), self.size

def random2dPoints(bounds, count, size=(1,1)):
    from random import randint
    xb = 0, bounds[0]
    yb = 0, bounds[1]
    pts = []
    for _ in range(count):
        pts.append(Point2d((randint(*xb), randint(*yb)), randint(*size)))
    return pts

class Line2d:
    def __init__(self, p1, p2):
        self.x1, self.y1 = p1
        self.x2, self.y2 = p2

    def get(self):
        return (self.x1, self.y1), (self.x2, self.y2)

def random2dLines(bounds, count):
    from random import randint
    xb = 0, bounds[0]
    yb = 0, bounds[1]
    lns = []
    for _ in range(count):
        lns.append(Line2d( (randint(*xb), randint(*yb)), (randint(*xb), randint(*yb)) ))
    return lns

class Poly2d:
    def __init__(self, points, solid=False):
        self.points = points
        self.solid = solid
    def get(self):
        return self.points, self.solid

def randomPoly2d(bounds, count, verts=(3,3), fill=False):
    import random, itertools
    try: len(fill)
    except TypeError: fill = [fill]
    xb = 0, bounds[0]
    yb = 0, bounds[1]
    poly = []
    for _, f in itertools.zip_longest(range(count), fill, fillvalue=fill[-1]):
        s = random.randint(*verts)
        vert = [(random.randint(*xb), random.randint(*yb)) for _ in range(s)]
        poly.append(Poly2d(vert, f))
    return poly

class Poly3d:
    def __init__(self, points, camera=(500,500,-1000)):
        self.points3d = points
        self.camera = camera
        self.points2d = []
        self.compiled = False

    def compile(self):
        self.points2d = []
        for point in self.points3d:
            x, y, z = [i-j for i,j in zip(point, self.camera)]
            u = (x / (z/1000)) + self.camera[0]
            v = (y / (z/1000)) + self.camera[1]
            self.points2d.append((u,v))

    def get(self):
        if not self.compiled:
            self.compile()
        return self.points2d, False

    def rotate(self, origin, xrot, yrot, zrot):
        def rot(origin, point, angle):
            ox, oy = origin
            px, py = point
            qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
            return qx, qy

        def rotate_point(point, origin, xrot, yrot, zrot):
            x, y, z = point
            x0, y0, z0 = origin
            x, y = rot((x0,y0), (x,y), math.radians(zrot))
            x, z = rot((x0,z0), (x,z), math.radians(yrot))
            y, z = rot((y0,z0), (y,z), math.radians(xrot))
            return x,y,z

        pts = []
        for point in self.points3d:
            pt = rotate_point(point, origin, xrot, yrot, zrot)
            pts.append(pt)
        self.points3d = pts

    def __str__(self):
        return "\t".join([str(i) for i in self.points3d])
