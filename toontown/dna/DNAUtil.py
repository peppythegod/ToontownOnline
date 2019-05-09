from panda3d.core import Vec4

def dgiExtractString8(dgi):
    return dgi.getString() #dgi.extractBytes(dgi.getUint8())

def dgiExtractColor(dgi):
    a, b, c, d = (dgi.getUint8() / 255.0 for _ in xrange(4))
    return Vec4(a, b, c, d)

