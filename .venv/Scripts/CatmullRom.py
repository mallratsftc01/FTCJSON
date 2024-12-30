import math

SPLINE_SCALE = 0.5

class KeyPoint:

    def __init__(self, x, y, xd, yd):
        self.x = x
        self.y = y
        if (xd != None):
            self.xd = xd
        else:
            self.xd = 0
        if (yd != None):
            self.yd = yd
        else:
            self.yd = 1

    def __str__(self):
        return f"{self.x},{self.y}"

    def setxd(self, xd):
        self.xd = xd

    def setyd(self, yd):
        self.yd = yd

    def getTrajectory(self, t):
        if (t == None):
            t = 1
        x1: float = (self.xd * t) + self.x
        y1: float = (self.yd * t) + self.y
        return x1, y1


points: list[KeyPoint] = []
restriction = []


def h00(t):
    return (2 * math.pow(t, 3)) - (3 * math.pow(t, 2)) + 1


def h10(t):
    return math.pow(t, 3) - (2 * math.pow(t, 2)) + t


def h01(t):
    return (-2 * math.pow(t, 3)) + (3 * math.pow(t, 2))


def h11(t):
    return math.pow(t, 3) - math.pow(t, 2)


def hermite(t, p0, p1, m0, m1):
    return (h00(t) * p0) + (h10(t) * m0) + (h01(t) * p1) + (h11(t) * m1)


def interpolateArc(keypoint1: KeyPoint, keypoint2: KeyPoint, precision):
    kp: list[KeyPoint] = [keypoint1]
    # restriction.append(keypoint1)
    p = 10
    if (precision != None):
        p = precision
    i = 0
    while i <= p:
        x = hermite((i / p), keypoint1.x, keypoint2.x, keypoint1.xd, keypoint2.xd)
        y = hermite((i / p), keypoint1.y, keypoint2.y, keypoint1.yd, keypoint2.yd)
        kp.append(KeyPoint(x, y, None, None))
        # restriction.append(KeyPoint(x,y,None,None))
        # canvas.create_oval(x-HALF_LINE_SPACING,y-HALF_LINE_SPACING,x+HALF_LINE_SPACING,y+HALF_LINE_SPACING,width=0,tags=('space'))
        # canvas.create_line(kp[i].x, kp[i].y, x, y,tags=('path'))
        i += 1
    return kp


def plotKeypoint(x, y, precision):
    points.append(KeyPoint(x, y, None, None))
    if (len(points) == 2):
        xd = points[len(points) - 1].x - points[len(points) - 2].x
        yd = points[len(points) - 1].y - points[len(points) - 2].y
        x = points[len(points) - 2].x - xd
        y = points[len(points) - 2].y - yd
        points.insert(0, KeyPoint(x, y, xd, yd))
    if (len(points) > 2):
        xd = points[len(points) - 1].x - points[len(points) - 3].x
        yd = points[len(points) - 1].y - points[len(points) - 3].y
        points[len(points) - 2].setxd(xd * SPLINE_SCALE)
        points[len(points) - 2].setyd(yd * SPLINE_SCALE)
    if (len(points) > 3):
        return interpolateArc(points[len(points) - 3], points[len(points) - 2], precision)