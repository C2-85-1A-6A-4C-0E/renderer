import math
import accel

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

def distance3d(a,b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    z = a[2] - b[2]
    return (x**2 + y**2 + z**2)**0.5

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
    def __init__(self, points, camera=(700,500,-1000)):
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
        return self.points2d, True

    def take(self):
        return self.points3d

    def set(self, pos):
        size = len(self.points3d)
        self.points3d = pos[:size]
        self.compiled = False

    def center(self):
        x = sum([x for x,y,z in self.points3d])/len(self.points3d)
        y = sum([y for x, y, z in self.points3d]) / len(self.points3d)
        z = sum([z for x, y, z in self.points3d]) / len(self.points3d)

        return x,y,z

    def depth(self):
        return max(distance3d(vertex, self.camera) for vertex in self.points3d)

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

    def translate(self, *, x=0, y=0, z=0):
        self.compiled = False
        trans = (x,y,z)
        newpos = []
        for point in self.points3d:
            newpos.append(tuple([i+j for i,j in zip(point, trans)]))
        self.points3d = newpos

    def __str__(self):
        return "\t".join([str(i) for i in self.points3d])

class Point3d:
    def __init__(self, position, size=1, camera=(700,500,-1000)):
        self.position3d = position
        self.size3d = size
        self.camera = camera
        self.position2d = None
        self.size2d = None
        self.compiled = False

    def compile(self):
        self.compiled = True
        x, y, z = [i - j for i, j in zip(self.position3d, self.camera)]
        u = (x / (z / 1000)) + self.camera[0]
        v = (y / (z / 1000)) + self.camera[1]
        self.position2d = int(u), int(v)
        self.size2d = int(max(self.size3d / (z/1000), 1))

    def take(self):
        return self.position3d

    def get(self):
        if not self.compiled:
            self.compile()
        return self.position2d, self.size2d

    def rotate(self, origin, xrot, yrot, zrot):
        self.compiled = False
        def rot(origin, point, angle):
            ox, oy = origin
            px, py = point
            qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
            return qx, qy

        x, y, z = self.position3d
        x0, y0, z0 = origin
        x, y = rot((x0, y0), (x, y), math.radians(zrot))
        x, z = rot((x0, z0), (x, z), math.radians(yrot))
        y, z = rot((y0, z0), (y, z), math.radians(xrot))

        self.position3d = x, y, z

    def translate(self, *, x=0, y=0, z=0):
        trans = (x,y,z)
        self.compiled = False
        self.position3d = tuple([i+j for i,j in zip(self.position3d, trans)])

def translate_polys(polys, offset):
    poss = []
    sets = [i.take() for i in polys]
    longest = len(max(sets, key=len))
    for s in sets:
        while len(s) < longest:
            s += (0,0,0)
        poss += s

    poss = accel.translate(poss, offset)
    for i, poly in zip(range(0,len(poss), longest), polys):
        poly.set(poss[i:i+longest])

def rotate_polys(polys, origin, rotation):
    poss = []
    sets = [i.take() for i in polys]
    longest = len(max(sets, key=len))
    for s in sets:
        while len(s) < longest:
            s += (0, 0, 0)
        poss += s

    poss = accel.rotate(poss, origin, rotation)

    for i, poly in zip(range(0,len(poss), longest), polys):
        poly.set(poss[i:i+longest])

def scale_polys(polys, origin, factor):
    poss = []
    sets = [i.take() for i in polys]
    longest = len(max(sets, key=len))
    for s in sets:
        while len(s) < longest:
            s += (0, 0, 0)
        poss += s

    poss = accel.scale(poss, origin, factor)

    for i, poly in zip(range(0, len(poss), longest), polys):
        poly.set(poss[i:i + longest])

class Solid3d:
    def __init__(self, polys, color=(0,255,25)):
        self.polys = polys
        self.color_edge = color
        self.color_fill = tuple([i//2 for i in color])

    def getPolys(self):
        return self.polys

    def export_polys(self, list):
        for poly in self.polys:
            list.append(poly)

    def translate(self, offset):
        translate_polys(self.polys, offset)

    def center(self):
        centers = [i.center() for i in self.polys]
        x = sum([x for x, y, z in centers]) / len(centers)
        y = sum([y for x, y, z in centers]) / len(centers)
        z = sum([z for x, y, z in centers]) / len(centers)
        return x, y, z

    def rotate(self, origin, rotation, degrees=True):
        if degrees: rotation = tuple([math.radians(i) for i in rotation])
        rotate_polys(self.polys, origin, rotation)

    def scale(self, origin, factor):
        scale_polys(self.polys, origin, factor)

    def size(self):
        c = self.center()
        centers = [i.center() for i in self.polys]
        return max(distance3d(i, c) for i in centers)