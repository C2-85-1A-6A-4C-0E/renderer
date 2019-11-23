import numpy as np
from numba import vectorize
import math

def translate(origins, offset):
    ofx, ofy, ofz = offset
    x,y,z = [],[],[]
    for i in origins:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])

    x = np.array(x, dtype=np.float32)
    y = np.array(y, dtype=np.float32)
    z = np.array(z, dtype=np.float32)
    ofx = np.full(len(x), ofx, dtype=np.float32)
    ofy = np.full(len(y), ofy, dtype=np.float32)
    ofz = np.full(len(z), ofz, dtype=np.float32)

    if len(x) < 1000: f = trans_c
    else: f = trans_c

    nx = f(x, ofx)
    ny = f(y, ofy)
    nz = f(z, ofz)
    return list(zip(nx,ny,nz))

@vectorize(['float32(float32, float32)'], target='cuda')
def trans_c(start, off):
    return start + off

def trans(start, off):
    return start + off

@vectorize(['float32(float32, float32, float32)'], target='cuda')
def rotx_c(px, py, angle):
    qx = math.cos(angle) * (px) - math.sin(angle) * (py)
    return qx

def rotx(px, py, angle):
    qx = math.cos(angle) * (px) - math.sin(angle) * (py)
    return qx

@vectorize(['float32(float32, float32, float32)'], target='cuda')
def roty_c(px, py, angle):
    qy = math.sin(angle) * (px) + math.cos(angle) * (py)
    return qy

def roty(px, py, angle):
    qy = math.sin(angle) * (px) + math.cos(angle) * (py)
    return qy

def rot(px, py, angle):
    return rotx(px, py, angle), roty(px, py, angle)

def rot_c(px, py, angle):
    return rotx_c(px, py, angle), roty_c(px, py, angle)

def rotate(starts, origin, rotation):
    rox, roy, roz = rotation
    ox, oy, oz = origin
    x, y, z = [], [], []
    for i in starts:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])

    x = np.array(x, dtype=np.float32)
    y = np.array(y, dtype=np.float32)
    z = np.array(z, dtype=np.float32)

    ofx = np.full(len(x), -ox, dtype=np.float32)
    ofy = np.full(len(y), -oy, dtype=np.float32)
    ofz = np.full(len(z), -oz, dtype=np.float32)

    if len(x) < 1000:
        f = rot
        t = trans
    else:
        f = rot_c
        t = trans_c

    nx = t(x, ofx)
    ny = t(y, ofy)
    nz = t(z, ofz)

    nx, ny = f(nx, ny, roz)
    nx, nz = f(nx, nz, roy)
    ny, nz = f(ny, nz, rox)

    ofx = np.full(len(x), ox, dtype=np.float32)
    ofy = np.full(len(y), oy, dtype=np.float32)
    ofz = np.full(len(z), oz, dtype=np.float32)

    nx = t(nx, ofx)
    ny = t(ny, ofy)
    nz = t(nz, ofz)

    return list(zip(nx, ny, nz))

@vectorize(['float32(float32, float32, float32)'], target='cuda')
def sca_c(origin, start, factor):
    dist = start - origin
    dist = dist * factor
    pos = dist + origin
    return pos

def sca(origin, start, factor):
    dist = start - origin
    dist = dist * factor
    pos = dist + origin
    return pos

def scale(starts, origin, factor):
    ox, oy, oz = origin
    x, y, z = [], [], []
    for i in starts:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])

    x = np.array(x, dtype=np.float32)
    y = np.array(y, dtype=np.float32)
    z = np.array(z, dtype=np.float32)

    ofx = np.full(len(x), ox, dtype=np.float32)
    ofy = np.full(len(y), oy, dtype=np.float32)
    ofz = np.full(len(z), oz, dtype=np.float32)

    factor = np.full(len(x), factor, dtype=np.float32)

    if len(x) < 1000: f = sca
    else: f = sca_c

    x = f(ofx, x, factor)
    y = f(ofy, y, factor)
    z = f(ofz, z, factor)
    return list(zip(x, y, z))
