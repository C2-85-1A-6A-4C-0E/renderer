import clss

FILENAME = "cube.3d"

def load(filename=FILENAME):
    solids = []
    with open(filename) as file:
        raw = file.read()
        for raw_solid in raw.split("==="):
            polys = []
            if len(raw_solid) == 0:
                break
            for raw_poly in raw_solid.split('---'):
                points = []
                if len(raw_poly) == 0:
                    break
                for raw_point in raw_poly.split('\n'):
                    point = [float(i) for i in raw_point.split() if "#" not in raw_point]
                    if len(point) == 3:
                        points.append(point)

                if len(points) > 2:
                    poly = clss.Poly3d(points)
                    polys.append(poly)

            if len(polys) > 1:
                solid = clss.Solid3d(polys)
                solids.append(solid)
        return solids